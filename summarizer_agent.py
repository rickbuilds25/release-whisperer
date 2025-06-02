import os
import json
import openai
from dotenv import load_dotenv
from input_parser import InputParser
from enum import Enum

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

class SummaryTone(Enum):
    DEV = "developer-friendly"
    EXEC = "executive-style"
    SASSY = "pm-sassy"

SYSTEM_ROLES = {
    SummaryTone.DEV: "You're a senior developer summarizing key changes for tech teams.",
    SummaryTone.EXEC: "You're a Chief Product Officer summarizing changes for leadership review.",
    SummaryTone.SASSY: "You're a Gen Z PM with attitude summarizing changes in a fun, bold style."
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

    def generate_summary(self, input_text, tone: SummaryTone):
        prompt = self._build_prompt(input_text)
        system_prompt = SYSTEM_ROLES.get(tone, SYSTEM_ROLES[SummaryTone.SASSY])
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

    def _build_prompt(self, input_text):
        return f"Here’s the change: {input_text}\nSummarize it in your own style."

    def summarize_all(self, tickets, tones):
        summaries = []
        for t in tickets:
            result = {
                "ticket_id": t["ticket_id"],
                "summary": t["summary"],
                "summaries": {}
            }
            for tone in tones:
                tone_enum = tone if isinstance(tone, SummaryTone) else SummaryTone[tone.upper()]
                summary_text = self.generate_summary(t["summary"], tone_enum)
                result["summaries"][tone_enum.value] = summary_text
            summaries.append(result)
        return summaries

# Optional CLI mode for local runs
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

    print("Select tone(s) to generate summaries:")
    for i, tone in enumerate(SummaryTone, start=1):
        print(f"{i}. {tone.value}")

    selection = input("Enter tone numbers (comma-separated, e.g., 1,3): ").strip()
    try:
        selected_indices = [int(idx.strip()) for idx in selection.split(",") if idx.strip().isdigit()]
        selected_tones = [list(SummaryTone)[i - 1] for i in selected_indices if 0 < i <= len(SummaryTone)]
    except:
        print("❌ Invalid selection. Exiting.")
        sys.exit(1)

    if not selected_tones:
        print("❌ No valid tones selected. Exiting.")
        sys.exit(1)

    parser = InputParser(input_file)
    parsed_data = parser.parse()
    agent = SummarizerAgent()

    results = agent.summarize_all(parsed_data, selected_tones)

    with open("release_summary.json", "w") as outfile:
        json.dump(results, outfile, indent=2)

    print("✅ Release summaries saved to release_summary.json")
