def reply_to_job(email_text):
    return f"This seems like a job opportunity. Here's a polite reply:\n\nThank you for reaching out! I'd love to learn more. Could you please share more details?"

def summarize_newsletter(email_text):
    return f"Newsletter Summary:\n• Point 1\n• Point 2\n• Point 3"

def classify_promo(email_text):
    return f"Looks like a promo. Ignore."

def reply_to_friend(email_text):
    return f"Hey! Thanks for writing. I’ll get back to you soon :)"

TOOL_REGISTRY = {
    "reply_to_job": reply_to_job,
    "summarize_newsletter": summarize_newsletter,
    "classify_promo": classify_promo,
    "reply_to_friend": reply_to_friend
}

TOOL_DESCRIPTIONS = """
Available Tools:

1. reply_to_job - Use if it's a recruiter or job-related email
2. summarize_newsletter - Use for newsletters or notifications
3. classify_promo - Use for advertisements or product emails
4. reply_to_friend - Use for informal/personal messages
"""

