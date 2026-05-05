from crewai import Agent, Task, Crew
from dotenv import load_dotenv
import os

load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

# ── 1. Agent ───────────────────────────────────────────────────
shopping_agent = Agent(
    role="Shopping Expert",
    goal="Help users find the best laptop within their budget in India",
    backstory="""You are an expert shopping assistant with deep knowledge 
    of Indian e-commerce platforms like Amazon and Flipkart. 
    You help users find the best products within their budget.""",
    llm="groq/llama-3.3-70b-versatile",
    verbose=True
)

# ── 2. Task ────────────────────────────────────────────────────
task = Task(
    description="What are the top 3 laptops under 80000 rupees for coding in India?",
    expected_output="A list of 3 laptops with name, price and key specs",
    agent=shopping_agent
)

# ── 3. Crew ────────────────────────────────────────────────────
crew = Crew(
    agents=[shopping_agent],
    tasks=[task],
    verbose=True
)

# ── 4. Run ─────────────────────────────────────────────────────
result = crew.kickoff()
print("\n====== FINAL RESULT ======")
print(result)