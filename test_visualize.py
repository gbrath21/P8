from interpreter import run_gml

test_code = """
graph G
node A in G
node B in G
node C in G
edge A -> B in G
edge B -> C in G
edge A -> C in G
color node A "red"
color node B "green"
color node C "blue"
color edge A -> B "purple"
color edge B -> C "orange"
visualize G
"""

run_gml(test_code)
