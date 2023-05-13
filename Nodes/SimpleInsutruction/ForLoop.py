class ForLoop():
    def __init__(self,token,iterator,limit,instr):
        self.token = token
        self.iterator = iterator
        self.limit = limit
        self.instr = instr
    
    def to_dict(self):
        return {"type":self.token.type,"iterator":self.iterator.to_dict(),"limit" :self.limit.to_dict(),"instr":self.instr.to_dict()}
    
    def evaluate(self):
        for i in range(self.iterator.evaluate(),self.limit.evaluate()):
            # self.iterator.increase_by(1)
            if self.instr.token.type == "BREAK":
                break
            else:
                self.instr.evaluate()
      
