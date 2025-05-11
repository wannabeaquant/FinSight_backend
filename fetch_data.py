import os
import requests
from tenacity import retry, wait_exponential, stop_after_attempt

FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")

@retry(wait=wait_exponential(multiplier=1, min=2, max=30),
       stop=stop_after_attempt(3))
def get_stock_summary(ticker):
    try:
        headers = {'X-Finnhub-Token': FINNHUB_API_KEY}
        
        # Fetch company profile
        profile_url = f"https://finnhub.io/api/v1/stock/profile2?symbol={ticker}"
        profile_res = requests.get(profile_url, headers=headers).json()
        
        # Fetch financials
        metrics_url = f"https://finnhub.io/api/v1/stock/metric?symbol={ticker}&metric=all"
        metrics_res = requests.get(metrics_url, headers=headers).json()

        if not profile_res or "name" not in profile_res:
            raise ValueError("Invalid ticker or no data from Finnhub")

        market_cap = float(metrics_res.get("metric", {}).get("marketCapitalization", 0))
        eps = float(metrics_res.get("metric", {}).get("epsTTM", 0))
        pe_ratio = metrics_res.get("metric", {}).get("peTTM", "N/A")
        revenue = float(metrics_res.get("metric", {}).get("revenueTTM", 0))

        def format_money(val):
            return f"${val/1e9:.1f}B" if val >= 1e9 else f"${val/1e6:.0f}M"

        return {
            "name": profile_res.get("name", ticker),
            "market_cap": format_money(market_cap),
            "market_cap_raw": market_cap,
            "pe_ratio": pe_ratio,
            "eps": f"${eps:.2f}",
            "revenue": format_money(revenue),
            "sector": profile_res.get("finnhubIndustry", "Unknown"),
            "raw_data": {
                "market_cap": market_cap,
                "pe_ratio": float(pe_ratio) if pe_ratio != "N/A" else None,
                "eps": eps
            }
        }

    except Exception as e:
        return {"error": f"Finnhub API failed: {str(e)}"}
