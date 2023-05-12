class Length:
    def __init__(self,token, expr):
        self.expr = expr
        self.token = token
    def to_dict(self):
        return {"type":self.token.type,"input":self.expr.to_dict()}

    def evaluate(self):
        value = self.expr.evaluate()
        if not isinstance(value, str):
            raise Exception("Argument to LENGTH must be a string")
        return len(value)
