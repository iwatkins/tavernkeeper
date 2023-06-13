from modules.ply import yacc
import rollerLexer

# Parses a stream of tokens into an abstract syntax tree, representing their meaning.
tokens = rollerLexer.tokens

# Defines precedence of certain operators. All groups are of the same precedence, and are left or right-associative.
# The groups are ordered by precedence, from low to high.
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('left', 'UMINUS'),
    ('left', 'POWER'),
    ('right', 'DICE', 'KEEP'),
)


# Parsing rules, or the rules of our grammar.
# They are of the form "term : meaning", where a "term" is a single non-terminal,
# and "meaning" is a series of terminals or non-terminals.
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
    p[0] = ('empty', None)


def p_expression(p):
    """
    expression : INTEGER
               | unaryMinus
               | parenExpression
               | binaryOperation
               | diceRoll
    """
    p[0] = p[1]


def p_unary_minus(p):
    """
    unaryMinus : MINUS expression %prec UMINUS
    """
    p[0] = ('uminus', p[2])


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
    diceRoll : expression DICE expression KEEP expression
             | expression DICE expression
    """
    if len(p) == 6:
        p[0] = ('roll', p[1], p[3], p[5])
    else:
        p[0] = ('roll', p[1], p[3], p[1])


def p_error(p):

    print(f'Syntax error at {p.value!r}')


# Run the parser.
parser = yacc.yacc()


def parse(data, debug=0):
    parser.error = 0
    p = parser.parse(data, debug=debug)
    if parser.error:
        return None
    return p
