from copy import deepcopy

def optimizer(commands_list):
    return second_optimize(first_optimize(commands_list))

def first_optimize(commands_list):
    intermediate_list = deepcopy(commands_list)
    deleted_commands = 0
    for i in range(len(commands_list)):
        if len(commands_list[i]) > 1:
            value = commands_list[i][1]            
            if next_command_name(commands_list, i) == 'STORE ' and next_value(commands_list, i).startswith('$'):
                temp_var = commands_list[i + 1][1]
                match_index = find_var(intermediate_list, temp_var)
                intermediate_list[match_index][1] = value                
                del intermediate_list[i - deleted_commands]
                del intermediate_list[i - deleted_commands]
                deleted_commands += 2
    return intermediate_list

def second_optimize(intermediate_list):
    optimal_commands_list = deepcopy(intermediate_list)
    deleted_commands = 0
    for i in range(len(intermediate_list)):
        if len(intermediate_list[i]) > 1:
            command_name, value = intermediate_list[i]
            if command_name == 'STORE ' and next_command_name(intermediate_list, i) == 'LOAD ' \
                and value == next_value(intermediate_list, i):                
                del optimal_commands_list[i - deleted_commands + 1]
                deleted_commands += 2               
    return optimal_commands_list

def next_command_name(commands_list, index):
    return commands_list[index + 1][0] if index + 1 < len(commands_list) else ''

def next_value(commands_list, index):
    return commands_list[index + 1][1] if index + 1 < len(commands_list) else ''

def find_var(commands_list, var):
    for i in range(len(commands_list)):
        if len(commands_list[i]) > 1:
            command_name, value = commands_list[i]
            if command_name in {'ADD ','MPY ','SUB ','DIV ','LARG ','EQ ','LESS '} and value == var:
                return i
        