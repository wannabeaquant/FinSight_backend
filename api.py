from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from main import run_all_agents
from fetch_data import get_stock_summary
from agents import hedge_fund_prompt, retail_prompt, news_prompt
from news_fetcher import get_google_news_rss
from llm_runner import run_agent_with_openrouter
from debate import conduct_debate

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

@app.get("/")
def root():
    return {"message": "Welcome to FinSight API 👋 Send a POST to /analyze with a ticker symbol."}

@app.post("/analyze")
def analyze_stock(req: TickerRequest):
    ticker = req.ticker.strip().upper()
    if not ticker:
        raise HTTPException(status_code=400, detail="Ticker cannot be empty")

    try:
        result = run_all_agents(ticker)
        if result is None:
            raise HTTPException(status_code=500, detail="Error analyzing ticker")
        return {"ticker": ticker, "analysis": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/analyze/{ticker}")
def analyze_via_url(ticker: str):
    return analyze_stock(TickerRequest(ticker=ticker))

# 👔 HedgeFundGPT only
@app.get("/hedgefund/{ticker}")
def run_hedge_fund_agent(ticker: str):
    data = get_stock_summary(ticker)
    if "error" in data:
        raise HTTPException(status_code=404, detail=data["error"])

    prompt = hedge_fund_prompt(data)
    result = run_agent_with_openrouter(prompt)
    return {"agent": "HedgeFundGPT", "result": result}

# 🧢 RetailGPT only
@app.get("/retail/{ticker}")
def run_retail_agent(ticker: str):
    data = get_stock_summary(ticker)
    if "error" in data:
        raise HTTPException(status_code=404, detail=data["error"])

    prompt = retail_prompt(data)
    result = run_agent_with_openrouter(prompt)
    return {"agent": "RetailGPT", "result": result}

# 🗞️ NewsBot only
@app.get("/news/{ticker}")
def run_news_agent(ticker: str):
    data = get_stock_summary(ticker)
    if "error" in data:
        raise HTTPException(status_code=404, detail=data["error"])

    headlines = get_google_news_rss(ticker)
    if not headlines:
        return {"agent": "NewsBot", "result": "⚠️ No recent news available."}

    prompt = news_prompt(headlines, data)
    result = run_agent_with_openrouter(prompt)
    return {"agent": "NewsBot", "result": result}

# 🤝 Consensus only (debate between agents)
from fastapi import Query

@app.get("/consensus/{ticker}")
def run_custom_debate(ticker: str, agents: list[str] = Query(default=["hedgefund", "retail", "news"])):
    agent_map = {
        "hedgefund": ("HedgeFundGPT", hedge_fund_prompt),
        "retail": ("RetailGPT", retail_prompt),
        "news": ("NewsBot", news_prompt)
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

            output = run_agent_with_openrouter(prompt)
            results[name] = output
        except Exception as e:
            results[name] = f"{name} failed: {str(e)}"

    valid_agents = list(results.keys())
    if len(valid_agents) < 2:
        raise HTTPException(status_code=400, detail="Need at least two valid agents for consensus")

    debate_result = conduct_debate(*[results[name] for name in valid_agents])
    return {
        "ticker": ticker,
        "agents": valid_agents,
        "consensus": debate_result
    }

