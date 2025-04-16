import yfinance as yf
from datetime import datetime

# fetch_data.py (updated)
def get_stock_summary(ticker):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        def format_money(value):
            if not value: return ("N/A", 0)
            if value >= 1e9: return (f"${value/1e9:.1f}B", value)
            return (f"${value/1e6:.0f}M", value)

        market_cap_fmt, market_cap_raw = format_money(info.get("marketCap"))
        revenue_fmt, revenue_raw = format_money(info.get("totalRevenue"))
        
        return {
            "name": info.get("longName", ticker),
            "market_cap": market_cap_fmt,
            "market_cap_raw": market_cap_raw,
            "pe_ratio": info.get("trailingPE", "N/A"),
            "eps": f"${info.get('trailingEps', 0):.2f}",
            "revenue": revenue_fmt,
            "sector": info.get("sector", "Unknown"),
            "raw_data": {  # Preserve numeric values for comparisons
                "market_cap": market_cap_raw,
                "pe_ratio": info.get("trailingPE"),
                "eps": info.get("trailingEps")
            }
        }
    except Exception as e:
        return {"error": str(e)}