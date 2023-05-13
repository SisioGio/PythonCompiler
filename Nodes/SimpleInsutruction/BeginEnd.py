class BeginEnd():
    def __init__(self,token,instrs):
        self.token = token
        self.instrs = instrs
    
    def to_dict(self):
        return {"type":self.token.type,"instructions":self.instrs.to_dict()}
    
    def evaluate(self):
        self.instrs.evaluate()
      
