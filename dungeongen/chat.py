import httpx
import json
from dotenv import load_dotenv
from os import getenv
from schema.openrouter_model import Response

load_dotenv()


async def send_prompt(prompt: str) -> str:
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {getenv('OPENROUTER_API_KEY')}",
    }
    data = json.dumps(
        {"model": "openrouter/auto", "messages": [{"role": "user", "content": prompt}]}
    )

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, data=data)
            response.raise_for_status()
            chat_response = Response(**response.json())
    except httpx.HTTPError as e:
        print(f"Error: {e}")
        return {}
    return chat_response.choices[0].message.content


if __name__ == "__main__":
    import asyncio

    prompt = "What is the meaning of life?"
    response = asyncio.run(send_prompt(prompt))
    print(response)
