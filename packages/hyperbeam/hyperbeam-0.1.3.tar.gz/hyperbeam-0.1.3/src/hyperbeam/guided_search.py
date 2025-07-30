import os
import time
from datetime import datetime
from functools import cache
from typing import Any

from openai import OpenAI

from hyperbeam.constants import GUIDED_SEARCH_MODEL
from hyperbeam.constants import SYSTEM_MESSAGE
from hyperbeam.prompts import GUIDED_SEARCH_PROMPT_V2
from hyperbeam.typing import Message

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


def llm_call(
    model: str,
    messages: list[Message],
    system_message: list = SYSTEM_MESSAGE,
    max_tokens: int = 1500,
    temperature=None,
) -> dict:
    """Makes a call to a large language model (LLM) and returns the response.

    This function supports models from OpenAI (GPT series) and Groq (Llama series).
    It records the time taken for the call and includes usage statistics in the response.

    :param model: The identifier of the LLM to use (e.g., "gpt-4o-mini", "llama-70b").
    :type model: str
    :param messages: A list of message objects to send to the LLM.
    :type messages: list[Message]
    :param system_message: A list of system messages to prepend to the user messages.
                           Defaults to SYSTEM_MESSAGE from constants.
    :type system_message: list, optional
    :param max_tokens: The maximum number of tokens to generate in the response.
                       Defaults to 1500.
    :type max_tokens: int, optional
    :param temperature: The sampling temperature for the LLM. Higher values make the output
                        more random. Defaults to None (model's default).
    :type temperature: float, optional
    :return: A dictionary containing the LLM's response content, role, timestamp,
             time taken, model used, and token usage statistics.
    """
    start = time.time()
    if model.startswith("llama-"):
        messages = [Message(role=m["role"], content=m["content"]) for m in messages]
    answer = get_llm_client(model).chat.completions.create(
        model=model,
        messages=system_message + messages,
        stream=False,
        max_tokens=max_tokens,
        temperature=temperature,
    )
    stop = time.time()
    delta = stop - start
    return {
        "content": answer.choices[0].message.content,
        "role": "assistant",
        "timestamp": str(datetime.fromtimestamp(answer.created)),
        "timedelta_s": delta,
        "model": model,
        "usage": {
            "prompt_tokens": answer.usage.prompt_tokens,
            "completion_tokens": answer.usage.completion_tokens,
        },
    }


@cache
def get_llm_client(model: str) -> OpenAI:
    """Returns an LLM client instance based on the model name.

    This function is cached to avoid reinitializing clients for the same model.
    It supports OpenAI and Groq clients.

    :param model: The identifier of the LLM (e.g., "gpt-4o-mini", "llama-70b").
    :type model: str
    :raises ValueError: If an unsupported model prefix is provided.
    :return: An instance of the OpenAI client configured for the specified model.
    """
    if model.startswith("gpt-"):
        return OpenAI(api_key=OPENAI_API_KEY)
    elif model.startswith("llama-"):
        return OpenAI(base_url="https://api.groq.com/openai/v1", api_key=GROQ_API_KEY)
    else:
        raise ValueError(f"Unexpected model {model}")


def guided_search_queries(
    messages: list[Message],
    llm_model: str = GUIDED_SEARCH_MODEL,
) -> list[dict[str, Any]]:
    """Generates guided search queries based on the latest user message.

    This function formats a prompt using the last message from the provided
    message history and then calls an LLM to generate search query suggestions.

    :param messages: A list of message objects representing the conversation history.
                     The last message is used to generate the queries.
    :type messages: list[Message]
    :param llm_model: The identifier of the LLM to use for generating queries.
                      Defaults to GUIDED_SEARCH_MODEL from constants.
    :type llm_model: str, optional
    :return: The raw content string from the LLM, which is expected to be
             a string representation of a list of query dictionaries.
    """
    formatted_prompt = GUIDED_SEARCH_PROMPT_V2.format(
        message_history=messages[-1]["content"]
    )
    formatted_msg_history = [{"role": "user", "content": formatted_prompt}]

    response = llm_call(model=llm_model, messages=formatted_msg_history, max_tokens=300)
    return eval(response["content"])
