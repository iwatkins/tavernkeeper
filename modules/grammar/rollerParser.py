from modules.ply import yacc, lex
import rollerLexer

tokens = rollerLexer.tokens

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('left', 'POWER'),
    ('left', 'DICE'),
)


def p_roll(p):
    """
    roll : expression
         | empty
    """
    p[0] = p[1]


def p_empty(p):
    """
    empty :
    """
    p[0] = 'empty'


def p_expression(p):
    """
    expression : INTEGER
               | parenExpression
               | binaryOperation
               | diceRoll
    """
    p[0] = p[1]


def p_paren_expression(p):
    """
    parenExpression : LPAREN expression RPAREN
    """
    p[0] = ('group', p[2])


def p_binary_operation(p):
    """
    binaryOperation : expression PLUS expression
                    | expression MINUS expression
                    | expression TIMES expression
                    | expression DIVIDE expression
                    | expression POWER expression
    """
    p[0] = ('binop', p[2], p[1], p[3])


def p_dice_roll(p):
    """
    diceRoll : expression DICE expression
    """
    p[0] = ('roll', p[1], p[3])


def p_error(p):

    print(f'Syntax error at {p.value!r}')


# Build the parser
parser = yacc.yacc()


# Parse an expression
ast = parser.parse('')
print(ast)


def parse(data, debug=0):
    parser.error = 0
    p = parser.parse(data, debug=debug)
    if parser.error:
        return None
    return p
