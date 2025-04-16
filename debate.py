from llm_runner import run_agent_with_openrouter

def conduct_debate(hedge_analysis, retail_analysis):
    DEBATE_PROMPT = f"""
[STRICT DEBATE FORMAT - USE BULLET POINTS]

**Financial Debate Moderator Instructions**
Analyze these perspectives:

🦈 Hedge Fund Analysis:
{hedge_analysis}

🦍 Retail Investor Analysis:
{retail_analysis}

**Required Elements:**
1. Identify 3 KEY DIFFERENCES in their approaches
2. Find 1 UNEXPECTED COMMON GROUND
3. Highlight the MOST CONTROVERSIAL POINT
4. Final Recommendation (BUY/HOLD/SELL) with RISK LEVEL (1-5)

**Output Format:**
🤝|CONSENSUS: [RECOMMENDATION]  
🔥|RISK LEVEL: [NUMBER]/5  
💼|RATIONALE: [1-sentence summary]  
⚔️|KEY DIFFERENCES:  
- Difference 1  
- Difference 2  
- Difference 3  
🕊️|COMMON GROUND:  
- [Common point]  
💣|CONTROVERSY:  
- [Most contentious issue]

ONLY respond using the format above. Do NOT explain or repeat the instructions.
"""

    return run_agent_with_openrouter(DEBATE_PROMPT)