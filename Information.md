# AI_Agents
Building AI Agents



Limit 12,000 tokens/min — you used 6,112 + requested 11,285 = too many!

use the smaller faster model for agents that don't need heavy reasoning, and add a delay between agents.


The free tier limits are very tight for a 4-agent crew. 
I had solved this properly by adding automatic retry with wait so it handles rate limits gracefully.


Only add these lines at the top, and change time.sleep(30) to time.sleep(60):


✅ max_iter=1      → each agent does only 1 action (saves tokens)
✅ Shorter tasks   → less tokens per LLM call
✅ sleep(60)       → full minute wait before starting
✅ auto-retry      → if rate limit hits, waits 60s and retries


✅ Agent 1 — Product Research Specialist → Found 3 real laptops
✅ Agent 2 — Deal Hunter → Found bank offers for each
✅ Agent 3 — Product Analyst → Scored & ranked all 3
✅ Agent 4 — Report Writer → Generated final buying report


The 4 parts of every Agent definition
search_agent = Agent(
  role="Product Research Specialist",   # WHO the agent is
  goal="Find 3 real products...",       # WHAT it must achieve
  backstory="You are an expert...",     # HOW it should behave / its personality
  llm=llm,                              # BRAIN (Groq Llama 3.3)
  tools=[search_tool],                  # HANDS (what it can do)
  verbose=True,                         # show thinking in terminal
  max_iter=1                            # max times it can loop
)

---------------------------------------------------------------------------------



What is max_iter?
max_iter limits how many times an agent can loop (Thought → Action → Observation). We set it to 1 to save API tokens on the free tier. 
In production you'd set it to 3-5 to let agents search multiple times if needed.

max_iter	         Behaviour	                                     Token cost
1	               One search, then answer	                    Low — good for free tier
3	               Can search 3 times, pick best result	             Medium
5+	               Deep research, multiple angles	                  High

-----------------------------------------------------------------------------


The ReAct loop — how an agent thinks
Every CrewAI agent follows the ReAct pattern (Reasoning + Acting). This is the core of how agents work:

Thought
"I need to search for laptops. Let me use the search tool."
↓
Action
Calls tavily_search("laptop under 80000 India")
↓
Observation
Gets back: HP Victus ₹79,999, Acer Nitro ₹78,990...
↓
Thought
"I have 3 products now. I can give my final answer."
↓
Final Answer
Returns the structured product list

------------------------------------------------------------------------------------------



How TavilySearchTool works
When the agent decides to use the search tool, this is what happens under the hood:

1. LLM outputs: Action: tavily_search("laptop under 80000 India")
↓
2. CrewAI intercepts this, calls Tavily API with that query
↓
3. Tavily searches the web, returns JSON with URLs + content snippets
↓
4. JSON result is fed back to the LLM as an "Observation"
↓
5. LLM reads it and decides: "enough data" or "search again"


---------------------------------------------------------------------------------------



Which agents have tools and why
Agent	       Has Tool?	Why?
Search Agent	✅ Tavily	Needs live product data from Amazon/Flipkart
Coupon Agent	✅ Tavily	Needs live offer/discount data
Analyst Agent	❌          None	Only needs to reason about data already given to it
Writer Agent	❌          None	Only needs to write — no external data needed

Agents 3 and 4 receive everything they need through the context parameter — the output from previous tasks is passed directly to them.
    
-----------------------------------------------------------------------------------

How crew.kickoff() works step by step
crew = Crew(
  agents=[search_agent, coupon_agent, analyst_agent, writer_agent],
  tasks=[task_search, task_coupons, task_analyse, task_report],
  process=Process.sequential  # run in order
)
result = crew.kickoff()

# What happens internally:
# 1. task_search runs → search_agent searches Tavily → returns product list
# 2. task_coupons runs → coupon_agent gets task_search output in its context
#    → searches Tavily for deals → returns coupon list  
# 3. task_analyse runs → analyst_agent gets task_search + task_coupons output
#    → scores products → returns ranked list
# 4. task_report runs → writer_agent gets ALL previous outputs
#    → writes final report → this is result



