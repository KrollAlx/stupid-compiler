import re
from IdTable import IdTable

def is_duplicate(id_table, target):
    return bool(id_table.look_up(target[0]))

def lexer(characters, rules):
    index = 1
    regex_parts = []
    group_type = {}
    table = IdTable()
    for regex, token_type in rules:
        group_name = f'GROUP{index}'
        regex_parts.append(f'(?P<{group_name}>{regex})')
        group_type[group_name] = token_type
        index += 1
    regex = re.compile('|'.join(regex_parts))
    re_skip = re.compile(r'[^\s\n\r\t\}\{]')

    token_list = []
    pos = 0
    while pos < len(characters):
        match = re_skip.search(characters, pos)
        if match:
            pos = match.start()
        else:
            break
        match = regex.match(characters, pos)
        if match:
            group_name = match.lastgroup
            token_type = group_type[group_name]
            if token_type != 'UNKNOWN':
                id_table_row = (match.group(group_name), token_type)
                if not is_duplicate(table, id_table_row):
                    table.insert(id_table_row)
                token_list.append(id_table_row)
            pos = match.end()

    return (table, token_list)