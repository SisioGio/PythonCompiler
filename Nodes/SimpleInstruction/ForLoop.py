from Nodes.SimpleInstruction.BreakControl import BreakControl
from Nodes.SimpleInstruction.ContinueControl import ContinueControl
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
            output = self.instr.evaluate()
            if type(output) == BreakControl:
                print("break")
                break
            elif type(output) == ContinueControl:
                
                self.iterator.increase_by(1)
                continue
            else:
                output

            self.iterator.increase_by(1)
      
