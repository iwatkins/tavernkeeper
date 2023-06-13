import random
import rollerParser

max_dice = 1000
max_sides = 1000


# Rolls dice based on number of dice, number of sides per die, and number of rolls to keep.
def roll(dice, sides, keep, print_rolls=0):
    if dice > max_dice:
        print(f'Invalid number of dice: {dice}.')
        return 0
    elif sides < 1 or sides > max_sides:
        print(f'Invalid number of sides: {sides}.')
        return 0
    elif keep < 0 or keep > abs(dice):
        print(f'Invalid number of dice to keep: {keep}.')
        return 0

    multiplier = 1
    if dice < 0:
        print('Warning: (-x)dy will be treated as -(xdy).')
        multiplier = -1

    rolls = [random.randint(1, sides) for _ in range(abs(dice))]
    rolls.sort(reverse=True)
    final_rolls = rolls[:keep]
    if print_rolls:
        print(f'Roll: {rolls}')
        print(f'Keep: {final_rolls}')
    return multiplier * sum(final_rolls)


# A simple DFS that processes the abstract syntax tree, returning int values for each node.
def resolve(node) -> int:
    # A single character string cannot be processed. This can happen for single digit ints.
    if len(node) < 2:
        return int(node)

    match node[0], node[1]:
        case 'empty', _:
            print('No roll specified')
            return 0
        case 'uminus', _:
            return -1 * resolve(node[1])
        case 'group', _:
            return resolve(node[1])
        case 'binop', '+':
            return resolve(node[2]) + resolve(node[3])
        case 'binop', '-':
            return resolve(node[2]) - resolve(node[3])
        case 'binop', '*':
            return resolve(node[2]) * resolve(node[3])
        case 'binop', '/':
            return resolve(node[2]) // resolve(node[3])
        case 'binop', '^':
            return int(pow(resolve(node[2]), resolve(node[3])))
        case 'roll', _:
            return roll(resolve(node[1]), resolve(node[2]), resolve(node[3]))
        case _, _:
            return int(node)


# Run the lexer, parser, and resolver for a given data string.
def run(data, seed=None, print_tree=0, debug=0):
    ast = rollerParser.parse(data, debug)
    if None:
        return None
    if print_tree:
        print(ast)
    random.seed(seed)
    return resolve(ast)
