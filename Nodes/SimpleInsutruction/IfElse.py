class IfElse():
    def __init__(self,token,bool_expr,simple_instr,else_simple_instr):
        self.token = token
        self.bool_expr = bool_expr
        self.simple_instr = simple_instr
        self.else_simple_instr = else_simple_instr
    
    def to_dict(self):
        return {"type":self.token.type,"operator":self.token.value,"expression" :self.bool_expr.to_dict(),"simple_instruction":self.simple_instr.to_dict(),"else_instr":self.else_simple_instr.to_dict()}
    
    def evaluate(self):
        if self.bool_expr.evaluate():
            return self.simple_instr.evaluate()
        else:
            return self.else_simple_instr.evaluate()
