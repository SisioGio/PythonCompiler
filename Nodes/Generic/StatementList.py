class StatementList:
    def __init__(self,statements,name):
        self.statements = statements
        self.name= name

    def append(self, statement):
        self.statements.append(statement)

    def __iter__(self):
        return iter(self.statements)

    def to_dict(self):
        return {self.name:[(stmt.to_dict()) for stmt in self.statements]}
    
    def evaluate(self):
        for statement in self.statements:
            statement.evaluate()