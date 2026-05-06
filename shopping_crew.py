from crewai import Agent, Task, Crew, LLM
from crewai_tools import TavilySearchTool
from dotenv import load_dotenv
import os
import time
from litellm import RateLimitError

load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")

# ── Single LLM for all agents ──────────────────────────────────
llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.2
)

# ── Tool ───────────────────────────────────────────────────────
search_tool = TavilySearchTool(api_key=os.getenv("TAVILY_API_KEY"))

# ══════════════════════════════════════════════════════════════
# 4 AGENTS — all use same LLM, max_iter=1 to save tokens
# ══════════════════════════════════════════════════════════════

search_agent = Agent(
    role="Product Research Specialist",
    goal="Search for 3 real laptops under 80000 rupees in India with prices",
    backstory="Expert researcher who finds real products on Amazon India and Flipkart.",
    llm=llm,
    tools=[search_tool],
    verbose=True,
    max_iter=1        # ← only 1 search, saves tokens
)

coupon_agent = Agent(
    role="Deal Hunter",
    goal="Find one bank offer or coupon for each laptop found",
    backstory="Deal hunter who finds real discounts on Indian e-commerce sites.",
    llm=llm,
    tools=[search_tool],
    verbose=True,
    max_iter=1        # ← only 1 search, saves tokens
)

analyst_agent = Agent(
    role="Product Analyst",
    goal="Score and rank the 3 laptops out of 100",
    backstory="Data-driven analyst who scores laptops on value, specs and ratings.",
    llm=llm,
    verbose=True,
    max_iter=1
)

writer_agent = Agent(
    role="Report Writer",
    goal="Write a short buying report with winner, table and verdict",
    backstory="Clear writer who produces concise buying reports.",
    llm=llm,
    verbose=True,
    max_iter=1
)

# ══════════════════════════════════════════════════════════════
# 4 TASKS — kept very short to save tokens
# ══════════════════════════════════════════════════════════════

user_query = "best laptop under 80000 rupees for coding in India"

task_search = Task(
    description=f"Search: {user_query}. Find exactly 3 laptops with name, price, platform, processor, RAM, storage.",
    expected_output="3 laptops with name, price in ₹, platform, processor, RAM, storage",
    agent=search_agent
)

task_coupons = Task(
    description="Search for ONE bank offer or coupon for each of the 3 laptops found. Keep it brief.",
    expected_output="One offer per laptop: platform and discount amount",
    agent=coupon_agent,
    context=[task_search]
)

task_analyse = Task(
    description="Score each laptop out of 100 (value 30pts, specs 25pts, ratings 20pts, display 15pts, build 10pts). Rank them.",
    expected_output="3 laptops ranked with score/100 and 1 pro + 1 con each",
    agent=analyst_agent,
    context=[task_search, task_coupons]
)

task_report = Task(
    description="""Write this report:
    ## 🏆 TOP PICK (name, price, score, why)
    ## 📊 TABLE (Rank | Laptop | Price | Score)
    ## 🎟️ DEALS (offers found)
    ## 💡 VERDICT (1 sentence)""",
    expected_output="Short formatted buying report",
    agent=writer_agent,
    context=[task_search, task_coupons, task_analyse]
)

# ══════════════════════════════════════════════════════════════
# CREW with auto-retry on rate limit
# ══════════════════════════════════════════════════════════════

crew = Crew(
    agents=[search_agent, coupon_agent, analyst_agent, writer_agent],
    tasks=[task_search, task_coupons, task_analyse, task_report],
    verbose=True
)

print("\n🛒 Starting Shopping Agent Crew...")
print("⏳ Waiting 60 seconds to reset rate limits...\n")
time.sleep(60)

# ── Run with retry ─────────────────────────────────────────────
max_retries = 3
for attempt in range(max_retries):
    try:
        result = crew.kickoff()
        print("\n" + "="*60)
        print("📄 FINAL SHOPPING REPORT")
        print("="*60)
        print(result)
        break
    except RateLimitError as e:
        wait = 60
        print(f"\n⚠️  Rate limit hit (attempt {attempt+1}/{max_retries})")
        print(f"⏳ Waiting {wait} seconds before retry...\n")
        time.sleep(wait)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        break