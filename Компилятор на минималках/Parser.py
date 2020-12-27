from copy import deepcopy

class Tree:
    def __init__(self, value=None, childs=[]):
        self.value = value        
        self.childs = deepcopy(childs)
    
    def __str__(self, level=1):
        string = f'{self.value}\n'
        for child in self.childs:
            string += '   ' * level + child.__str__(level+1)
        return string

def parser(token_list):
    return get_program(token_list)

def get_term(token_list, expected_type):
    value, token_type = token_list[0]
    if token_type != expected_type:
        raise SyntaxError('Неверный синтаксис!') 
    del token_list[0]
    return Tree(value)

def get_group(token_list):
    current, token_type = token_list[0]
    if current == '(':
        #удаляем '('
        del token_list[0] 
        result = get_noterm(token_list)
        #удаляем ')'
        del token_list[0]
        return result
    else:
        return get_term(token_list, token_type)

def get_mult(token_list):
    result = get_group(token_list)
    current, _ = token_list[0]
    while current == '*' or current == '/':
        operator = current
        del token_list[0]
        group = get_group(token_list)
        result = Tree(operator,childs=[result,group])
        current, _ = token_list[0]
    return result

def get_add(token_list):    
    result = get_mult(token_list)
    current, _ = token_list[0]
    while current == '+' or current == '-':
        operator = current
        del token_list[0]
        mult = get_mult(token_list)
        result = Tree(operator,childs=[result,mult])
        current, _ = token_list[0]
    return result

def get_noterm(token_list):
    return get_add(token_list)

def get_expr(token_list):
    var = get_term(token_list,'VAR')
    current, _ = token_list[0]
    if current == ':=':
        del token_list[0]
        value = get_noterm(token_list)
        current, _ = token_list[0]
        if current == ";":
            del token_list[0]
            return Tree(':=',childs=[var,value])
    raise SyntaxError('Неверный синтаксис!')

def get_condition(token_list):
    current, _ = token_list[0]
    if current == '(':
        #удаляем '('
        del token_list[0]
        noterm_1 = get_noterm(token_list)
        current, _ = token_list[0]
        if current == '<' or current == '>' or current == '=':
            operator = current
            del token_list[0]
            noterm_2 = get_noterm(token_list)
            result = Tree(operator,childs=[noterm_1,noterm_2])
            current, _ = token_list[0]
            if current == ')':
                #удаляем ')'
                del token_list[0]
            else:    
                raise SyntaxError('Неверный синтаксис!')
            return result
    raise SyntaxError('Неверный синтаксис!')

def get_loop(token_list):
    current, _ = token_list[0]
    if current == 'while':
        del token_list[0]
        condition = get_condition(token_list)
        loop = Tree(current,childs=[condition])
        current, _ = token_list[0]
        while current != 'done':
            loop.childs.append(get_program_part(token_list))
            current, _ = token_list[0]
        del token_list[0]
        return loop
    raise SyntaxError('Неверный синтаксис!')        

def get_program_part(token_list):
    current, token_type = token_list[0]
    if current == 'while' or token_type == 'VAR':
        if current == 'while':
            return get_loop(token_list)
        else:
            return get_expr(token_list)
    raise SyntaxError('Неверный синтаксис!')

def get_program(token_list):
    try:
        program = Tree('Program')
        while token_list != []:
            program.childs.append(get_program_part(token_list))
        return program
    except IndexError:
        raise SyntaxError('Неверный синтаксис!')