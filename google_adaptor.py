import os
import requests
import json

API_KEY = os.environ.get("GEMINI_API_KEY")
headers = {"Content-Type": "application/json"}

def google_ai(model, query):
    MODEL_ID = model
    url = f"https://googleapis.com{MODEL_ID}:generateContent?key={API_KEY}"
    payload = {
        "contents": [
            {
                "parts": [{"text": query}]
            }
        ]
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code== 200:
        return response.json()["candidates"][0]["contents"]["parts"][0]["text"] , response.json()["candidates"]["usageMetadata"]["totalTokenCount"]
