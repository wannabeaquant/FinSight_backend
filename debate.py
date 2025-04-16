from llm_runner import run_agent_with_openrouter

def conduct_debate(hedge_analysis, retail_analysis, news_analysis):
    DEBATE_PROMPT = f"""
[STRICT DEBATE FORMAT - INCLUDE ALL 3 PERSPECTIVES]

**Financial Debate Moderator Instructions**
Analyze these perspectives:

🦈 Hedge Fund Analysis:
{hedge_analysis}

🦍 Retail Investor Analysis:
{retail_analysis}

📰 News-Based Analysis:
{news_analysis}

**Instructions:**
1. Compare how all 3 differ in methodology or assumptions
2. Highlight a shared observation between at least 2 agents
3. Identify the most polarizing claim
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