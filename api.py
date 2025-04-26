from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from main import run_all_agents
from fetch_data import get_stock_summary
from agents import hedge_fund_prompt, retail_prompt, news_prompt, sell_side_prompt
from news_fetcher import get_google_news_rss
from llm_runner import run_agent_with_groq
from debate import conduct_debate
import re
from collections import Counter

app = FastAPI(title="FinSight API", description="AI Multi-Agent Stock Analyzer", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TickerRequest(BaseModel):
    ticker: str

class FollowUpRequest(BaseModel):
    consensus: str
    user_question: str

@app.get("/")
def root():
    return {"message": "Welcome to FinSight API 👋 Send a POST to /analyze with a ticker symbol."}

RATING_KEYWORDS = ["buy", "sell", "hold", "neutral"]

def parse_agent_output(output: str):
    lines = output.strip().splitlines()
    rating = "Neutral"
    summary = output.strip()

    for kw in RATING_KEYWORDS:
        pattern = re.compile(rf"\b{kw}\b", re.IGNORECASE)
        if pattern.search(output):
            rating = kw.capitalize()
            break

    return {"rating": rating, "summary": summary, "raw": output.strip()}

@app.post("/analyze")
def analyze_stock(req: TickerRequest):
    ticker = req.ticker.strip().upper()
    if not ticker:
        raise HTTPException(status_code=400, detail="Ticker cannot be empty")

    try:
        raw_results = run_all_agents(ticker)
        if raw_results is None:
            raise HTTPException(status_code=500, detail="Error analyzing ticker")

        structured_results = {
            agent: parse_agent_output(result)
            for agent, result in raw_results.items()
            if agent != "consensus"
        }

        consensus_result = raw_results.get("consensus", "No consensus available")

        votes = [v['rating'].lower() for v in structured_results.values() if 'rating' in v]
        final_vote = "Neutral"
        if votes:
            vote_counts = Counter(votes)
            final_vote = vote_counts.most_common(1)[0][0].capitalize()

        return {
            "ticker": ticker,
            "agents": structured_results,
            "final_recommendation": final_vote,
            "consensus": consensus_result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/analyze/{ticker}")
def analyze_via_url(ticker: str):
    return analyze_stock(TickerRequest(ticker=ticker))

@app.get("/hedgefund/{ticker}")
def run_hedge_fund_agent(ticker: str):
    data = get_stock_summary(ticker)
    if "error" in data:
        raise HTTPException(status_code=404, detail=data["error"])

    prompt = hedge_fund_prompt(data)
    result = run_agent_with_groq(prompt)
    return {"agent": "HedgeFundGPT", "result": result}

@app.get("/retail/{ticker}")
def run_retail_agent(ticker: str):
    data = get_stock_summary(ticker)
    if "error" in data:
        raise HTTPException(status_code=404, detail=data["error"])

    prompt = retail_prompt(data)
    result = run_agent_with_groq(prompt)
    return {"agent": "RetailGPT", "result": result}

@app.get("/news/{ticker}")
def run_news_agent(ticker: str):
    data = get_stock_summary(ticker)
    if "error" in data:
        raise HTTPException(status_code=404, detail=data["error"])

    headlines = get_google_news_rss(ticker)
    if not headlines:
        return {"agent": "NewsBot", "result": "⚠️ No recent news available."}

    prompt = news_prompt(headlines, data)
    result = run_agent_with_groq(prompt)
    return {"agent": "NewsBot", "result": result}

@app.get("/sellside/{ticker}")
def run_sell_side_agent(ticker: str):
    data = get_stock_summary(ticker)
    if "error" in data:
        raise HTTPException(status_code=404, detail=data["error"])

    prompt = sell_side_prompt(data)
    result = run_agent_with_groq(prompt)
    return {"agent": "SellSideAnalyst", "result": result}

@app.get("/consensus/{ticker}")
def run_custom_debate(ticker: str, agents: list[str] = Query(default=["hedgefund", "retail", "news", "sellside"])):
    agent_map = {
        "hedgefund": ("HedgeFundGPT", hedge_fund_prompt),
        "retail": ("RetailGPT", retail_prompt),
        "news": ("NewsBot", news_prompt),
        "sellside": ("SellSideAnalyst", sell_side_prompt)
    }

    ticker = ticker.strip().upper()
    data = get_stock_summary(ticker)
    if "error" in data:
        raise HTTPException(status_code=404, detail=data["error"])

    results = {}

    for agent_key in agents:
        if agent_key not in agent_map:
            raise HTTPException(status_code=400, detail=f"Invalid agent: {agent_key}")

        name, prompt_fn = agent_map[agent_key]

        try:
            if agent_key == "news":
                headlines = get_google_news_rss(ticker)
                if not headlines:
                    results[name] = "⚠️ No recent news available."
                    continue
                prompt = prompt_fn(headlines, data)
            else:
                prompt = prompt_fn(data)

            output = run_agent_with_groq(prompt)
            results[name] = output
        except Exception as e:
            results[name] = f"{name} failed: {str(e)}"

    debate_args = {
        "HedgeFundGPT": None,
        "RetailGPT": None,
        "NewsBot": None,
        "SellSideAnalyst": None
    }

    for name in debate_args:
        if name in results and not results[name].startswith("⚠️") and "failed" not in results[name]:
            debate_args[name] = results[name]

    valid_agents = [k for k, v in debate_args.items() if v is not None]

    if len(valid_agents) < 2:
        raise HTTPException(status_code=400, detail="Need at least two valid agents for consensus")

    debate_result = conduct_debate(
        hedge_analysis=debate_args["HedgeFundGPT"],
        retail_analysis=debate_args["RetailGPT"],
        news_analysis=debate_args["NewsBot"],
        sellside_analysis=debate_args["SellSideAnalyst"]
    )

    return {
        "ticker": ticker,
        "agents": valid_agents,
        "consensus": debate_result
    }

@app.post("/follow-up")
def follow_up_response(request: FollowUpRequest):
    from llm_runner import run_agent_with_groq

    prompt = f"""
You are a seasoned financial analyst AI following up on an investor's question.

🧠 Here is the consensus analysis provided earlier:
{request.consensus}

🙋 The investor now asks:
"{request.user_question}"

📌 Your task:
- Provide a clear and concise expert-level response.
- Reference key points from the consensus analysis.
- Include relevant data, trends, or reasoning that supports your reply.
- Maintain a confident, professional tone — no fluff.

Respond directly and helpfully to the investor’s question below:
"""

    try:
        response = run_agent_with_groq(prompt)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))