import csv
import re
from typing import List, Dict

class InputParser:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def parse(self) -> List[Dict]:
        if self.file_path.endswith('.csv'):
            return self.parse_jira_csv()
        elif self.file_path.endswith('.md'):
            return self.parse_markdown_bullets()
        elif self.file_path.endswith('.log') or self.file_path.endswith('.txt'):
            return self.parse_git_log()
        else:
            raise ValueError("Unsupported file format")
    def parse(self):
        parsed_data = []
        with open(self.file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                row = {k.strip().lower(): v.strip() for k, v in row.items()}  # 🔥 THIS LINE
                parsed_data.append({
                    "source": "jira",
                    "ticket_id": row.get("ticket_id", ""),
                    "summary": row.get("summary", ""),
                    "type": row.get("type", ""),
                    "assignee": row.get("assignee", ""),
                    "status": row.get("status", "")
                })
        return parsed_data


    def parse_git_log(self) -> List[Dict]:
        entries = []
        with open(self.file_path, 'r', encoding='utf-8') as file:
            for line in file:
                match = re.match(r'^commit (\w+)', line)
                if match:
                    commit_hash = match.group(1)
                    entries.append({
                        "source": "git",
                        "ticket_id": commit_hash,
                        "summary": "Commit " + commit_hash,
                        "type": "Commit",
                        "assignee": "",
                        "status": ""
                    })
        return entries

    def parse_markdown_bullets(self) -> List[Dict]:
        entries = []
        with open(self.file_path, 'r', encoding='utf-8') as file:
            for line in file:
                if line.strip().startswith("- "):
                    entries.append({
                        "source": "markdown",
                        "ticket_id": "",
                        "summary": line.strip()[2:],
                        "type": "Note",
                        "assignee": "",
                        "status": ""
                    })
        return entries
