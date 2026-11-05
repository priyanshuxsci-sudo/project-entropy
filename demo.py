from router import Router


payload = {
  "model": "google/gemini-3.6-flash",
  "messages": [{"role": "user", "content": "You can tell me about the latest research on quantum computing?"}],
  "fallbacks": ["mistral/ministral-3b-2512"],
  "grounding": "auto"
}

output = Router(payload["model"], payload["messages"][0]["content"], payload["grounding"], payload["fallbacks"])
print(output.output)



