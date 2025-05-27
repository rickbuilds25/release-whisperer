from input_parser import InputParser
from quality_guard import QualityGuard

parser = InputParser("sample_jira.csv")
parsed_data = parser.parse()

for item in parsed_data:
    print(item)

guard = QualityGuard(parsed_data)
results = guard.evaluate()

for item in results:
    print(f"[{item['ticket_id']}] {item['summary']}")
    for issue in item['issues']:
        print(f"  ❌ {issue}")
    print()
