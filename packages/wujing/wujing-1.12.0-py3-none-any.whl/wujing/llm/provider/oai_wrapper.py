from openai import OpenAI
from diskcache import FanoutCache as Cache
import os

cache = None


def oai_call(
    *,
    api_key,
    api_base,
    model,
    messages,
    **kwargs,
):
    try:
        client = OpenAI(
            api_key=api_key,
            base_url=api_base,
        )
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            **kwargs,
        )
        return response

    except Exception as e:
        raise RuntimeError(f"Failed to send request: {e}") from e


def send_req(
    *,
    api_key,
    api_base,
    model,
    messages,
    cache_enabled: bool = True,
    cache_directory: str = "./.diskcache/litellm_cache",
    debug: bool = False,
    **kwargs,
):
    global cache

    if cache_enabled and cache is None:
        cache = Cache(directory=cache_directory)

    if cache_enabled:
        cached_send_req = cache.memoize(typed=True)(oai_call)
        chat_response = cached_send_req(
            model=model,
            messages=messages,
            api_key=api_key,
            api_base=api_base,
            **kwargs,
        )
    else:
        chat_response = oai_call(
            model=model,
            messages=messages,
            api_key=api_key,
            api_base=api_base,
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
