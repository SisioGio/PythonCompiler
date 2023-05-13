class Or():
    def __init__(self,token,left,right):
        self.token = token
        self.left = left
        self.right = right
    
    def to_dict(self):
        return {"type":self.token.type,"left":self.left.to_dict(),"right":self.right.to_dict()}
    
    def evaluate(self):
        return self.left.evaluate() | self.right.evaluate()