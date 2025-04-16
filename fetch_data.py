import yfinance as yf
from datetime import datetime

def get_stock_summary(ticker):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        # Format numbers with error handling
        def format_money(value):
            if not value: return "N/A"
            return f"${value/1e9:.1f}B" if value >= 1e9 else f"${value/1e6:.0f}M"

        return {
            "name": info.get("longName", ticker),
            "market_cap": format_money(info.get("marketCap")),
            "pe_ratio": info.get("trailingPE", "N/A"),
            "eps": f"${info.get('trailingEps', 0):.2f}",
            "revenue": format_money(info.get("totalRevenue")),
            "sector": info.get("sector", "Unknown"),
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
    except Exception as e:
        print(f"Data Error: {str(e)}")
        return {"error": f"Failed to fetch data for {ticker}"}