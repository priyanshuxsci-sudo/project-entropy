from tavily import TavilyClient
import os
from dotenv import load_dotenv
load_dotenv()

def tavily_search(query):
    tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    response = tavily_client.search(
        query,
        max_results=2
    )

    context = ""
    for i, r in enumerate(response["results"], start=1):
        context += f"[{i}] {r['title']} ({r['url']})\n{r['content'][:500]}\n\n"

    return context