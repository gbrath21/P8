from lexer_module import lexer

# code = """
# delete1 node A from G
# delete1 edge A -> B from G
# """

# lexer.input(code)

# for token in lexer:
#     print(token)


# code = """
# edge A -> B weight 5 in G
# """

# lexer.input(code)

# for token in lexer:
#     print(token)


code = """
graph G
node A in G
node B in G
edge A -> B weight 10 in G
node C in G
edge B -> C weight 5 in G
visualize G
"""

lexer.input(code)

for token in lexer:
    print(token)
