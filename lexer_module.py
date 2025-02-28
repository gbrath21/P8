import ply.lex as lex

tokens = (
    'GRAPH', 'NODE', 'EDGE', 'COLOR', 'FIND', 'CYCLE', 'PATH', 
    'VISUALIZE', 'IN', 'TO', 'ARROW', 'IDENTIFIER', 'STRING'
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

# SYMBOLS
t_ARROW = r'->'
t_STRING = r'"[a-zA-Z_]+"'

# IDENTIFIER - **SKAL DEFINITIONERES SIDST**
def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value in {'graph', 'node', 'edge', 'color', 'find', 'cycle', 'path', 'visualize', 'in', 'to'}:
        t.type = t.value.upper()  # Konverter til token-type
    return t

# IGNORER mellemrum & tab
t_ignore = ' \t'

# HÅNDTER NEWLINES
def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

# HÅNDTER FEJL
def t_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lineno}")
    t.lexer.skip(1)

lexer = lex.lex()