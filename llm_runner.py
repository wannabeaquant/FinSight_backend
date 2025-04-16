import os
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential
from validation import process_response

# Safely get API key from env or hardcoded fallback (optional)
API_KEY = os.getenv("OPENROUTER_API_KEY", "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")

# Initialize OpenRouter client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_KEY,
    default_headers={
        "HTTP-Referer": "http://localhost",
        "X-Title": "FinSight"
    }
)

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def run_agent_with_openrouter(prompt):
    try:
        print("✅ Prompt ready to send to OpenRouter...")
        print("=" * 60)
        print(prompt)
        print("=" * 60)

        # Perform chat completion
        response = client.chat.completions.create(
            model="meta-llama/llama-3-70b-instruct",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000,
            top_p=1,
            frequency_penalty=0.2,
            presence_penalty=0,
        )

        # Check and return result
        if response.choices and len(response.choices) > 0:
            reply = response.choices[0].message.content.strip()
            print("✅ Got response from OpenRouter.")
            return process_response(reply)
        else:
            print("❌ No choices returned by OpenRouter.")
            return "Analysis failed: No response choices received."

    except Exception as e:
        print(f"❌ Exception during OpenRouter call: {e}")
        return f"Analysis failed: {str(e)}"
