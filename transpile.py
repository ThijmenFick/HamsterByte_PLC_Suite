from lark import Lark
import json

def parse_tree(lines):
    root = {}
    stack = [(root, -1)]  # (current_dict, indent_level)

    for line in lines:
        if not line.strip():
            continue

        indent = len(line) - len(line.lstrip())
        key_value = line.strip().split("\t")

        # Handle key + optional value
        key = key_value[0]
        value = key_value[1] if len(key_value) > 1 else None

        # Move up the stack until indent matches
        while stack and stack[-1][1] >= indent:
            stack.pop()

        parent, _ = stack[-1]

        # If key already exists, turn it into a list
        if key in parent:
            if not isinstance(parent[key], list):
                parent[key] = [parent[key]]
            entry = {} if value is None else value
            parent[key].append(entry)
            if isinstance(entry, dict):
                stack.append((entry, indent))
        else:
            if value is None:
                parent[key] = {}
                stack.append((parent[key], indent))
            else:
                # Convert booleans and integers
                if value in ("TRUE", "true"):
                    parent[key] = True
                elif value in ("FALSE", "false"):
                    parent[key] = False
                elif value.isdigit():
                    parent[key] = int(value)
                else:
                    parent[key] = value

    return root

with open("grammar.lark", "r", encoding="utf-8") as f:
    grammar = f.read()

parser = Lark(grammar, start="start", parser="earley")

with open("code.txt", "r", encoding="utf-8") as f:
    code = f.read()

tree = parser.parse(code)

with open("output.txt", "w", encoding="utf-8") as f:
    f.write(tree.pretty())

with open("output.json", "w", encoding="utf-8") as of:
    with open("output.txt", "r", encoding="utf-8") as f:
        lines = f.read().splitlines()
        parsed = parse_tree(lines)
        of.write(json.dumps(parsed, indent=2))