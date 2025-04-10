import ply.yacc as yacc
from lexer_module import tokens  # Importer tokens fra lexeren

# abstract syntax tree struktur
def p_statement_node(p):
    'statement : NODE IDENTIFIER IN IDENTIFIER'
    p[0] = ('node', p[2], p[4])

def p_statement_directed_graph(p):
    'statement : GRAPH IDENTIFIER DIRECTED'
    p[0] = ('directed_graph', p[2])

def p_statement_graph(p):
    'statement : GRAPH IDENTIFIER'
    p[0] = ('graph', p[2])

def p_statement_weighted_edge(p):
    'statement : EDGE IDENTIFIER ARROW IDENTIFIER WEIGHT NUMBER IN IDENTIFIER'
    p[0] = ('edge', p[2], p[4], p[8], p[6])

def p_statement_edge(p):
    'statement : EDGE IDENTIFIER ARROW IDENTIFIER IN IDENTIFIER'
    p[0] = ('edge', p[2], p[4], p[6], 1)

def p_statement_visualize(p):
    'statement : VISUALIZE IDENTIFIER'
    p[0] = ('visualize', p[2])

def p_statement_find_cycle(p):
    'statement : FIND CYCLE IN IDENTIFIER'
    p[0] = ('find_cycle', p[4])
    
def p_statement_shortest_path(p):
    'statement : FIND PATH IDENTIFIER TO IDENTIFIER IN IDENTIFIER'
    p[0] = ('shortest_path', p[3], p[5], p[7])
    
def p_statement_color_node(p):
    'statement : COLOR NODE IDENTIFIER STRING'
    p[0] = ('color_node', p[3], p[4])

def p_statement_color_edge(p):
    'statement : COLOR EDGE IDENTIFIER ARROW IDENTIFIER STRING'
    p[0] = ('color_edge', p[3], p[5], p[6])

def p_statement_delete_node(p):
    'statement : DELETE1 NODE IDENTIFIER FROM IDENTIFIER'
    p[0] = ('delete1_node', p[3], p[5])

def p_statement_delete_edge(p):
    'statement : DELETE1 EDGE IDENTIFIER ARROW IDENTIFIER FROM IDENTIFIER'
    p[0] = ('delete1_edge', p[3], p[5], p[7])

def p_statement_save_graph(p):
    'statement : SAVE GRAPH IDENTIFIER TO STRING'
    p[0] = ('save_graph', p[3], p[5].strip('"'))

def p_statement_load_graph(p):
    'statement : LOAD GRAPH IDENTIFIER FROM STRING'
    p[0] = ('load_graph', p[3], p[5].strip('"'))
    
def p_statement_find_mst(p):
    'statement : FIND MST IN IDENTIFIER'
    p[0] = ('find_mst', p[4])

def p_statement_if_node(p):
    'statement : IF NODE IDENTIFIER IN IDENTIFIER THEN statement'
    p[0] = ('if_node', p[3], p[5], p[7])

def p_statement_if_edge(p):
    'statement : IF EDGE IDENTIFIER ARROW IDENTIFIER IN IDENTIFIER THEN statement'
    p[0] = ('if_edge', p[3], p[5], p[7], p[9])

def p_statement_if_path(p):
    'statement : IF PATH IDENTIFIER TO IDENTIFIER IN IDENTIFIER THEN statement'
    p[0] = ('if_path', p[3], p[5], p[7], p[9])

def p_statement_if_cycle(p):
    'statement : IF FIND CYCLE IN IDENTIFIER THEN statement'
    p[0] = ('if_cycle', p[5], p[7])
    
# def p_statement_if_not_node(p):
#     'statement : IF NOT NODE IDENTIFIER IN IDENTIFIER THEN statement'
#     p[0] = ('if_not_node', p[4], p[6], p[8])

# def p_statement_if_not_edge(p):
#     'statement : IF NOT EDGE IDENTIFIER ARROW IDENTIFIER IN IDENTIFIER THEN statement'
#     p[0] = ('if_not_edge', p[4], p[6], p[8], p[10])

# def p_statement_if_not_path(p):
#     'statement : IF NOT PATH IDENTIFIER TO IDENTIFIER IN IDENTIFIER THEN statement'
#     p[0] = ('if_not_path', p[4], p[6], p[8], p[10])

# def p_statement_if_not_cycle(p):
#     'statement : IF NOT FIND CYCLE IN IDENTIFIER THEN statement'
#     p[0] = ('if_not_cycle', p[6], p[8])
    
def p_statement_closure(p):
    'statement : CLOSURE closure_type IN IDENTIFIER'
    p[0] = ('closure', p[2], p[4])

def p_closure_type(p):
    '''closure_type : REFLEXIVE
                    | SYMMETRIC
                    | TRANSITIVE'''
    p[0] = p[1]

def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}', line {p.lineno}")
    else:
        print("Syntax error at end of input")

parser = yacc.yacc()