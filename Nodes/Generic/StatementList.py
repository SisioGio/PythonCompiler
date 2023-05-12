class StatementList:
    def __init__(self,statements):
        self.statements = statements

    def append(self, statement):
        self.statements.append(statement)

    def __iter__(self):
        return iter(self.statements)

    def __str__(self):
        return {"Program":[(stmt.to_dict()) for stmt in self.statements]}
    
    def evaluate(self):
        for statement in self.statements:
            statement.evaluate()