# hyperbeam

Hyperbeam is a Python library designed to provide intelligent search tooling. 

## Features

- Search via DuckDuckGo for text, news, videos, and images.
- Optional integration with ScraperAPI for proxied requests.
- Standardized output schema for search results across different modes.
- Site-specific search limiting.
- LLM-powered guided search query generation.

## Installation

You can install `hyperbeam` directly from PyPI using pip (or any pip-compatible package manager like uv):

```bash
pip install hyperbeam
```

Or using uv:

```bash
uv pip install hyperbeam
```

**Prerequisites for Usage:**

- Python 3.10+
- If you plan to use the ScraperAPI integration: a ScraperAPI API key set as the environment variable `SCRAPERAPI_API_KEY`.
- For `guided_search_queries`: OpenAI API key (`OPENAI_API_KEY`) and/or Groq API key (`GROQ_API_KEY`) set as environment variables, depending on the chosen LLM.

## Usage

Once installed, you can import and use functions from the `hyperbeam` package:

### Web Search

The `web_search` function allows you to perform searches using DuckDuckGo:

```python
from hyperbeam import web_search, ddgs_scraperapi_patch

# To use standard DuckDuckGo search (no ScraperAPI):
# Perform a text search
text_results = web_search(keywords="latest advancements in AI", mode="text")
for result in text_results[:2]: # Print first two results
    print(result)

# Perform a news search for the last week
news_results = web_search(keywords="python programming news", mode="news", timeframe="w")
for result in news_results[:2]:
    print(result)

# To use ScraperAPI for proxied requests:
# 1. Ensure the SCRAPERAPI_API_KEY environment variable is set.
# 2. Call the patch function *once* in your application startup.
try:
    ddgs_scraperapi_patch()
    print("ScraperAPI patch applied successfully.")
except ValueError as e:
    print(f"ScraperAPI patch could not be applied: {e}")
    print("Proceeding without ScraperAPI.")

# Example call after attempting to patch (will use ScraperAPI if patch was successful and key was set):
video_results_via_scraper = web_search(keywords="uv python tutorial", mode="video", timeframe = "y")
if video_results_via_scraper:
    print("\nVideo results (potentially via ScraperAPI if patched):")
    for result in video_results_via_scraper[:5]:
        print(result)
```

### Guided Search Query Generation

The `guided_search_queries` function uses a Large Language Model (LLM) to generate a list of diverse search queries based on an initial user message. This can help in exploring different facets of a search topic.

**Prerequisites:**
- Ensure `OPENAI_API_KEY` (for GPT models) or `GROQ_API_KEY` (for Llama models via Groq) environment variables are set.

```python
from hyperbeam import guided_search_queries
from hyperbeam.typing import Message # Or define your own Message structure if not importing

# Example messages (replace with your actual message history)
messages: list[Message] = [
    {"role": "user", "content": "What are the best ways to learn a new programming language?"},
    # Add more messages if relevant to your use case, 
    # though guided_search_queries currently uses the last message.
]

try:
    suggested_queries = guided_search_queries(messages=messages)
    print("\nSuggested search queries:")
    for query_info in suggested_queries:
        print(query_info)
except Exception as e:
    print(f"Error generating guided search queries: {e}")

# Example with a Llama model via Groq (ensure GROQ_API_KEY is set)
# from hyperbeam.constants import GUIDED_SEARCH_MODEL # Default is GPT
# messages_for_llama: list[Message] = [
#     {"role": "user", "content": "planning a trip to Kyoto"},
# ]
# try:
#     # You might need to adjust GUIDED_SEARCH_MODEL in constants.py 
#     # or pass the model directly if the function signature allows
#     suggested_queries_llama = guided_search_queries(
#         messages=messages_for_llama, 
#         llm_model="llama3-8b-8192" # Example Llama model available on Groq
#     )
#     print("\nSuggested_queries_llama search queries:")
#     for query_info in suggested_queries_llama:
#         print(query_info)
# except Exception as e:
#     print(f"Error generating guided search queries with Llama: {e}")

```

For more detailed examples, including how to set up and use the ScraperAPI patch effectively, refer to the example notebooks or documentation within the repository (once available).

## Development Setup

If you want to contribute to `hyperbeam` or install it for development purposes:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/hyprbm/hyperbeam.git
    cd hyperbeam
    ```

2.  **Recommended: Set up a virtual environment using `uv` (or your preferred tool):**
    ```bash
    uv venv # Create a virtual environment (e.g., .venv)
    source .venv/bin/activate # Activate (Linux/macOS)
    # For Windows (PowerShell): .venv\Scripts\Activate.ps1
    # For Windows (CMD): .venv\Scripts\activate.bat
    ```

3.  **Install in editable mode with development dependencies:**
    This project uses `pyproject.toml` for packaging.
    ```bash
    uv pip install -e .[development]
    ```
    The `[development]` extra includes tools like linters and formatters (e.g., black, flake8, isort).

4.  **Set up Environment Variables for Development (Optional):**
    If you'll be testing the ScraperAPI integration during development, create a `.env` file in the project root:
    ```env
    SCRAPERAPI_API_KEY="your_actual_api_key_here"
    OPENAI_API_KEY="your_openai_api_key_here"
    GROQ_API_KEY="your_groq_api_key_here"
    ```
    The library itself (when used as a package) relies on the environment variable being set directly in the execution environment, but for development, a `.env` file can be convenient if you use a tool that loads it (like `python-dotenv` specified in `dev` dependencies, often used in test runners or scripts).

## Contributing

(Optional: Add details about running tests, linters, or specific contribution guidelines here if applicable.)
