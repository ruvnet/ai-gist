import os
from litellm import completion

async def chat_completion(messages):
    response = completion(
        model=os.getenv("LITELLM_MODEL", "gpt-4o"),  # Default to "gpt-4o-2024-05-1" if not set
        messages=messages,
        api_base=os.getenv("LITELLM_API_BASE"),
        api_key=os.getenv("LITELLM_API_KEY"),
        stream=False
    )
    return response
