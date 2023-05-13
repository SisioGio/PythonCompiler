class Not():
    def __init__(self,token,bool_expr):
        self.token = token
        self.bool_expr = bool_expr
    
    def to_dict(self):
        return {"type":self.token.type,"expression":self.bool_expr.to_dict()}
    
    def evaluate(self):
        return not self.bool_expr.evaluate()