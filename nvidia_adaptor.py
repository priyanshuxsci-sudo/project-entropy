import os
from openai import APIConnectionError, APIStatusError, OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(
  base_url = "https://integrate.api.nvidia.com/v1",
  api_key = os.getenv("NVIDIA_API_KEY"),
  max_retries = 0
)
def nvidia_ai(provider, model, query):
  for attempt in range(3):
    try:
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
    except APIConnectionError:
      if attempt == 2:
        raise
    except APIStatusError as error:
      if error.status_code not in {408, 409, 429} and error.status_code < 500:
        raise
      if attempt == 2:
        raise