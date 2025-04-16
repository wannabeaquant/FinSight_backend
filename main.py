from fetch_data import get_stock_summary
from agents import hedge_fund_prompt, retail_prompt
from llm_runner import run_agent_with_openrouter
from debate import conduct_debate
import os

AGENTS = {
    "HedgeFundGPT": hedge_fund_prompt,
    "RetailGPT": retail_prompt,
}

def run_all_agents(ticker):
    # Get data with error handling
    data = get_stock_summary(ticker)
    if 'error' in data:
        print(f"❌ Error: {data['error']}")
        return None

    results = {}
    
    print(f"\n🔍 Analyzing {data['name']} ({ticker})")
    print(f"📊 Market Cap: {data['market_cap']} | 📈 P/E Ratio: {data['pe_ratio']}\n")

    # Run agents
    for name, prompt_fn in AGENTS.items():
        try:
            prompt = prompt_fn(data)
            print(f"\n🚀 Running {name}...")
            output = run_agent_with_openrouter(prompt)
            results[name] = output
            print(f"\n✅ {name} Completed:")
            print(output)
            print("="*80)
        except Exception as e:
            print(f"❌ Agent {name} failed: {str(e)}")
            results[name] = f"{name} analysis unavailable"

    # Run debate
    if all(v is not None for v in results.values()):
        print("\n💼 Starting Agent Debate...")
        debate_result = conduct_debate(results['HedgeFundGPT'], results['RetailGPT'])
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
            print(f"\n{agent}:")
            print(response)
            print("-"*80)