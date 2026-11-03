import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

INSTRUCTIONS = (
    "In some cases, context will be provided to help answer the user's query. "
    "If context is provided, use it to answer the query. If no context is "
    "provided, answer based on your own knowledge. Do not output the context "
    "verbatim; use your own words."
)


def google_ai(provider, model, query):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is not set. Add it to the environment or .env file."
        )
    for _ in range(2):
        try:
            client = genai.Client(api_key=api_key)

            interaction = client.interactions.create(
                model=model,
                input=f"{INSTRUCTIONS}\n\nUser query:\n{query}",
            )

            print(interaction.output_text)
            usage = interaction.usage
            return interaction.output_text, {
                "prompt_token": usage.total_input_tokens,
                "output_token": usage.total_output_tokens,
                "total_token": usage.total_tokens,
            }
        except Exception as e:
            print(f"Error occurred: {e}. (ENTROPY) Retrying...")