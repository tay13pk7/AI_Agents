# AI_Agents
Building AI Agents


Autonomous Shopping & Price Comparison Agent

An AI-powered multi-agent system that autonomously searches Amazon India & Flipkart, compares prices, discovers coupon codes, scores products, and generates a ranked buying report — all from a single natural language query.


What It Does ->

User types a query
        │
        ▼
"Best laptop under ₹80,000 for coding in India"
        │
        ▼
┌───────────────────────────────────────────────────────────────┐
│                     AGENT CREW (CrewAI)                       │
│                                                               │
│  ┌─────────────────┐     ┌─────────────────┐                 │
│  │  🔍 RESEARCHER  │────▶│ 🎟️ DEAL HUNTER  │                 │
│  │                 │     │                 │                  │
│  │ Searches Amazon │     │ Finds coupons   │                  │
│  │ & Flipkart for  │     │ & bank offers   │                  │
│  │ real products   │     │ per product     │                  │
│  └─────────────────┘     └────────┬────────┘                 │
│           │                       │                           │
│           └──────────┬────────────┘                          │
│                      ▼                                        │
│           ┌─────────────────┐                                 │
│           │  📊 ANALYST     │                                 │
│           │                 │                                 │
│           │ Scores products │                                 │
│           │ out of 100 and  │                                 │
│           │ ranks them      │                                 │
│           └────────┬────────┘                                 │
│                    │                                          │
│                    ▼                                          │
│           ┌─────────────────┐                                 │
│           │  ✍️ WRITER      │                                 │
│           │                 │                                 │
│           │ Generates final │                                 │
│           │ buying report   │                                 │
│           └────────┬────────┘                                 │
└────────────────────┼──────────────────────────────────────────┘
                     │
                     ▼
         📄 Final Buying Report




🏗️ Full Architecture

┌─────────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                              │
│                                                                     │
│   Streamlit Web UI (app.py)      CLI Terminal (shopping_crew.py)   │
│   ┌──────────────────────┐       ┌──────────────────────┐          │
│   │ • Query input box    │       │ • python main.py     │          │
│   │ • Example buttons    │       │ • Rich terminal UI   │          │
│   │ • Agent progress     │       │ • Auto saves report  │          │
│   │ • Download report    │       └──────────────────────┘          │
│   └──────────┬───────────┘                                         │
└──────────────┼──────────────────────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      ORCHESTRATION LAYER                            │
│                         CrewAI v1.14.4                              │
│                                                                     │
│   crew.kickoff()  ──▶  Sequential Task Execution                   │
│                        Task 1 ──▶ Task 2 ──▶ Task 3 ──▶ Task 4    │
└─────────────────────────────────────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         AGENT LAYER                                 │
│                                                                     │
│  Agent 1              Agent 2              Agent 3      Agent 4    │
│  ┌──────────┐         ┌──────────┐         ┌────────┐  ┌────────┐  │
│  │🔍 Product│         │🎟️ Deal   │         │📊      │  │✍️      │  │
│  │Research  │         │Hunter    │         │Analyst │  │Writer  │  │
│  │          │         │          │         │        │  │        │  │
│  │Tools:    │         │Tools:    │         │No tool │  │No tool │  │
│  │Tavily ✓  │         │Tavily ✓  │         │        │  │        │  │
│  │max_iter=1│         │max_iter=1│         │max_iter│  │max_iter│  │
│  └──────────┘         └──────────┘         │=1      │  │=1      │  │
│                                            └────────┘  └────────┘  │
└─────────────────────────────────────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                          LLM LAYER                                  │
│                                                                     │
│              Groq API ──▶ Llama 3.3 70B Versatile                  │
│              • 280 tokens/second (ultra fast)                       │
│              • Free tier: 14,400 requests/day                       │
│              • Temperature: 0.2 (focused, deterministic)           │
│              • Connected via LiteLLM bridge                         │
└─────────────────────────────────────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         SEARCH LAYER                                │
│                                                                     │
│              Tavily Search API                                      │
│              • Real-time web search                                 │
│              • Searches Amazon.in + Flipkart + review sites        │
│              • Returns structured JSON with URLs and content        │
│              • Free tier: 1,000 searches/month                      │
└─────────────────────────────────────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         OUTPUT LAYER                                │
│                                                                     │
│   Streamlit UI          Markdown File         Terminal              │
│   (rendered report)     (saved to disk)       (rich output)         │
└─────────────────────────────────────────────────────────────────────┘


