import os
import litellm
from litellm.caching.caching import Cache
from typing import Optional, Dict, Any, List

_cache: Optional[Cache] = None

litellm.suppress_debug_info = True


def send_req(
    *,
    api_key: str,
    api_base: str,
    model: str,
    messages: List[Dict[str, str]],
    cache_enabled: bool = True,
    cache_directory: str = "./.diskcache/litellm_cache",
    debug: bool = False,
    **kwargs: Any,
) -> Dict[str, Any]:
    """Send a request to the LLM API with optional caching.

    Args:
        api_key: API key for authentication
        api_base: Base URL for the API
        model: Model name to use
        messages: List of message dictionaries with role and content
        cache_enabled: Whether to enable caching
        cache_directory: Directory for disk cache
        debug: Enable debug logging
        **kwargs: Additional arguments to pass to litellm.completion

    Returns:
        The chat response from the API
    """
    global _cache

    if cache_enabled and _cache is None:
        _cache = Cache(type="disk", disk_cache_dir=cache_directory)
        litellm.cache = _cache

    if debug:
        litellm._turn_on_debug()

    chat_response = litellm.completion(
        model=f"openai/{model}",
        api_key=api_key,
        api_base=api_base,
        messages=messages,
        **kwargs,
    )

    return chat_response


if __name__ == "__main__":
    result = send_req(
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
    )
    print(f"result:{result}")
