
# 🧬 Release Whisperer v1.1

An AI-powered agent that automates the most painful part of product development: writing, managing, and exporting clean, contextual release notes from Jira tickets, Git logs, or even raw bullet points.

---

## 🚀 Why It Exists

Let’s face it:  
- No PM likes writing release notes.  
- No engineer likes formatting them.  
- No stakeholder likes chasing them down.

So we built **Release Whisperer**—a local-first Python agent that:
- Parses raw Jira stories, Git logs, or bullet notes
- Runs quality checks (title, tone, clarity)
- Flags low-quality inputs (e.g., vague tickets)
- Auto-generates clean summaries in multiple tones
- Exports to `.docx`, `.md`, or Slack-ready formats
- Saves output in a vault for reuse

---

## 🧠 Core Modules

| Module                           | Purpose                                                       |
|----------------------------------|---------------------------------------------------------------|
| `input_parser.py`                | Parses Jira CSV into structured ticket dictionaries           |
| `quality_guard.py`               | Flags weak or generic ticket summaries                        |
| `summarizer_agent.py`            | Uses GPT-4 to generate summaries in multiple tones            |
| `formatter.py`                   | Converts summaries to `.docx`, `.md`, and Slack block text    |
| `formatter_runner.py`            | CLI wrapper to run formatters standalone                      |
| `release_whisperer_agent_runner.py` | Runs full E2E flow via CLI (input → summary → expor      |

---

## 🧪 How to Run

### 🧵 Full End-to-End Flow
```bash
python3 release_whisperer_agent_runner.py \
  --input jira_input.csv \
  --tones dev,exec \
  --format docx
```

- `--input` → Optional: path to a Jira CSV (or defaults to `sample_jira.csv`)
- `--tones` → Pick one or more: `dev`, `exec`, `sassy`
- `--format` → Output format: `docx`, `markdown`, or `slack`

### 🧩 Format Only (via Formatter Runner)
```bash
python3 formatter_runner.py --format docx
```

This will pick up the last `release_summary.json` and export in your chosen format.

---

## 🔐 Output Vault

All exports are saved in the `/release_output/` folder:
- `release_summary.docx`
- `release_summary.md`
- `release_slack.txt`
- `release_summary.json` (raw summary data)

---

## 🧪 Test Coverage

```bash
python3 test_input_parser.py
python3 test_quality_guard.py
python3 test_summarizer_agent.py
```

---

## 🔁 DevOps Integration (Jira + GitHub)

- Commits with ticket IDs (e.g. `KAN-5`) update Jira
- Pull Requests auto-move tickets to “Testing”
- Merge = ticket marked as “Done”

---

## 💡 Example Tickets (from sample_jira.csv)

| Ticket ID | Summary                                                       |
|-----------|---------------------------------------------------------------|
| RW-1      | Implement release parser for raw CSV input                    |
| RW-2      | Bug fix                                                       |
| RW-3      | Misc updates and changes                                      |
| RW-7      | Refactor release module to support multi-source inputs        |

---

## 👨‍💻 Made By

**Arindam Nath a.k.a. The Product Geek**  
With support from **Summer**, the AI co-builder at TPG

🔗 [theproductgeek.club](https://theproductgeek.club)  
📸 Instagram: [@the.productgeek](https://www.instagram.com/the.productgeek)  
🔗 LinkedIn: [Arindam Nath](https://www.linkedin.com/in/arindam-nath/)

---

## ✨ Future Scope

- 🧠 KAN-6: Add hallucination audit guard  
- 🛠 KAN-7: Full release runner agent with config YAML  
- 🌍 KAN-8: Multi-language summary generation

---

Made with 💕 by The Product Geek · Built for speed, soul & sanity.
