# AI_Agents

Building AI Agents

---

# 🛒 Autonomous Shopping & Price Comparison Agent

An AI-powered multi-agent system that autonomously searches Amazon India & Flipkart, compares prices, discovers coupon codes, scores products, and generates a ranked buying report — all from a single natural language query.

---

# 🚀 What It Does

```text
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
│  │  🔍 RESEARCHER  │────▶│ 🎟️ DEAL HUNTER │                 │
│  │                 │     │                 │                 │
│  │ Searches Amazon │     │ Finds coupons   │                 │
│  │ & Flipkart for  │     │ & bank offers   │                 │
│  │ real products   │     │ per product     │                 │
│  └─────────────────┘     └────────┬────────┘                 │
│           │                       │                           │
│           └──────────┬────────────┘                           │
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
```

---

# 🏗️ Full Architecture

```text
┌─────────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                              │
│                                                                     │
│   Streamlit Web UI (app.py)      CLI Terminal (shopping_crew.py)   │
│   ┌──────────────────────┐       ┌──────────────────────┐           │
│   │ • Query input box    │       │ • python main.py     │           │
│   │ • Example buttons    │       │ • Rich terminal UI   │           │
│   │ • Agent progress     │       │ • Auto saves report  │           │
│   │ • Download report    │       └──────────────────────┘           │
│   └──────────┬───────────┘                                           │
└──────────────┼──────────────────────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      ORCHESTRATION LAYER                            │
│                         CrewAI v1.14.4                              │
│                                                                     │
│   crew.kickoff()  ──▶  Sequential Task Execution                    │
│                        Task 1 ──▶ Task 2 ──▶ Task 3 ──▶ Task 4      │
└─────────────────────────────────────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         AGENT LAYER                                 │
│                                                                     │
│  Agent 1              Agent 2              Agent 3      Agent 4     │
│  ┌──────────┐         ┌──────────┐         ┌────────┐  ┌────────┐   │
│  │🔍 Product│         │🎟️ Deal   │         │📊      │  │✍️      │   │
│  │Research  │         │Hunter    │         │Analyst │  │Writer  │   │
│  │          │         │          │         │        │  │        │   │
│  │Tools:    │         │Tools:    │         │No tool │  │No tool │   │
│  │Tavily ✓  │         │Tavily ✓  │         │        │  │        │   │
│  │max_iter=1│         │max_iter=1│         │=1      │  │=1      │   │
│  └──────────┘         └──────────┘         └────────┘  └────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

---

# 🤖 Agent Details

## Agent 1 — 🔍 Product Research Specialist

| Property | Value |
|---|---|
| Goal | Find 3 real products with live prices from Amazon India / Flipkart |
| Tool | Tavily Search API |
| LLM | Groq Llama 3.3 70B |
| Max Iterations | 1 |
| Output | Product name, price in ₹, platform, processor, RAM, storage |

---

## Agent 2 — 🎟️ Deal Hunter

| Property | Value |
|---|---|
| Goal | Find one active bank offer or coupon per product |
| Tool | Tavily Search API |
| LLM | Groq Llama 3.3 70B |
| Max Iterations | 1 |
| Output | Platform, offer description, discount amount |

---

## Agent 3 — 📊 Product Analyst

| Property | Value |
|---|---|
| Goal | Score and rank products out of 100 |
| Tool | None (reasoning only) |
| LLM | Groq Llama 3.3 70B |
| Max Iterations | 1 |
| Scoring | Value 30pts + Specs 25pts + Ratings 20pts + Display 15pts + Build 10pts |
| Output | Ranked list with scores, pros, cons |

---

## Agent 4 — ✍️ Report Writer

| Property | Value |
|---|---|
| Goal | Write a clean formatted buying report |
| Tool | None (writing only) |
| LLM | Groq Llama 3.3 70B |
| Max Iterations | 1 |
| Output | Top pick, comparison table, deals, verdict |

---

# 🔄 Data Flow

```text
Query: "Best laptop under ₹80,000 for coding"
  │
  ▼
[Task 1 - Search]
  Tavily searches → Amazon.in, Flipkart, Smartprix, 91Mobiles
  Returns → 3 products with real prices and specs
  │
  ▼
[Task 2 - Coupons]
  Tavily searches → HDFC offers, SBI cashback, Axis discounts
  Returns → 1 offer per product
  │
  ▼
[Task 3 - Analysis]
  LLM reasons → scores each product across 5 dimensions
  Returns → ranked list with scores out of 100
  │
  ▼
[Task 4 - Report]
  LLM writes → formatted markdown report
  Returns → 🏆 Top Pick + 📊 Table + 🎟️ Deals + 💡 Verdict
```

---

# 🛠️ Tech Stack

- CrewAI
- Groq API
- Llama 3.3 70B
- Tavily Search API
- Streamlit
- Python
- LiteLLM

---

# 🚀 Quick Start

## Prerequisites

- Python 3.10+
- PyCharm (or any IDE)

---

## Step 1 — Clone the repo

```bash
git clone https://github.com/yourusername/AI-Shopping-Agent
cd AI-Shopping-Agent
```

---

## Step 2 — Create virtual environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Mac/Linux

```bash
source venv/bin/activate
```

---

## Step 3 — Install dependencies

```bash
pip install crewai crewai-tools litellm streamlit python-dotenv tavily-python
```

---

## Step 4 — Set up API keys

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_key_here
TAVILY_API_KEY=your_tavily_key_here
```

### Get your FREE API keys

| Key | Link | Cost |
|---|---|---|
| GROQ_API_KEY | console.groq.com | Free tier — 14,400 req/day |
| TAVILY_API_KEY | tavily.com | Free tier — 1,000 searches/month |

---

## Step 5 — Run

### Option A — Streamlit UI

```bash
streamlit run app.py
```

### Option B — Terminal CLI

```bash
python shopping_crew.py
```

---

# 💡 Example Queries

- "Best laptop under ₹80,000 for coding in India"
- "Gaming laptop under ₹70,000 with RTX GPU"
- "Best phone under ₹30,000 with good camera"
- "Wireless noise-cancelling headphones under ₹20,000"
- "Best tablet under ₹50,000 for students"

---

# ⚙️ Scoring Methodology

| Dimension | Weight | What it measures |
|---|---|---|
| Value for Money | 30% | Price vs budget ratio |
| Specifications | 25% | Processor + RAM + Storage tier |
| User Ratings | 20% | Star rating + review count |
| Display Quality | 15% | Size, resolution, panel type |
| Build Quality | 10% | Weight + warranty years |

---

# 🔑 Key Concepts Demonstrated

- ✅ Multi-Agent Orchestration
- ✅ Tool Use
- ✅ Sequential Task Pipeline
- ✅ Context Passing
- ✅ Real-time Web Search
- ✅ Structured Output
- ✅ Rate Limit Handling
- ✅ Secure Config
- ✅ Production UI

---

# 🧑‍💻 Author

Built by Prasad Kute

💼 Software Engineer

🔗 LinkedIn: https://www.linkedin.com/in/prasad-kute-7b0169222/

---

# 📄 License

MIT License — feel free to use, modify and share.

---

⭐ If this project helped you, give it a star!

> "This project was built from scratch — step by step — as a portfolio project demonstrating real-world AI agent engineering with multi-agent orchestration, tool use, and live web search."
