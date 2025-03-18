from interpreter import run_gml

test_code = """
graph G
node A in G
node B in G
node C in G
node D in G
edge A -> B in G
edge B -> C in G
edge C -> D in G
find path A to D in G
"""

run_gml(test_code)