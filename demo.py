from router import Router


payload = {
  "model": "nvidia/nemotron-3-ultra-550b-a55b",
  "messages": [{"role": "user", "content": "What's the price of Bitcoin Right now?"}],
  "fallbacks": ["google/gemini-3.6-flash"],
  "grounding": "auto"
}

output = Router(payload["model"], payload["messages"][0]["content"], payload["grounding"], payload["fallbacks"])
print(output.output)



