import logging
import os
import time
from functools import lru_cache
from types import SimpleNamespace
from typing import Any
from typing import cast
from urllib.parse import urlencode

from duckduckgo_search import DDGS
from duckduckgo_search.exceptions import DuckDuckGoSearchException
from duckduckgo_search.exceptions import RatelimitException
from duckduckgo_search.exceptions import TimeoutException
from duckduckgo_search.utils import _extract_vqd
from scraperapi_sdk import ScraperAPIClient

LOGGER = logging.getLogger("web_search")

# Initialize SCRAPER_API_CLIENT to None. It will be set in ddgs_scraperapi_patch()
SCRAPER_API_CLIENT: ScraperAPIClient | None = None


def _get_url(
    self,
    method: str,
    url: str,
    params: dict[str, str] | None = None,
    content: bytes | None = None,
    data: dict[str, str] | bytes | None = None,
) -> SimpleNamespace:
    """Patches DDGS._get_url to use ScraperAPIClient for making HTTP requests.

    This method is intended to replace the internal _get_url method of a DDGS
    instance when the ScraperAPI patch is applied. It routes HTTP requests
    through the ScraperAPI service.

    :param self: The DDGS instance.
    :param method: HTTP method (e.g., 'GET', 'POST').
    :param url: The target URL for the request.
    :param params: Optional dictionary of URL parameters.
    :param content: Optional bytes content for the request body (rarely used with GET/POST data).
    :param data: Optional dictionary or bytes for the POST request body.
    :raises DuckDuckGoSearchException: If a general error occurs during the request
                                     or if the response status indicates an issue.
    :raises TimeoutException: If the request times out.
    :raises RatelimitException: If a ratelimit status code (202, 301, 403) is received.
    :return: A SimpleNamespace object with a `content` attribute containing the response body as bytes.
    """
    if hasattr(self, "_exception_event") and self._exception_event.is_set():
        raise DuckDuckGoSearchException("Exception occurred in previous call.")
    try:
        original_url = url
        if params is not None:
            url = f"{original_url}?{urlencode(params)}"
        resp = SCRAPER_API_CLIENT.make_request(
            url=url, method=method, data=data, timeout=15
        )
    except Exception as ex:
        if hasattr(self, "_exception_event"):
            self._exception_event.set()
        if "time" in str(ex).lower():
            raise TimeoutException(f"{url} {type(ex).__name__}: {ex}") from ex
        raise DuckDuckGoSearchException(f"{url} {type(ex).__name__}: {ex}") from ex
    LOGGER.debug(f"_get_url() {resp.url} {resp.status_code} {len(resp.content)}")
    if resp.status_code == 200:
        return SimpleNamespace(content=cast(bytes, resp.content))
    if hasattr(self, "_exception_event"):
        self._exception_event.set()
    if resp.status_code in (202, 301, 403):
        raise RatelimitException(f"{resp.url} {resp.status_code} Ratelimit")
    raise DuckDuckGoSearchException(
        f"{resp.url} return None. {params=} {content=} {data=}"
    )


@lru_cache
def _get_vqd(self, keywords: str) -> str:
    """Patches DDGS._get_vqd to obtain the VQD token for a search query via ScraperAPI.

    VQD (Vastly Quick Dispatcher) is a token used by DuckDuckGo for search sessions.
    This method uses the patched _get_url (which uses ScraperAPI) to fetch the VQD.

    :param self: The DDGS instance.
    :param keywords: The search keywords to obtain a VQD for.
    :raises Exception: If VQD extraction fails after multiple attempts.
    :return: The extracted VQD token as a string.
    """
    attempts = 1
    total_attempts = 3
    while True:
        try:
            response_object = self._get_url(
                "POST", "https://duckduckgo.com", data={"q": keywords}
            )
            vqd = _extract_vqd(response_object.content, keywords)
            LOGGER.debug(f"_get_vqd succeeded after {attempts} attempts")
            return vqd
        except Exception as e:
            LOGGER.warning(
                f"_get_vqd failed {attempts} out of {total_attempts} attempts. Error: {e}"
            )
            if attempts >= total_attempts:
                LOGGER.error(f"_get_vqd failed {attempts} attempts. Last error: {e}")
                raise
            attempts += 1
            time.sleep(0.5 * attempts)


def ddgs_scraperapi_patch():
    """Applies patches to the DDGS class to use ScraperAPI.

    This function replaces the internal `_get_url` and `_get_vqd` methods
    of the `duckduckgo_search.DDGS` class with custom versions that route
    requests through the ScraperAPI service.
    This should be called once if ScraperAPI integration is desired for all
    DDGS instances.

    :raises ValueError: If the SCRAPERAPI_API_KEY environment variable is not set.
    """
    global SCRAPER_API_CLIENT # Declare that we are modifying the global variable
    api_key = os.getenv("SCRAPERAPI_API_KEY")
    if not api_key:
        raise ValueError(
            "SCRAPERAPI_API_KEY environment variable is not set. "
            "It is required to use the ScraperAPI patch."
        )
    SCRAPER_API_CLIENT = ScraperAPIClient(api_key=api_key)
    
    DDGS._get_url = _get_url
    DDGS._get_vqd = _get_vqd


