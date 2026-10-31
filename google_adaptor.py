import os
import requests
import json
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
headers = {"Content-Type": "application/json"}

def google_ai(model, query):
    MODEL_ID = model
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={API_KEY}"
    payload = {
        "contents": [
            {
                "parts": [{"text": query}]
            }
        ]
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code== 200:
        return response.json()["candidates"][0]["content"]["parts"][0]["text"] , response.json()["candidates"]["usageMetadata"]["totalTokenCount"]
    else:
        return f"Error: {response.status_code} - {response.text}", None