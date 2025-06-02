class QualityGuard:
    def __init__(self):
        pass

    def check_summary_quality(self, ticket_id, summary):
        issues = []

        if not summary or len(summary.strip()) < 10:
            issues.append("❌ Too short")

        if summary.lower() in ["fix", "update", "misc updates and changes"]:
            issues.append("❌ Generic title")

        if not any(verb in summary.lower() for verb in ["fix", "implement", "create", "add", "remove", "refactor", "support", "update"]):
            issues.append("❌ Likely missing a verb")

        if issues:
            print(f"[{ticket_id}] {summary}")
            for issue in issues:
                print(f"  {issue}")
            print()
        return issues
