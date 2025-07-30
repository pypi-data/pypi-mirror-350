# hyperbeam

Hyperbeam is a Python library designed to provide intelligent search tooling. 

## Features

- Search via DuckDuckGo for text, news, videos, and images.
- Optional integration with ScraperAPI for proxied requests.
- Standardized output schema for search results across different modes.
- Site-specific search limiting.

## Prerequisites

- Python 3.10+ (as seen in your virtual environment path)
- [uv](https://github.com/astral-sh/uv): A fast Python package installer and resolver, written in Rust.
- A ScraperAPI API key.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/hyprbm/hyperbeam.git
    cd hyperbeam
    ```

2.  **Set up the environment variable for ScraperAPI:**
    Create a `.env` file in the root of the project directory and add your ScraperAPI key:
    ```
    SCRAPERAPI_API_KEY="your_actual_api_key_here"
    ```
    Alternatively, you can set this environment variable directly in your system.
    The `src/web_search.py` module will raise a ValueError if this key is not set.

3.  **Create a virtual environment and install dependencies using uv:**
    ```bash
    uv venv # Create a virtual environment (e.g., .venv)
    source .venv/bin/activate # Activate the virtual environment (Linux/macOS)
    # For Windows (PowerShell): .venv\Scripts\Activate.ps1
    # For Windows (CMD): .venv\Scripts\activate.bat
    ```
    If you have a `requirements.txt` file:
    ```bash
    uv pip install -r requirements.txt
    ```
    If your project is packaged with `pyproject.toml` and you want to install it (e.g., in editable mode for development):
    ```bash
    uv pip install -e .
    ```
    (Ensure your `pyproject.toml` is configured correctly for this.)

## Usage

The primary search functionality can be accessed via the `web_search` function in `src/web_search.py`.

Example (from `src/example.ipynb` or a Python script):

```python
from src.web_search import web_search, ddgs_scraperapi_patch

# Important: If you want to use ScraperAPI for all DDGS calls,
# ensure SCRAPERAPI_API_KEY is set in your environment and then call the patch:
ddgs_scraperapi_patch()

# Perform a text search
text_results = web_search(keywords="latest advancements in AI", mode="text")
for result in text_results[:2]: # Print first two results
    print(result)

# Perform a news search for the last week
news_results = web_search(keywords="python programming news", mode="news", timeframe="w")
for result in news_results[:2]:
    print(result)

# Perform a video search
video_results = web_search(keywords="uv python tutorial", mode="video")
for result in video_results[:2]:
    print(result)
```

Refer to the `src/example.ipynb` notebook for more detailed examples and to experiment with the different search modes and parameters.

## Development

(Optional: Add details about running tests, linters, or contributing guidelines here if applicable.)
