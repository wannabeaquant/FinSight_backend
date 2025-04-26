from fastapi import FastAPI
from fetch_data import get_stock_summary
from agents import hedge_fund_prompt, retail_prompt, news_prompt, sell_side_prompt
from llm_runner import run_agent_with_groq
from debate import conduct_debate
from news_fetcher import get_google_news_rss
from colorama import Fore, Style, init
init(autoreset=True)
import os

AGENTS = {
    "HedgeFundGPT": hedge_fund_prompt,
    "RetailGPT": retail_prompt,
    "SellSideAnalyst": sell_side_prompt
}

# main.py (updated section)
def run_all_agents(ticker):
    data = get_stock_summary(ticker)
    if 'error' in data:
        print(f"{Fore.RED}❌ Data Error: {data['error']}")
        return None

    results = {}

    print(f"\n🔍 Analyzing {data['name']} ({ticker})")
    print(f"📊 Market Cap: {data['market_cap']} | 📈 P/E Ratio: {data['pe_ratio']}\n")

    # Run agents
    for name, prompt_fn in AGENTS.items():
        try:
            if not data['raw_data']['market_cap']:
                raise ValueError("Missing numeric market cap data")

            prompt = prompt_fn(data)
            print(f"\n🚀 Running {name}...")
            output = run_agent_with_groq(prompt)
            results[name] = output
            print(f"\n✅ {name} Completed:")
            print(output)
            print("="*80)
        except Exception as e:
            print(f"{Fore.RED}❌ Agent {name} failed: {str(e)}")
            results[name] = f"{name} analysis failed: {str(e)}"
            if name == "RetailGPT":
                results[name] = "🚀 TO THE MOON! BUY! (Fallback analysis)"

    # === NEWSBOT ===
    print("\n🗞️ Fetching recent news...")
    headlines = get_google_news_rss(ticker)

    if not headlines:
        news_analysis = "⚠️ No recent news available."
    else:
        news_prompt_blob = news_prompt(headlines, data)
        news_analysis = run_agent_with_groq(news_prompt_blob)

    print("\n✅ NewsBot Completed:")
    print(news_analysis)
    print("="*80)

    results["NewsBot"] = news_analysis

    # Run debate
    if all(v is not None for v in results.values()):
        print("\n💼 Starting Agent Debate...")
        debate_result = conduct_debate(
            results.get('HedgeFundGPT'),
            results.get('RetailGPT'),
            results.get('NewsBot'),
            results.get('SellSideAnalyst')
        )
        results['Consensus'] = debate_result
        print("\n🤝 Final Consensus:")
        print(debate_result)

    return results

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    ticker = input("Enter a stock ticker (e.g., AAPL): ").strip().upper()

    responses = run_all_agents(ticker)

    if responses:
        print("\n📊 Final Results:")
        for agent, response in responses.items():
            print(f"\n{Fore.CYAN}{agent}:{Style.RESET_ALL}")
            print(response)
            print(f"{Fore.LIGHTBLACK_EX}{'-'*80}{Style.RESET_ALL}")

    print("\n✅ Analysis complete. Exiting...\n")
    input("Press Enter to close...")