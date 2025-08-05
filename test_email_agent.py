import os
import sys

# Set base path for project
base_path = os.path.abspath(os.path.join(os.getcwd()))
sys.path.append(os.path.join(base_path, "src"))

from agents.gmail_agent.agent_runner import run_email_agent

email = """
Hi M

We are seeking a skilled Data Engineer for our team at CoffeeBeans, based in Bengaluru and Pune. In this role, you will design, build, and manage scalable data platforms, collaborating with clients and internal teams to create robust data pipelines that support analytics and AI/ML initiatives. Your expertise will also contribute to mentoring junior engineers and establishing strong engineering practices.

If you are interested in this opportunity and meet the qualifications outlined in the job description, we encourage you to apply and join our dynamic team.

Thanks
Nikita
"""

response = run_email_agent(email)
print(response)