def _standardize_result(item: dict, mode: str) -> dict:
    """Converts a DDGS result item to a standard schema.
    
    Maps fields from various DDGS search modes (text, news, video, image)
    to a common dictionary structure.
    
    :param item: A dictionary representing a single search result from DDGS.
    :param mode: The search mode (e.g., 'text', 'news') that produced the item.
    :return: A dictionary with a standardized set of keys.
    """
    standardized = {
        "type": mode,
        "title": None,
        "url": None,
        "body": None,
        "image_url": None,
        "source": None,
        "date_published": None,
        "original_data": item,  # Store the original item
    }

    if mode == "text":
        standardized["title"] = item.get("title")
        standardized["url"] = item.get("href")
        standardized["body"] = item.get("body")
    elif mode == "news":
        standardized["title"] = item.get("title")
        standardized["url"] = item.get("url")
        standardized["body"] = item.get("body")
        standardized["image_url"] = item.get("image")
        standardized["source"] = item.get("source")
        standardized["date_published"] = item.get("date")  # Already in ISO-like format
    elif mode == "video":
        standardized["title"] = item.get("title")
        standardized["url"] = item.get("content")  # 'content' seems to be the video URL
        standardized["body"] = item.get("description")
        if isinstance(item.get("images"), dict):
            standardized["image_url"] = item.get("images", {}).get("large") or item.get(
                "images", {}
            ).get("medium")
        standardized["source"] = item.get("publisher") or item.get("provider")
        standardized["date_published"] = item.get("published")
        # You might want to add 'duration', 'embed_url' etc. to original_data or specific fields
    elif mode == "image":
        standardized["title"] = item.get("title")
        standardized["url"] = item.get("url")  # URL of the page containing the image
        standardized["image_url"] = item.get("image")  # Direct URL to the image
        standardized["source"] = item.get("source")
        # body for image might be an alt text or not directly available in typical DDGS image
        # results.
        # date_published is also not commonly available for images.

    return standardized


def _format_included_site_query(urls: list[str]) -> str:
    """Formats a list of URLs into a DuckDuckGo 'site:' query string portion.

    :param urls: A list of URLs to restrict the search to.
    :return: A string formatted for inclusion in a DDG query (e.g., "(site:example.com OR site:another.org)"),
             or an empty string if the input list is empty.
    """
    if not urls:
        return ""
    return "(" + " OR ".join(f"site: {u}" for u in urls) + ")"


def web_search(
    keywords: str,
    timeframe: str = None,
    mode: str = "text",
    safesearch: str = "moderate",
    region: str = "wt-wt",
    limit_sites: list[str] = [],
) -> list[dict[str, Any]]:
    """Performs a DuckDuckGo search using the DDGS library and returns standardized results.

    This function supports various search modes (text, news, image, video) and allows
    for site-restricted searches. Results are standardized into a common schema.

    :param keywords: The search keywords.
    :param timeframe: Time limit for the search (e.g., 'd' for day, 'w' for week, 'm' for month).
    :param mode: The type of search to perform ('text', 'news', 'image', 'video').
    :param safesearch: Safesearch level ('moderate', 'strict', 'off').
    :param region: Region for the search (e.g., 'wt-wt' for worldwide, 'us-en' for US English).
    :param limit_sites: A list of URLs to restrict the search to (e.g., ["example.com", "another.org"]).
    :raises ValueError: If an invalid `mode` is specified.
    :return: A list of dictionaries, where each dictionary represents a standardized search result.
    """
    ddgs = DDGS()
    results = []
    included_site_query = _format_included_site_query(limit_sites)
    if included_site_query:
        keywords = f"{keywords} {included_site_query}"

    raw_results: list[dict[str, Any]] | None = [] # Ensure raw_results is initialized

    if mode == "news":
        raw_results = ddgs.news(
            keywords,
            timelimit=timeframe,
            safesearch=safesearch,
            region=region,
            max_results=20 if timeframe else 50,
        )
    elif mode == "image":
        # time frame doesn't work for some reason (?)
        raw_results = ddgs.images(
            keywords, timelimit=None, safesearch=safesearch, region=region
        )
    elif mode == "video":
        raw_results = ddgs.videos(
            keywords,
            timelimit=timeframe,
            safesearch=safesearch,
            region=region,
            max_results=20 if timeframe else 50,
        )  # videos() requires max_results
    elif mode == "text":
        raw_results = ddgs.text(
            keywords, timelimit=timeframe, safesearch=safesearch, region=region
        )
    else:
        raise ValueError(f"Invalid mode: {mode}")

    if raw_results:  # Ensure there are results before trying to standardize
        for item in raw_results:
            if item: # Check if item is not None
                results.append(_standardize_result(item, mode))
    return results
