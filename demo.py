import json
import requests
from router import Router


payload = {
  "model": "google/gemini-3.7-flash-lite",
  "messages": [{"role": "user", "content": "Tell me a joke."}],
  "fallbacks": ["mistral/ministral-3b-2512"],
  "grounding": "off"
}

output = Router(payload["model"], payload["messages"][0]["content"], payload["fallbacks"])
print(output.output)



