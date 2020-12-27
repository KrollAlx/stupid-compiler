from IdTable import IdTable
from operator import add
from functools import reduce
from itertools import zip_longest

def generator(tree, id_table):
    command_list = []
    for child in tree.childs:        
        command_list += get_commands_list(child, id_table, 1)
    return command_list

def get_commands_list(tree, id_table, level):
    value, value_type = id_table.look_up(tree.value)
    if value == ':=':
        command_list = get_commands_list(tree.childs[1], id_table, level+1) + \
            [['STORE ', tree.childs[0].value]]
    elif value in {'*','+','-','/'}:
        command_list = get_operation_code(tree, id_table, value_type, level)            
    elif value_type == 'VAR':
        command_list = [['LOAD ' , value]]
    elif value_type == 'INT' or value_type == 'FLOAT':
        command_list = [['LOAD ', f'={value}']]
    elif value_type == 'ROMAN_DIGIT':
        command_list = [['LOAD ', f'={to_arabic(value)}']]
    elif value_type == 'LOOP':
        command_list = get_loop_code(tree, id_table, level)
    return command_list       
     
def get_operation_code(tree, id_table, operator, level):
    return get_commands_list(tree.childs[1], id_table, level+1) + \
            [['STORE ',f'${level}']] + get_commands_list(tree.childs[0], id_table, level+1) + \
            [[f'{operator} ', f'${level}']]

def to_arabic(rom_digit):
    digits = {'I':1,'V':5,'X':10}
    if rom_digit:
        return reduce(add, ((-digits[x], digits[x]) 
                [y is None or digits[x]>=digits[y]] for x, y in zip_longest(rom_digit,rom_digit[1:])))

def get_loop_code(tree, id_table, level):
    _, operator = id_table.look_up(tree.childs[0].value)
    condition_code = [['CONDITION:']] + get_operation_code(tree.childs[0], id_table, operator, level)
    commands_list = condition_code + [['CMP ', '1'],['JMPE ', 'START_LOOP'],['JMP ', 'END_LOOP'],['START_LOOP:']]
    for child in tree.childs[1:]:
        commands_list += get_commands_list(child, id_table, level)
    return commands_list + [['JMP ', 'CONDITION'],['END_LOOP:']]