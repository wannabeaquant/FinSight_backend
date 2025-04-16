import openai

def hedge_fund_prompt(data):
    return f"""
[STRICT ANALYST FORMAT - USE BULLET POINTS]
## Hedge Fund Analysis: {data['name']} ({data['sector']})

**Financial Snapshot**:
- Market Cap: {data['market_cap']}
- P/E Ratio: {data['pe_ratio']} 
- Revenue: {data['revenue']}

**Key Analysis**:
1. Valuation Check: {"Overvalued" if data['pe_ratio'] > 25 else "Undervalued"} based on industry average
2. Growth Potential: Analyze {data['eps']} EPS trend
3. Risk Factors: List 2-3 sector-specific risks

**Final Recommendation**: 
[BUY/HOLD/SELL] - Max 15 word justification
"""

def retail_prompt(data):
    return f"""
[USE EMOJIS AND MEME REFERENCES - KEEP UNDER 200 TOKENS]

🚀 **{data['name']} Stock Breakdown** 🚀

📈 Key Stats:
- MCap: {data['market_cap']}
- EPS: {data['eps']}

💎 Diamond Hands or 💩 Paper Hands?
- Hype factor analysis (1-5 rating)
- Meme potential: {"🚀 Moon" if data['market_cap'] < 50000000000 else "😴 Sleepy"}

🏆 Final Call: [BULLISH/BEARISH] [BUY/HOLD/SELL]
"""