# quality_guard.py

class QualityGuard:
    def __init__(self, parsed_data):
        self.data = parsed_data

    def is_generic(self, summary):
        generic_keywords = ["fix", "bug", "update", "misc", "change"]
        return any(word in summary.lower() for word in generic_keywords)

    def is_short(self, summary):
        return len(summary.split()) < 4

    def has_missing_verb(self, summary):
        # Naive check: does not contain common verbs
        common_verbs = ["add", "remove", "fix", "implement", "create", "update", "improve", "refactor"]
        return not any(verb in summary.lower() for verb in common_verbs)

    def evaluate(self):
        flagged = []
        for entry in self.data:
            summary = entry.get("summary", "")
            issues = []
            if self.is_short(summary):
                issues.append("Too short")
            if self.is_generic(summary):
                issues.append("Generic title")
            if self.has_missing_verb(summary):
                issues.append("Likely missing a verb")

            if issues:
                flagged.append({
                    "ticket_id": entry.get("ticket_id", ""),
                    "summary": summary,
                    "issues": issues
                })
        return flagged
