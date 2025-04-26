import os
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential
from validation import process_response

# Update to use Groq API key
API_KEY = os.getenv("API_KEY")

# Initialize Groq client
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=API_KEY
)

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def run_agent_with_groq(prompt):  # Renamed function
    try:
        print("✅ Prompt ready to send to Groq...")
        print("=" * 60)
        print(prompt)
        print("=" * 60)

        response = client.chat.completions.create(
            model="llama3-70b-8192",  # Updated model name
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000,
            top_p=1,
            frequency_penalty=0.2,
            presence_penalty=0,
)

        if response.choices and len(response.choices) > 0:
            reply = response.choices[0].message.content.strip()
            print("✅ Got response from Groq.")
            return process_response(reply)
        else:
            print("❌ No choices returned by Groq.")
            return "Analysis failed: No response choices received."

    except Exception as e:
        print(f"❌ Exception during Groq call: {e}")
        return f"Analysis failed: {str(e)}"