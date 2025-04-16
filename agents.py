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

ONLY respond using the format above. Do NOT explain or repeat the instructions.

"""

def retail_prompt(data):
    return f"""
[KEEP IT FUN! USE EMOJIS! MEME STOCK VIBES ONLY!]

🔥 **{data['name']} STOCK HYPE CHECK** 🔥

📊 Quick Stats:
- Market Cap: {data['market_cap']}
- EPS: {data['eps']}

💎 MEME POTENTIAL ANALYSIS:
{"🚀 MOON SHOT ALERT!" if data['raw_data']['market_cap'] < 100_000_000_000 else "🐢 BOOMER STOCK"}
{"🤑 EPS GROWTH HYPE!" if data['raw_data']['eps'] and data['raw_data']['eps'] > 2 else "😴 EPS SNOOZEFEST"}

🤔 YOUR GUT SAYS:
[1-2 sentences of pure emotion/meme logic]

🏆 FINAL CALL: [BUY/HOLD/SELL] 
[Include a meme reference or crypto analogy]

ONLY respond using the format above. Do NOT explain or repeat the instructions.
"""

def news_prompt(headlines, data):
    headlines_blob = "\n".join(headlines)

    return f"""
[NEWS ANALYSIS MODE]

Analyze recent news headlines related to {data['name']} ({data['sector']}) stock.

📰 Headlines:
{headlines_blob}

**Instructions:**
- Identify sentiment (Positive/Negative/Neutral)
- Highlight 2-3 key risks or opportunities mentioned
- Mention if any catalyst exists for price movement
- Final call: [BUY/HOLD/SELL] with 1-sentence justification

ONLY respond using the following format:

📊|SENTIMENT: [Positive/Negative/Neutral]  
⚠️|KEY RISKS/OPPORTUNITIES:  
- Bullet 1  
- Bullet 2  
🚀|CATALYST:  
- [Catalyst or None]  
🏁|RECOMMENDATION: [BUY/HOLD/SELL] – [short reasoning]
"""