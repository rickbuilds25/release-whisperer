import os
import openai
from dotenv import load_dotenv
from input_parser import InputParser

# Load environment variables from .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

SYSTEM_ROLES = {
    "developer-friendly": "You're a senior developer summarizing key changes for tech teams.",
    "executive-style": "You're a Chief Product Officer summarizing changes for leadership review.",
    "pm-sassy": "You're a Gen Z PM with attitude summarizing changes in a fun, bold style."
}

def create_sample_file_if_missing():
    sample_data = """ticket_id,summary,type,assignee,status
RW-1,Implement release parser for raw CSV input,Task,Arindam,To Do
RW-2,Bug fix,Task,Arindam,In Progress
RW-3,Misc updates and changes,Task,Arindam,To Do
RW-4,Login button,Task,Arindam,To Do
RW-5,Fix,Task,Arindam,To Do
RW-6,Update stuff quickly,Task,Arindam,To Do
RW-7,Refactor release module to support multi-source inputs,Task,Arindam,To Do
"""
    with open("sample_jira.csv", "w") as f:
        f.write(sample_data)

class SummarizerAgent:
    def __init__(self):
        pass

    def generate_summary(self, input_text, tone="pm-sassy"):
        prompt = self._build_prompt(input_text, tone)
        system_prompt = SYSTEM_ROLES.get(tone, SYSTEM_ROLES["pm-sassy"])
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error generating summary: {e}"

    def _build_prompt(self, input_text, tone):
        return f"Here’s the change: {input_text}\nSummarize it in your own style."

# Example use with conditional file input
if __name__ == "__main__":
    import sys

    input_file = "sample_jira.csv"

    if os.path.exists("jira_input.csv"):
        input_file = "jira_input.csv"
    else:
        user_input = input("No Jira input found. Do you want to run with the local sample file? (yes/no): ").strip().lower()
        if user_input != "yes":
            print("❌ Exiting: Please provide a valid Jira input file named 'jira_input.csv'.")
            sys.exit(1)
        else:
            print("✅ Running with local sample_jira.csv")
            if not os.path.exists("sample_jira.csv"):
                create_sample_file_if_missing()

    parser = InputParser(input_file)
    parsed_data = parser.parse()
    agent = SummarizerAgent()

    for entry in parsed_data:
        print(f"\n🔹 Ticket: {entry['ticket_id']} — {entry['summary']}")
        for tone in ["developer-friendly", "executive-style", "pm-sassy"]:
            print(f"🧠 {tone.title()} Summary:")
            print(agent.generate_summary(entry['summary'], tone=tone))
            print("—" * 40)
