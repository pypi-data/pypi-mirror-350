import os
from typing import Optional
from wujing.llm.provider.litellm_wrapper import send_req as litellm_call
from wujing.llm.provider.oai_wrapper import send_req as oai_call
from typing import Optional, Dict, Any
import functools


def llm_call(
    *,
    api_key: Optional[str] = None,
    api_base: Optional[str] = None,
    model: str,
    messages: list,
    cache_enabled: bool = True,
    cache_directory: str = "./.diskcache/oai_cache",
    provider: str = "oai",  # Moved from kwargs to explicit parameter
    debug: bool = False,
    **kwargs: Dict[str, Any],
) -> str:
    """
    Make an LLM API call using the specified provider.

    Args:
        api_key: API key for authentication
        api_base: Base URL for the API
        model: Model identifier to use
        messages: List of messages for the conversation
        cache_enabled: Whether to enable response caching
        cache_directory: Directory to store cached responses
        provider: Which provider to use ('oai' or 'litellm')
        **kwargs: Additional provider-specific arguments

    Returns:
        The generated response as a string
    """
    # Map provider names to their corresponding call functions
    provider_functions = {
        "oai": oai_call,
        "litellm": litellm_call,
    }

    if provider not in provider_functions:
        raise ValueError(f"Unsupported provider: {provider}. Supported providers are: {list(provider_functions.keys())}")

    # Create a partial function with common arguments
    call_function = functools.partial(
        provider_functions[provider],
        api_key=api_key,
        api_base=api_base,
        model=model,
        messages=messages,
        cache_enabled=cache_enabled,
        cache_directory=cache_directory,
        debug=debug,
    )

    return call_function(**kwargs)


to_llm = llm_call


if __name__ == "__main__":
    result = to_llm(
        model=os.getenv("model"),
        messages=[
            {
                "role": "user",
                "content": "1+1=?",
            },
        ],
        max_tokens=8 * 1024,
        api_key=os.getenv("api_key"),
        api_base=os.getenv("api_base"),
        provider="litellm",
        debug=1,
        cache_enabled=False,
    )
    print(f"result:{result}")
