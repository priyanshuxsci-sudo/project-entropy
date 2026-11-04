import os
from mistralai.client import Mistral

INSTRUCTIONS = """You'll be provided with a query. You have to analyse that wether the query need search grounding or not.
If yes then output the query in the following format:
{ "query": "<query>", "search_grounding": true } 

EXAMPLE 1:
input: 'What is the capital of France?'
output: { "query": "What is the capital of France?", "search_grounding": False }

Because the answer to this question is well known and does not require any search grounding.

EXAMPLE 2:
input: 'What is the latest research on quantum computing?'
output: { "query": "What is the latest research on quantum computing?", "search_grounding": True }

Because the answer to this question may require up-to-date information and search grounding to provide an accurate response.

EXAMPLE 3:
input: 'Who won the 2023 FIFA World Cup?'
output: { "query": "Who won the 2023 FIFA World Cup?", "search_grounding": False }

Because the answer to this question is well known and does not require any search grounding. Like the user is asking question of Previous Years. Not Latest. (Current Year is 2026)
"""

def auto_caller(query):
    client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))
    for attempt in range(3):
        try:
            response = client.chat.complete(
                model="ministral-8b-2512",
                messages=[
                    {"role": "system", "content": INSTRUCTIONS},
                    {"role": "user", "content": query}],
            )

            
            return response.choices[0].message.content
            
        except Exception as e:
            if attempt == 2:
                raise e