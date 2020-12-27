from Lexer import lexer
from Parser import parser
from Generator import generator
from Optimizer import optimizer

rules = [
    (r'\b[X]{1,3}[V]?[I]{1,3}\b|\b[X]{1,3}[V]?\b|' + 
        r'\b[X]{0,3}[I][XV]\b|\b[V][I]{0,3}\b|\b[I]{1,3}\b','ROMAN_DIGIT'),
    (r'\bwhile\b','LOOP'),
    (r'\bdone\b','ENDLOOP'),
    (r'[A-Za-z][A-Za-z0-9_]*', 'VAR'),
    (r'[0-9]*\.[0-9]*', 'FLOAT'),
    (r'[1-9][0-9]*|[0]', 'INT'),
    (r'\<', 'LESS'),
    (r'\=', 'EQ'),
    (r'\>', 'LARG'),
    (r'\*', 'MPY'),
    (r'\/', 'DIV'),
    (r'\+', 'ADD'),
    (r'\-', 'SUB'),
    (r':=', 'ASSIGN'),
    (r'[\(\)]', 'GROUP'),
    (r'\;', 'END_EXPR'),
    (r'[\^\&\%\:\#\@\!\~\`\'\"\$]*','UNKNOWN')
]

if __name__ == "__main__":
    with open('input.txt') as file:
        source_code = file.read()
    id_table, token_list = lexer(source_code, rules)
    print(id_table)
    try:
        ast = parser(token_list)
        print('Дерево разбора')
        print(ast)  
        object_code = generator(ast, id_table)    
        object_code = optimizer(object_code)
        with open('object_code.txt', 'w') as file:
            file.write('\n\n'.join([''.join(command) for command in object_code]))           
    except SyntaxError as error:
        print(error)   
