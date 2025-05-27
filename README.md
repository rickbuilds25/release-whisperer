# 🧬 Release Whisperer v1.0

An AI-powered agent that automates the most painful part of product development: writing, managing, and retrieving clean, contextual release notes from Jira tickets, Git logs, or even raw bullet points.

## 🚀 Why It Exists

Let’s face it:  
No PM likes writing release notes.  
No engineer likes formatting them.  
No stakeholder likes chasing them down.

So I built **Release Whisperer**—a local-first Python agent that:
- Parses raw Jira stories, git logs, or notes
- Runs quality checks (title, tone, clarity)
- Flags missing Acceptance Criteria
- Auto-generates clean, branded summaries
- Stores them in a searchable output vault

## 🛠 Tech Stack

- Python 3.x
- Git + GitHub
- Local CSV & Markdown parsing
- GPT-powered summarizer
- Terminal-based CLI (coming soon)

## 🔄 DevOps Integration

- ✅ GitHub → Jira linkage active  
- ✅ Commits auto-link to tickets (`KAN-#`)
- ✅ Automation:
  - Commit → `In Progress`
  - PR → `Testing`
  - Merge → `Done`

## 🔍 Modules

| Module           | Description                                 |
|------------------|---------------------------------------------|
| `input_parser.py` | Parses raw inputs (Jira CSV, Git logs, etc.) |
| `quality_guard.py` | Flags vague/incomplete input (WIP)          |
| `summarizer_agent.py` | Generates clean summaries using GPT       |
| `ac_checker.py`  | Detects missing Acceptance Criteria (WIP)   |
| `vault_writer.py` | Outputs clean release doc bundle           |

## 🧪 How to Run

```bash
python3 test_input_parser.py

MORE COMMANDS COMING SOON...

🧠 Built by - Arindam a.k.a. @theproductgeek with Summer (your PM-AI whisperer)
Made with ☕, 💻, and hatred for manually updating Jira.