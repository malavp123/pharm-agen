from dotenv import load_dotenv
load_dotenv()
import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_response(email_data: dict) -> str:
    subject = email_data.get("subject", "").strip()
    body = email_data.get("body", "").strip()
    sender = email_data.get("sender", "the requester")

    prompt = f"""
You are my personal email assistant.

Your job is to help me write polite, clear, and smart replies to incoming emails. 
You must:
- Match the tone of the sender, but err on the side of professionalism
- Avoid quoting the original message
- Respond helpfully based on the email content
- Keep the reply short and actionable, unless more detail is required

From: {sender}
Subject: {subject}
Message:
\"\"\"
{body}
\"\"\"

Write a reply I can send back:
"""

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",  # or "gpt-3.5-turbo" if latency/cost matters
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=400
    )

    reply = response['choices'][0]['message']['content'].strip()
    return reply