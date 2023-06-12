import rollerParser

data = '123+4^6'

ast = rollerParser.parse(data)

print(ast)


def resolve(node) -> int:
    match node[0]:
        case 'empty':
            print('No roll specified')
            return 0
        case 'group':
            return resolve(node[1])
        case 'binop':
            match node[1]:
                case '+':
                    return resolve(node[2]) + resolve(node[3])
                case '-':
                    return resolve(node[2]) - resolve(node[3])
                case '*':
                    return resolve(node[2]) * resolve(node[3])
                case '/':
                    return resolve(node[2]) // resolve(node[3])
                case '^':
                    return pow(resolve(node[2]), resolve(node[3]))
        case 'roll':
            return 0
        case _:
            return int(node[0])


print(resolve(ast))
