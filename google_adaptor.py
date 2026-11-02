import os
import requests
import json
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
headers = {"Content-Type": "application/json"}

def google_ai(provider, model, query):
    MODEL_ID = model
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
            return response.json()["candidates"][0]["content"]["parts"][0]["text"]
        except requests.exceptions.HTTPError as error:
            status_code = error.response.status_code
            if status_code not in {408, 409, 429} and status_code < 500:
                raise
            if _ == 2:
                raise
        except requests.exceptions.RequestException as e:
            if _ == 2:
                raise e