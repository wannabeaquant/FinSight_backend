from llm_runner import run_agent_with_openrouter

def conduct_debate(hedge_analysis=None, retail_analysis=None, news_analysis=None):
    DEBATE_PROMPT = f"""
[STRICT DEBATE FORMAT - INCLUDE ALL PERSPECTIVES PRESENT]

**Financial Debate Moderator Instructions**
Analyze these perspectives:

{"🦈 Hedge Fund Analysis:\n" + hedge_analysis if hedge_analysis else ""}
{"🦍 Retail Investor Analysis:\n" + retail_analysis if retail_analysis else ""}
{"📰 News-Based Analysis:\n" + news_analysis if news_analysis else ""}

**Instructions:**
1. Compare how the perspectives differ in methodology or assumptions.
2. Highlight any shared observations.
3. Identify the most polarizing claim.
4. Final Consensus: [BUY/HOLD/SELL] + risk score (1–5)

**Output Format:**
🤝|CONSENSUS: [RECOMMENDATION]  
🔥|RISK LEVEL: [NUMBER]/5  
💼|RATIONALE: [1-sentence summary]  
📈|KEY DIFFERENCES:  
- Difference 1  
- Difference 2  
- Difference 3  
🧹|COMMON GROUND:  
- [Shared insight]  
💣|CONTROVERSY:  
- [Most contentious issue]

ONLY respond using the format above. Do NOT explain or repeat the instructions.
"""
    return run_agent_with_openrouter(DEBATE_PROMPT)
