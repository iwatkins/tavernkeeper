from modules.ply import lex

# Lexes a stream of characters into a stream of tokens.
# The words of our grammar. All inputs should match to one of these items.
tokens = (
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'LPAREN',
    'RPAREN',
    'INTEGER',
    'POWER',
    'DICE',
    'KEEP',
)

# Ignore all whitespace
t_ignore = ' \t\r\n'


def t_ignore_newline(t):
    r"""\n+"""
    t.lexer.lineno += t.value.count('\n')


# Regex definitions of our words.
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_INTEGER = r'\d+'
t_POWER = r'\^'
t_DICE = r'[dD]'
t_KEEP = r'[kK]'


# Error out if an unexpected word is encountered.
def t_error(t):
    print("Illegal character %s" % t.value[0])
    t.lexer.skip(1)


# Run the lexer.
lex.lex(debug=0)
