from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from main import run_all_agents

app = FastAPI(title="FinSight API", description="AI Multi-Agent Stock Analyzer", version="1.0")

# Optional: Allow frontend/dev tools to access this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # update this in prod!
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
    ticker = ticker.strip().upper()
    if not ticker:
        raise HTTPException(status_code=400, detail="Ticker cannot be empty")

    try:
        result = run_all_agents(ticker)
        if result is None:
            raise HTTPException(status_code=500, detail="Error analyzing ticker")

        return {"ticker": ticker, "analysis": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
