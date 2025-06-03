import os
import argparse
from datetime import datetime
from input_parser import InputParser
from quality_guard import QualityGuard
from summarizer_agent import SummarizerAgent
from formatter_runner import format_to_docx, format_to_markdown, format_to_slack_block

# Constants
SAMPLE_FILE = "sample_jira.csv"
RELEASE_ROOT = "release_output"


def run_pipeline(jira_input=None, tones=["dev", "exec", "sassy"], format="docx"):
    print("\n🚀 Launching Release Whisperer Agent...")

    # Step 1: Input Parser
    if jira_input and os.path.exists(jira_input):
        print(f"📥 Parsing Jira file: {jira_input}")
        tickets = InputParser(jira_input).parse()
    elif os.path.exists(SAMPLE_FILE):
        choice = input("No Jira input found. Run with local sample file? (yes/no): ").strip().lower()
        if choice != "yes":
            print("❌ Aborting.")
            return
        print(f"📥 Using sample Jira file: {SAMPLE_FILE}")
        tickets = InputParser(SAMPLE_FILE).parse()
    else:
        print("❌ No input file available.")
        return

    if not tickets:
        print("⚠️ No valid tickets parsed. Exiting.")
        return

    # Step 2: Quality Guard
    print("🛡 Running quality checks on tickets...")
    good_tickets = []
    for t in tickets:
        issues = QualityGuard().check_summary_quality(t["ticket_id"], t["summary"])
        if issues:
            print(f"⚠️ [SKIPPED] {t['ticket_id']} — {t['summary']}\n     Issues: {issues}")
        else:
            good_tickets.append(t)

    if not good_tickets:
        print("❌ All tickets failed quality check. Exiting.")
        return

    # Step 3: Summarizer Agent
    print("🧠 Generating summaries...")
    summaries = SummarizerAgent().summarize_all(good_tickets, tones)

    # Step 4: Prepare Output Directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    version_folder = f"release_{timestamp}"
    output_dir = os.path.join(RELEASE_ROOT, version_folder)
    os.makedirs(output_dir, exist_ok=True)

    # Save JSON file
    import json
    summary_json_path = os.path.join(output_dir, "release_summary.json")
    with open(summary_json_path, "w") as f:
        json.dump(summaries, f, indent=2)
    print(f"📁 Intermediate summary saved to {summary_json_path}")

    # Step 5: Formatter
    print(f"🎨 Formatting to {format.upper()}...")
    if format == "docx":
        format_to_docx(summaries, os.path.join(output_dir, "release_summary.docx"))
    elif format == "markdown":
        format_to_markdown(summaries, os.path.join(output_dir, "release_summary.md"))
    elif format == "slack":
        format_to_slack_block(summaries, os.path.join(output_dir, "release_slack.txt"))
    else:
        print("❌ Unknown format. Aborting.")
        return

    print("✅ Release Agent completed successfully.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the full Release Agent pipeline")
    parser.add_argument("--input", help="Path to Jira CSV file", required=False)
    parser.add_argument("--tones", help="Comma-separated tones: dev,exec,sassy", default="dev,exec,sassy")
    parser.add_argument("--format", help="Output format: docx, markdown, slack", default="docx")

    args = parser.parse_args()
    tone_list = [t.strip() for t in args.tones.split(",") if t.strip() in ["dev", "exec", "sassy"]]
    run_pipeline(jira_input=args.input, tones=tone_list, format=args.format)
