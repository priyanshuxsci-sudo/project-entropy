import os
import requests
import json
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
headers = {"Content-Type": "application/json"}

def google_ai(provider, model, query):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={API_KEY}"
    payload = {
        "contents": [
            {
                "parts": [{"text": query}]
            }
        ]
    }
    for _ in range(3):
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            usage = data.get("usageMetadata", {})
            return data["candidates"][0]["content"]["parts"][0]["text"], {
                "prompt_tokens": usage.get("promptTokenCount", 0),
                "completion_tokens": usage.get("candidatesTokenCount", 0),
                "total_tokens": usage.get("totalTokenCount", 0),
            }
        except requests.exceptions.HTTPError as error:
            status_code = error.response.status_code
            if status_code not in {408, 409, 429} and status_code < 500:
                raise
            if _ == 2:
                raise
        except requests.exceptions.RequestException as e:
            if _ == 2:
                raise e