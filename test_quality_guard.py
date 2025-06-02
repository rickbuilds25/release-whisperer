from quality_guard import QualityGuard
from input_parser import InputParser

def test_quality_guard():
    parser = InputParser("sample_jira.csv")
    data = parser.parse()

    guard = QualityGuard()

    for entry in data:
        ticket_id = entry["ticket_id"]
        summary = entry["summary"]
        issues = guard.check_summary_quality(ticket_id, summary)
        if issues:
            print(f"Issues found in {ticket_id}: {issues}")
        else:
            print(f"[{ticket_id}] ✅ Passed quality check")

if __name__ == "__main__":
    test_quality_guard()
