from lexer_module import lexer  # Sørg for, at vi bruger det rigtige modul

code = """
graph G
node A in G
node B in G
edge A -> B in G
visualize G
"""

lexer.input(code)

for token in lexer:
    print(token)
