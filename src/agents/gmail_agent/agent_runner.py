import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from agents.gmail_agent.planner import planner_decide
from agents.gmail_agent.tools import TOOL_REGISTRY


def run_email_agent(email_text):
    tool_name = planner_decide(email_text)
    print(f"🤖 Chosen tool: {tool_name}")

    if tool_name not in TOOL_REGISTRY:
        return f"Unrecognized tool: {tool_name}"

    return TOOL_REGISTRY[tool_name](email_text)