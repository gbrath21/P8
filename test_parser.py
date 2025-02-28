from parser import parser

test_cases = [
    "graph G",
    "node A in G",
    "node B in G",
    "edge A -> B in G",
    "visualize G"
]

for test in test_cases:
    result = parser.parse(test)
    print(f"{test} -> {result}")