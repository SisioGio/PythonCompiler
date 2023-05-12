class Position:
    def __init__(self, token, input_expr,sub_expr):
        self.token = token
        self.input_expr = input_expr
        self.sub_expr = sub_expr

    def to_dict(self):
        return {"type":self.token.type,"input_string":self.input_expr.to_dict(),"sub_string":self.sub_expr.to_dict()}
    def evaluate(self):
        return self.input_expr.evaluate().find(self.sub_expr.evaluate())
