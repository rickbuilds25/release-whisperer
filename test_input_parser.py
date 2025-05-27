from input_parser import InputParser

parser = InputParser("sample_jira.csv")
parsed_output = parser.parse()

for entry in parsed_output:
    print(entry)
