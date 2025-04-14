import ply.lex as lex

# Definer tokens
tokens = (
    'GRAPH', 'NODE', 'EDGE', 'COLOR', 'FIND', 'CYCLE', 'PATH',
    'VISUALIZE', 'IN', 'TO', 'ARROW', 'NUMBER', 'IDENTIFIER', 'STRING',
    'DELETE1', 'FROM', 'WEIGHT', 'DIRECTED', 'SAVE', 'LOAD', 'MST', 'IF', 'THEN',
    'CLOSURE', 'REFLEXIVE', 'SYMMETRIC', 'TRANSITIVE', 'LOOP', 'BFS', 'DFS', 'ADD', 'OF', 'NOT'
)

# KEYWORDS
t_GRAPH = r'graph'
t_NODE = r'node'
t_EDGE = r'edge'
t_COLOR = r'color'
t_FIND = r'find'
t_CYCLE = r'cycle'
t_PATH = r'path'
t_VISUALIZE = r'visualize'
t_IN = r'in'
t_TO = r'to'
t_DELETE1 = r'delete1'
t_FROM = r'from'
t_WEIGHT = r'weight'
t_DIRECTED = r'directed'
t_SAVE = r'save'
t_LOAD = r'load'
t_MST = r'mst'
t_IF = r'if'
t_THEN = r'then'
t_CLOSURE = r'closure'
t_REFLEXIVE = r'reflexive'
t_SYMMETRIC = r'symmetric'
t_TRANSITIVE = r'transitive'
t_LOOP = r'loop'
t_BFS = r'bfs'
t_DFS = r'dfs'
t_ADD = r'add'
t_OF = r'of'
t_NOT = r'not'

# SYMBOLS
t_ARROW = r'->'
t_STRING = r'"[^"]*"'

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*' # Regular expression describing variable names (see SPO lec1)
    if t.value in {'graph', 'node', 'edge', 'color', 'find', 'cycle', 'path', 'visualize',
                    'in', 'to', 'delete1', 'from', 'weight', 'directed', 'save', 'load',
                    'mst', 'shortest', 'if', 'then', 'closure', 'transitive', 'symmetric', 'reflexive',
                    'loop', 'bfs', 'dfs', 'not', 'add', 'of'}:
        t.type = t.value.upper()  # Convert to token type
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)  # Convert to an int
    return t

def t_comment(t):
    r'\#.*'
    pass  # Ignore comments #

# Ignore space and tab
t_ignore = ' \t'

# Handle newlines
def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

# Handle syntax errors
def t_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lineno}")
    t.lexer.skip(1)

lexer = lex.lex()