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
            return response.choices[0].message.content
        except Exception as e:
            if attempt == 2:
                raise e