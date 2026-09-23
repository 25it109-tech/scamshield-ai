import os
import json
from dotenv import load_dotenv
from openai import OpenAI

# Load .env file
load_dotenv()

# Get OpenRouter API key
api_key = os.getenv("OPENROUTER_API_KEY")

# Create OpenRouter client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key
)


def analyze_with_llm(user_input):
    """
    Analyze user input for possible digital scams.
    """

    # Check for empty input
    if not user_input or not user_input.strip():
        return {
            "error": "Input cannot be empty"
        }

    # Prompt for the AI
    prompt = f"""
You are ScamShield AI, a digital scam detection assistant.

Analyze the following user content for possible signs of a digital scam.

Identify:
1. Risk level: LOW, MEDIUM, or HIGH.
2. Confidence score between 0 and 1.
3. What was detected.
4. Why the content may be suspicious.
5. What the user should do next.

User content:
{user_input}

IMPORTANT:
Return ONLY a valid JSON object.
Do not write any text before or after the JSON.
Do not use Markdown.
Do not write labels such as "User Safety".
Even when the content is completely safe, you MUST return the JSON format below.

Return ONLY valid JSON in exactly this format:

{{
  "risk_level": "HIGH",
  "confidence": 0.95,
  "what": "Possible scam",
  "why": [
    "Reason 1",
    "Reason 2"
  ],
  "action": [
    "Action 1",
    "Action 2"
  ]
}}
"""

    # Call OpenRouter AI
    try:
        response = client.chat.completions.create(
            model="openrouter/free",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

    except Exception as e:
        return {
            "error": "AI service failed",
            "details": str(e)
        }

    # Check for empty AI response
    if not response.choices or not response.choices[0].message.content:
        return {
            "error": "AI returned an empty response"
        }

    # Get AI response
    result = response.choices[0].message.content

    # Convert AI response into JSON
    try:
        result_json = json.loads(result)
        return result_json

    except json.JSONDecodeError:
        return {
            "error": "AI returned invalid JSON",
            "raw_response": result
        }


