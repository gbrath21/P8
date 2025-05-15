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

def p_statement_bfs(p):
    'statement : FIND BFS FROM IDENTIFIER IN IDENTIFIER'
    p[0] = ('find_bfs', p[4], p[6])

def p_statement_dfs(p):
    'statement : FIND DFS FROM IDENTIFIER IN IDENTIFIER'
    p[0] = ('find_dfs', p[4], p[6])

def p_statement_find_mst(p):
    'statement : FIND MST IN IDENTIFIER'
    p[0] = ('find_mst', p[4])

def p_statement_color_node(p):
    'statement : COLOR NODE IDENTIFIER STRING'
    p[0] = ('color_node', p[3], p[4])

def p_statement_remove_node(p):
    'statement : REMOVE NODE IDENTIFIER FROM IDENTIFIER'
    p[0] = ('remove_node', p[3], p[5])

def p_statement_remove_edge(p):
    'statement : REMOVE EDGE IDENTIFIER ARROW IDENTIFIER FROM IDENTIFIER'
    p[0] = ('remove_edge', p[3], p[5], p[7])

def p_statement_save_graph(p):
    'statement : SAVE GRAPH IDENTIFIER TO STRING'
    p[0] = ('save_graph', p[3], p[5].strip('"'))

def p_statement_load_graph(p):
    'statement : LOAD GRAPH IDENTIFIER FROM STRING'
    p[0] = ('load_graph', p[3], p[5].strip('"'))

def p_statement_if(p):
    'statement : IF condition THEN statement'
    p[0] = ('if_cond', p[2], p[4])

def p_condition_base(p):
    '''condition : NODE IDENTIFIER IN IDENTIFIER
                 | EDGE IDENTIFIER ARROW IDENTIFIER IN IDENTIFIER
                 | PATH IDENTIFIER TO IDENTIFIER IN IDENTIFIER
                 | FIND CYCLE IN IDENTIFIER
                 | NOT NODE IDENTIFIER IN IDENTIFIER
                 | NOT EDGE IDENTIFIER ARROW IDENTIFIER IN IDENTIFIER
                 | NOT PATH IDENTIFIER TO IDENTIFIER IN IDENTIFIER
                 | NOT FIND CYCLE IN IDENTIFIER'''
    p[0] = ('cond',) + tuple(p[1:])

def p_condition_and(p):
    'condition : condition AND condition'
    p[0] = ('and', p[1], p[3])

def p_condition_or(p):
    'condition : condition OR condition'
    p[0] = ('or', p[1], p[3])

def p_condition_edge_weight(p):
    '''condition : WEIGHT OF EDGE IDENTIFIER ARROW IDENTIFIER IS GREATER THAN NUMBER IN IDENTIFIER'''
    p[0] = ('cond', 'weight', p[4], p[6], p[10], p[12]) 

def p_statement_closure(p):
    'statement : CLOSURE closure_type IN IDENTIFIER'
    p[0] = ('closure', p[2], p[4])

def p_closure_type(p):
    '''closure_type : REFLEXIVE
                    | SYMMETRIC
                    | TRANSITIVE'''
    p[0] = p[1]

def p_statement_loop_node(p):
    'statement : LOOP NODE IDENTIFIER IN IDENTIFIER block'
    p[0] = ('loop_node', p[3], p[5], p[6])

def p_statement_loop_edge(p):
    'statement : LOOP EDGE IDENTIFIER ARROW IDENTIFIER IN IDENTIFIER block'
    p[0] = ('loop_edge', p[3], p[5], p[7], p[8])

def p_statement_loop_times(p):
    'statement : LOOP FROM NUMBER TO NUMBER block'
    p[0] = ('loop_times', p[3], p[5], p[6])

def p_statement_loop_from_to_in_graph(p):
    'statement : LOOP IDENTIFIER FROM NUMBER TO NUMBER IN IDENTIFIER block'
    p[0] = ('loop_graph_range', p[2], p[4], p[6], p[8], p[9])

def p_statement_loop_edge_from_to_in_graph(p):
    'statement : LOOP EDGE IDENTIFIER ARROW IDENTIFIER FROM NUMBER TO NUMBER IN IDENTIFIER block'
    p[0] = ('loop_edge_range', p[3], p[5], p[7], p[9], p[11], p[12])

def p_statement_add_weight(p):
    'statement : ADD NUMBER TO WEIGHT OF EDGE IDENTIFIER ARROW IDENTIFIER IN IDENTIFIER'
    p[0] = ('add_weight', p[2], p[7], p[9], p[11])

def p_block_multiple(p):
    'block : statement block'
    p[0] = [p[1]] + p[2]

def p_block_single(p):
    'block : statement'
    p[0] = [p[1]]

def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}', line {p.lineno}")
    else:
        print("Syntax error at end of input")

parser = yacc.yacc()