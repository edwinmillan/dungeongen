import requests
import json
from dotenv import load_dotenv
from yarl import URL
from os import getenv
from schema.openrouter_model import Response

load_dotenv()


def send_prompt(prompt: str) -> str:
    url = URL("https://openrouter.ai/api/v1/chat/completions")

    headers = {
        "Authorization": f"Bearer {getenv('OPENROUTER_API_KEY')}",
    }
    data = json.dumps(
        {"model": "openrouter/auto", "messages": [{"role": "user", "content": prompt}]}
    )

    try:
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
        chat_response = Response(**response.json())

    except requests.exceptions.HTTPError as e:
        print(f"Error: {e}")
        return {}
    return chat_response.choices[0].message.content


if __name__ == "__main__":
    prompt = "What is the meaning of life?"
    response = send_prompt(prompt)
    print(response)
