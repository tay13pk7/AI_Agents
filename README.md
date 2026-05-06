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