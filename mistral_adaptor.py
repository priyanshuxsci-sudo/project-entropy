import os
from mistralai.client import Mistral

def mistral_ai(model, query):
    client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

    response = client.chat.complete(
        model=model,
        messages=[{"role": "user", "content": query}],
    )

    return response.choices[0].message.content