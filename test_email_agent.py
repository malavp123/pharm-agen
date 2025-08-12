import os
import sys

# Set base path for project
base_path = os.path.abspath(os.path.join(os.getcwd()))
sys.path.append(os.path.join(base_path, "src"))

from agents.gmail_agent.agent_runner import run_email_agent

email = """
Hi ParekhMalav,

As part of our dedication to community-driven evaluation, we’re excited to introduce Kaggle Game Arena. Here, top AI models compete head-to-head in strategic games, starting with chess.

Game Arena is designed to benchmark model performance in dynamic, interactive environments. You’ll see how models like Gemini, Claude, and others handle real-time decision-making, strategic planning, and adaptation, all running on Kaggle. Visit kaggle.com/game-arena and learn more on our blog.

A screencast GIF of someone showcasing Game Arena on Kaggle

Learn More
First up is an AI chess exhibition tournament in partnership with Chess.com, Take Take Take, and top players including Hikaru Nakamura, Levy Rozman, and Magnus Carlsen. Matchups will stream live August 5–7 at 10:30 AM PT each day on kaggle.com/game-arena.

Each game has its own open-source environment and harness, with results published as live leaderboards on Kaggle Benchmarks. On August 7, we’ll reveal the Chess Text Input leaderboard, the inaugural installment of the broader Game Arena, which combines rigorous scientific methodology with spectator-friendly excitement. Over time, Game Arena will expand to include more games, modalities, and evaluation setups.

Curious what your favorite models are capable of? Dive into the bracket or catch the action live at kaggle.com/game-arena.

Happy Kaggling,

The Kaggle Team
"""

response = run_email_agent(email)
print(response)