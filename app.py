import streamlit as st
import time
from crewai import Agent, Task, Crew, LLM
from crewai_tools import TavilySearchTool
from dotenv import load_dotenv
from litellm import RateLimitError
import os

load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")

# ── Page Config ────────────────────────────────────────────────
st.set_page_config(
    page_title="🛒 AI Shopping Agent",
    page_icon="🛒",
    layout="wide"
)

# ── Header ─────────────────────────────────────────────────────
st.title("🛒 Autonomous Shopping Agent")
st.caption("Powered by CrewAI + Groq + Tavily | Built by [Your Name]")
st.divider()

# ── Sidebar ────────────────────────────────────────────────────
with st.sidebar:
    st.header("🤖 Agent Crew")
    st.markdown("""
    | Agent | Role |
    |-------|------|
    | 🔍 Researcher | Finds real products |
    | 🎟️ Deal Hunter | Finds offers & coupons |
    | 📊 Analyst | Scores & ranks |
    | ✍️ Writer | Writes report |
    """)
    st.divider()
    st.header("⚙️ Tech Stack")
    st.markdown("""
    - 🧠 **LLM:** Groq Llama 3.3 70B
    - 🔍 **Search:** Tavily API
    - 🤖 **Agents:** CrewAI
    - 🌐 **UI:** Streamlit
    """)
    st.divider()
    st.caption("💡 Each search takes ~2-3 mins due to free tier limits")

# ── Example Queries ────────────────────────────────────────────
st.subheader("🔎 What are you looking for?")

examples = [
    "Best laptop under ₹80,000 for coding",
    "Gaming laptop under ₹70,000 with RTX GPU",
    "Best phone under ₹30,000 with good camera",
    "Wireless headphones under ₹20,000",
]

# Show example buttons
col1, col2 = st.columns(2)
with col1:
    if st.button(examples[0], use_container_width=True):
        st.session_state.query = examples[0]
    if st.button(examples[2], use_container_width=True):
        st.session_state.query = examples[2]
with col2:
    if st.button(examples[1], use_container_width=True):
        st.session_state.query = examples[1]
    if st.button(examples[3], use_container_width=True):
        st.session_state.query = examples[3]

# ── Search Input ───────────────────────────────────────────────
query = st.text_input(
    "Or type your own query:",
    value=st.session_state.get("query", ""),
    placeholder="e.g. Best laptop under 80000 rupees for coding in India"
)

search_btn = st.button("🚀 Find Best Deals!", type="primary", use_container_width=True)

# ── Run Agents ─────────────────────────────────────────────────
if search_btn and query:

    st.divider()
    st.subheader(f"🔍 Searching for: *{query}*")

    # ── Agent progress tracker ─────────────────────────────────
    st.markdown("### 🤖 Agent Progress")
    col1, col2, col3, col4 = st.columns(4)
    with col1: step1 = st.empty()
    with col2: step2 = st.empty()
    with col3: step3 = st.empty()
    with col4: step4 = st.empty()

    step1.info("⏳ Researcher\nWaiting...")
    step2.info("⏳ Deal Hunter\nWaiting...")
    step3.info("⏳ Analyst\nWaiting...")
    step4.info("⏳ Writer\nWaiting...")

    status_box = st.empty()
    status_box.warning("⏳ Waiting 60 seconds to respect API rate limits...")
    time.sleep(60)

    # ── Build Crew ─────────────────────────────────────────────
    llm = LLM(
        model="groq/llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0.2
    )
    search_tool = TavilySearchTool(api_key=os.getenv("TAVILY_API_KEY"))

    search_agent = Agent(
        role="Product Research Specialist",
        goal=f"Find 3 real products for: {query}",
        backstory="Expert researcher finding real products on Amazon India and Flipkart.",
        llm=llm, tools=[search_tool], verbose=False, max_iter=1
    )
    coupon_agent = Agent(
        role="Deal Hunter",
        goal="Find one bank offer or coupon for each product",
        backstory="Deal hunter finding real discounts on Indian e-commerce sites.",
        llm=llm, tools=[search_tool], verbose=False, max_iter=1
    )
    analyst_agent = Agent(
        role="Product Analyst",
        goal="Score and rank the 3 products out of 100",
        backstory="Data-driven analyst scoring products on value, specs and ratings.",
        llm=llm, verbose=False, max_iter=1
    )
    writer_agent = Agent(
        role="Report Writer",
        goal="Write a clear buying report",
        backstory="Clear writer producing concise buying reports.",
        llm=llm, verbose=False, max_iter=1
    )

    task_search = Task(
        description=f"Search: {query}. Find 3 products with name, price, platform, processor, RAM, storage.",
        expected_output="3 products with name, price in ₹, platform, specs",
        agent=search_agent
    )
    task_coupons = Task(
        description="Find ONE bank offer or coupon per product. Keep it brief.",
        expected_output="One offer per product: platform and discount",
        agent=coupon_agent, context=[task_search]
    )
    task_analyse = Task(
        description="Score each product out of 100 (value 30, specs 25, ratings 20, display 15, build 10). Rank them.",
        expected_output="3 products ranked with score/100 and 1 pro + 1 con each",
        agent=analyst_agent, context=[task_search, task_coupons]
    )
    task_report = Task(
        description="""Write this report:
        ## 🏆 TOP PICK (name, price, score, why)
        ## 📊 TABLE (Rank | Product | Price | Score)
        ## 🎟️ DEALS (all offers found)
        ## 💡 VERDICT (1 sentence)""",
        expected_output="Formatted buying report",
        agent=writer_agent, context=[task_search, task_coupons, task_analyse]
    )

    crew = Crew(
        agents=[search_agent, coupon_agent, analyst_agent, writer_agent],
        tasks=[task_search, task_coupons, task_analyse, task_report],
        verbose=False
    )

    # ── Run with progress updates ──────────────────────────────
    try:
        status_box.info("🔍 Agent 1: Searching for products...")
        step1.success("🔍 Researcher\nRunning...")

        result = crew.kickoff()

        step1.success("✅ Researcher\nDone!")
        step2.success("✅ Deal Hunter\nDone!")
        step3.success("✅ Analyst\nDone!")
        step4.success("✅ Writer\nDone!")
        status_box.success("✅ Report Ready!")

        # ── Show Report ────────────────────────────────────────
        st.divider()
        st.markdown("## 📄 Your Shopping Report")
        st.markdown(str(result))

        # ── Download Button ────────────────────────────────────
        st.download_button(
            label="📥 Download Report",
            data=str(result),
            file_name="shopping_report.md",
            mime="text/markdown",
            use_container_width=True
        )

    except RateLimitError:
        status_box.error("⚠️ Rate limit hit. Please wait 2 minutes and try again.")
    except Exception as e:
        status_box.error(f"❌ Error: {str(e)}")

elif search_btn and not query:
    st.warning("Please enter a search query first!")

# ── Footer ─────────────────────────────────────────────────────
st.divider()
st.caption("Built with ❤️ using CrewAI · Groq · Tavily · Streamlit")