class UnaryOp():
    def __init__(self, token, expr):
        self.token = token
        self.expr = expr

    def __repr__(self):
        return f"{self.token}, {self.expr}"

    def evaluate(self):
        if self.token.type == "PLUS":
            return +self.expr.evaluate()
        elif self.token.type == "MINUS":
            return -self.expr.evaluate()
    def to_dict(self):
        return {"type": self.token.type, "expression":self.expr.to_dict() }        
