import json
import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(
  base_url = "https://integrate.api.nvidia.com/v1",
  api_key = os.getenv("DEEPN_API_KEY")
)
def nvidia_ai(provider, model, query):
  completion = client.chat.completions.create(
    model=provider + "/" + model,
    messages=[
        {"role": "user", "content": query}
      ],
    temperature=1,
    top_p=0.95,
    max_tokens=2048,
    stream=False
  )

  return completion.choices[0].message.content or ""