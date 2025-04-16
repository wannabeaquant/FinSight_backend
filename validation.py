def validate_analysis(response):
    REQUIRED_KEYWORDS = ["BUY", "HOLD", "SELL"]
    return any(kw in response.upper() for kw in REQUIRED_KEYWORDS)

def process_response(response):
    if not validate_analysis(response):
        return "⚠️ ANALYSIS INCONCLUSIVE: " + response
    return response