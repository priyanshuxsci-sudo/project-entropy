from router import Router


payload = {
  "model": "mistral/ministral-3b-2512",
  "messages": [{"role": "user", "content": "You can tell me about the latest research on quantum computing?"}],
  "fallbacks": ["nvidia/nemotron-3.5-lightning-30b-a3b"],
  "grounding": "auto"
}

output = Router(payload["model"], payload["messages"][0]["content"], payload["grounding"], payload["fallbacks"])
print(output.output)



