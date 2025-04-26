from llm_runner import run_agent_with_groq

def conduct_debate(hedge_analysis=None, retail_analysis=None, news_analysis=None, sellside_analysis=None):
    hedge_section = f"🦈 Hedge Fund Analysis:\n{hedge_analysis}\n" if hedge_analysis else ""
    retail_section = f"🦍 Retail Investor Analysis:\n{retail_analysis}\n" if retail_analysis else ""
    news_section = f"📰 News-Based Analysis:\n{news_analysis}\n" if news_analysis else ""
    sellside_section = f"💼 Sell-Side Analyst Report:\n{sellside_analysis}\n" if sellside_analysis else ""

    DEBATE_PROMPT = f"""
[STRICT DEBATE FORMAT - INCLUDE ALL PERSPECTIVES PRESENT]

**Financial Debate Moderator Instructions**
Analyze these perspectives:

{hedge_section}{retail_section}{news_section}{sellside_section}

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
""".strip()

    return run_agent_with_groq(DEBATE_PROMPT)