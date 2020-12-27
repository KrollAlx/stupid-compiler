class IdTable:
    def __init__(self,n=100):
        self.tokens = [[] for i in range(n)]

    def hash_function(self,item):
        code = 0
        for symbol in item:
            code += ord(symbol)
        return code % len(self.tokens)

    def __str__(self):
        string = 'Таблица идентификаторов:\n'
        for key, item in enumerate(self.tokens):
            for row in item:
                string += f'{key} - {row[0]} - {row[1]}\n'
        return string

    def insert(self, row):
        self.tokens[self.hash_function(row[0])].append(row)

    def look_up(self, name):
        index = self.hash_function(name)
        for token_name, token_type in self.tokens[index]:
            if token_name == name:
                return (token_name, token_type)
        return tuple()