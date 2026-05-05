from tavily import TavilyClient
from dotenv import load_dotenv
import os

load_dotenv()

client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

results = client.search(
    query="best laptop under 80000 rupees for coding in India 2025",
    max_results=3
)

for r in results["results"]:
    print("Title:", r["title"])
    print("URL  :", r["url"])
    print("Info :", r["content"][:200])
    print("---")