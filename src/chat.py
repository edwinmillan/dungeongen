import json
from os import getenv

import httpx
from dotenv import load_dotenv

from src.schema.openrouter_model import Response

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
            if response.status_code in range(200, 299):
                chat_response = Response(**response.json())
                return chat_response.choices[0].message.content
            else:
                return {}
    except httpx.HTTPError as e:
        print(f"Error: {e}")
        return {}
