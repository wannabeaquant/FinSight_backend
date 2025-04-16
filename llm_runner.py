import os
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential

# Initialize OpenAI client with the correct base URL and API key
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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",
)

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def run_agent_with_openrouter(prompt):
    try:
        # Prepare the request data for the OpenRouter API
        completion = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "http://localhost",
                "X-Title": "FinSight",
            },
            model="meta-llama/llama-3-70b-instruct",
            temperature=0.7,
            max_tokens=1000,
            top_p=1,
            frequency_penalty=0.2,
            presence_penalty=0,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        # Handle response validation
        if completion.choices and len(completion.choices) > 0:
            return completion.choices[0].message.content.strip()
        else:
            print("API Error: Received empty choices array")
            return "Model response format error"

    except Exception as e:
        print(f"API Error: {str(e)}")
        return f"Model failed to respond: {str(e)}"