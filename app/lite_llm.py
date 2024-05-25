import os
from litellm import completion

async def chat_completion(messages):
    response = await completion(
        model="gpt-4o",
        messages=messages,
        api_base=os.getenv("LITELLM_API_BASE"),
        api_key=os.getenv("LITELLM_API_KEY"),
        stream=False
    )
    return response
