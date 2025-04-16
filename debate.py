from llm_runner import run_agent_with_openrouter

def conduct_debate(hedge_analysis, retail_analysis):
    DEBATE_PROMPT = f"""
    [FINANCIAL DEBATE MODERATOR]
    Analyze these two perspectives:

    🦈 Hedge Fund View:
    {hedge_analysis}

    🐂 Retail Investor View:
    {retail_analysis}

    Identify:
    1. 2 key areas of disagreement
    2. 1 potential compromise
    3. Final consensus recommendation (BUY/HOLD/SELL)

    Format:
    🤝 Consensus: [RECOMMENDATION]
    📌 Reasoning: [1-sentence explanation]
    """
    
    return run_agent_with_openrouter(DEBATE_PROMPT)