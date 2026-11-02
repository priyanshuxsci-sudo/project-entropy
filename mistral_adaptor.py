import os
from mistralai.client import Mistral

def mistral_ai(provider, model, query):
    client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))
    for attempt in range(3):
        try:
            response = client.chat.complete(
                model=model,
                messages=[{"role": "user", "content": query}],
            )
            usage = response.usage
            return response.choices[0].message.content, {
                "prompt_tokens": usage.prompt_tokens,
                "completion_tokens": usage.completion_tokens,
                "total_tokens": usage.total_tokens,
            }
        except Exception as e:
            if attempt == 2:
                raise e