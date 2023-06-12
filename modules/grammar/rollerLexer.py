from modules.ply import lex

tokens = ('PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'LPAREN', 'RPAREN', 'INTEGER', 'POWER', 'DICE')

t_ignore = ' \t\r\n'


def t_ignore_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count('\n')


t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_INTEGER = r'\d+'
t_POWER = r'\^'
t_DICE = r'[dD]'


def t_error(t):
    print("Illegal character %s" % t.value[0])
    t.lexer.skip(1)


lex.lex(debug=0)