🤖 Agent Details
Agent 1 — 🔍 Product Research Specialist
PropertyValueGoalFind 3 real products with live prices from Amazon India / FlipkartToolTavily Search APILLMGroq Llama 3.3 70BMax Iterations1OutputProduct name, price in ₹, platform, processor, RAM, storage
Agent 2 — 🎟️ Deal Hunter
PropertyValueGoalFind one active bank offer or coupon per productToolTavily Search APILLMGroq Llama 3.3 70BMax Iterations1OutputPlatform, offer description, discount amount
Agent 3 — 📊 Product Analyst
PropertyValueGoalScore and rank products out of 100ToolNone (reasoning only)LLMGroq Llama 3.3 70BMax Iterations1ScoringValue 30pts + Specs 25pts + Ratings 20pts + Display 15pts + Build 10ptsOutputRanked list with scores, pros, cons
Agent 4 — ✍️ Report Writer
PropertyValueGoalWrite a clean formatted buying reportToolNone (writing only)LLMGroq Llama 3.3 70BMax Iterations1OutputTop pick, comparison table, deals, verdict


🔄 Data Flow

Query: "Best laptop under ₹80,000 for coding"
  │
  ▼
[Task 1 - Search]
  Tavily searches → Amazon.in, Flipkart, Smartprix, 91Mobiles
  Returns → 3 products with real prices and specs
  │
  ▼
[Task 2 - Coupons]         ← receives Task 1 output as context
  Tavily searches → HDFC offers, SBI cashback, Axis discounts
  Returns → 1 offer per product
  │
  ▼
[Task 3 - Analysis]        ← receives Task 1 + Task 2 as context
  LLM reasons → scores each product across 5 dimensions
  Returns → ranked list with scores out of 100
  │
  ▼
[Task 4 - Report]          ← receives Task 1 + 2 + 3 as context
  LLM writes → formatted markdown report
  Returns → 🏆 Top Pick + 📊 Table + 🎟️ Deals + 💡 Verdict
  │
  ▼
Output displayed in Streamlit UI / Terminal



🛠️ Tech Stack
<img width="677" height="367" alt="image" src="https://github.com/user-attachments/assets/0f90666e-e96f-40c3-ad94-8f9394488534" />


🚀 Quick Start
Prerequisites

Python 3.10+
PyCharm (or any IDE)

Step 1 — Clone the repo
bashgit clone https://github.com/yourusername/AI-Shopping-Agent
cd AI-Shopping-Agent
Step 2 — Create virtual environment
bashpython -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
Step 3 — Install dependencies
bashpip install crewai crewai-tools litellm streamlit python-dotenv tavily-python
Step 4 — Set up API keys
Create a .env file:
GROQ_API_KEY=your_groq_key_here
TAVILY_API_KEY=your_tavily_key_here
Get your FREE API keys:
KeyLinkCostGROQ_API_KEYconsole.groq.comFree tier — 14,400 req/dayTAVILY_API_KEYtavily.comFree tier — 1,000 searches/month
Step 5 — Run
Option A — Streamlit UI (recommended for demo)
bashstreamlit run app.py
Option B — Terminal CLI
bashpython shopping_crew.py

💡 Example Queries
"Best laptop under ₹80,000 for coding in India"
"Gaming laptop under ₹70,000 with RTX GPU"
"Best phone under ₹30,000 with good camera"
"Wireless noise-cancelling headphones under ₹20,000"
"Best tablet under ₹50,000 for students"



⚙️ Scoring Methodology
Total Score = Sum of all dimension scores (max 100)

┌─────────────────────┬────────┬─────────────────────────────────┐
│ Dimension           │ Weight │ What it measures                │
├─────────────────────┼────────┼─────────────────────────────────┤
│ Value for Money     │  30%   │ Price vs budget ratio           │
│ Specifications      │  25%   │ Processor + RAM + Storage tier  │
│ User Ratings        │  20%   │ Star rating + review count      │
│ Display Quality     │  15%   │ Size, resolution, panel type    │
│ Build Quality       │  10%   │ Weight + warranty years         │
└─────────────────────┴────────┴─────────────────────────────────┘


🔑 Key Concepts Demonstrated

✅ Multi-Agent Orchestration   — 4 agents with distinct roles
✅ Tool Use                    — agents calling Tavily API
✅ Sequential Task Pipeline    — output of each task feeds next
✅ Context Passing             — agents share information
✅ Real-time Web Search        — live data, not static knowledge
✅ Structured Output           — clean markdown reports
✅ Rate Limit Handling         — retry logic for free tier APIs
✅ Secure Config               — .env + .gitignore pattern
✅ Production UI               — Streamlit web interface

🧑‍💻 Author
Built by Prasad Kute

💼 Software Engineer
🔗 LinkedIn: https://www.linkedin.com/in/prasad-kute-7b0169222/

📄 License
MIT License — feel free to use, modify and share.

⭐ If this project helped you, give it a star!

"This project was built from scratch — step by step — as a portfolio project demonstrating real-world AI agent engineering with multi-agent orchestration, tool use, and live web search."

         
