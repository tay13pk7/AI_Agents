from crewai import Agent, Task, Crew, LLM
from crewai_tools import TavilySearchTool
from dotenv import load_dotenv
import os

load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")

# ── 1. LLM ─────────────────────────────────────────────────────
llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.2
)

# ── 2. Tool ────────────────────────────────────────────────────
search_tool = TavilySearchTool(api_key=os.getenv("TAVILY_API_KEY"))

# ── 3. Agent ───────────────────────────────────────────────────
shopping_agent = Agent(
    role="Shopping Expert",
    goal="Find the best laptops within budget by searching the internet",
    backstory="""You are an expert shopping assistant who searches 
    Amazon India and Flipkart to find real current prices and specs. 
    You always search before answering — never guess prices.""",
    llm=llm,
    tools=[search_tool],
    verbose=True,
    max_iter=3
)

# ── 4. Task ────────────────────────────────────────────────────
task = Task(
    description="""Search the internet and find the top 3 laptops 
    under 80000 rupees for coding in India right now.
    Find real current prices from Amazon India or Flipkart.""",
    expected_output="""A list of 3 laptops with:
    - Real product name
    - Current price in rupees
    - Where to buy (Amazon/Flipkart)
    - Key specs (processor, RAM, storage)""",
    agent=shopping_agent
)

# ── 5. Crew ────────────────────────────────────────────────────
crew = Crew(
    agents=[shopping_agent],
    tasks=[task],
    verbose=True
)

# ── 6. Run ─────────────────────────────────────────────────────
result = crew.kickoff()
print("\n====== FINAL RESULT ======")
print(result)