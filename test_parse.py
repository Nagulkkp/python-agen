import re, json

test_strings = [
    'Action: read_code({"file_path": "app/foo.php", "start_line": 40})',
    'Action: find_route\nAction Input: {"keyword": "billing"}',
    'Action: search_code\nActionInput: {"query": "billing"}'
]

for s in test_strings:
    action, raw_input = None, "{}"
    call_match = re.search(r"Action:\s*([a-zA-Z0-9_]+)\s*\(([\s\S]*?)\)", s, re.IGNORECASE)
    if call_match:
        action = call_match.group(1).strip()
        raw_input = call_match.group(2).strip()
    else:
        act_match = re.search(r"Action:\s*([a-zA-Z0-9_]+)", s, re.IGNORECASE)
        if act_match:
            action = act_match.group(1).strip()
            input_split = re.split(r"Action\s*Input:\s*", s, flags=re.IGNORECASE)
            if len(input_split) > 1:
                after_input = input_split[-1].strip()
                for kw in ["\nThought:", "\nAction:", "\nFinal Answer:"]:
                    if kw in after_input:
                        after_input = after_input.split(kw, 1)[0].strip()
                raw_input = after_input.strip()
    print(f"Parsed: action={action}, raw_input={raw_input}")
