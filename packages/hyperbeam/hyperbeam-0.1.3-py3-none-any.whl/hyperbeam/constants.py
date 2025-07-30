RESPONSE_WORD_LIMIT = 250

SYSTEM_MESSAGE = [
    {
        "content": f"Provide an answer in {RESPONSE_WORD_LIMIT} words or less",
        "role": "system",
    }
]

GUIDED_SEARCH_MODEL = "gpt-4.1-mini"
