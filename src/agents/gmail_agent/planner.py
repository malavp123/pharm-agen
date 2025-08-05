import os
from dotenv import load_dotenv
load_dotenv()
import openai
from agents.gmail_agent.tools import TOOL_REGISTRY, TOOL_DESCRIPTIONS

openai.api_key = os.getenv("OPENAI_API_KEY")

def planner_decide(email_text: str) -> str:
    prompt = f"""
You are an intelligent agent. Choose the correct tool based on the email content.
Only reply with one of: reply_to_job, summarize_newsletter, classify_promo, reply_to_friend

{TOOL_DESCRIPTIONS}

EMAIL:
\"\"\"
{email_text}
\"\"\"

Which tool should be used?
"""
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        max_tokens=10
    )
    return response['choices'][0]['message']['content'].strip()