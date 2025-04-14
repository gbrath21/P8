from interpreter import run_gml

test_code = """
graph G
node A in G
node B in G
node C in G
edge A -> B in G
edge B -> C in G
edge C -> A in G
find cycle in G
"""

run_gml(test_code)