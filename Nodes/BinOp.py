class BinOp:
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right
    def to_dict(self):
        return {"type": self.token.type, "left":self.left.to_dict(),"op":self.token.value,"right":self.right.to_dict() }    
    def evaluate(self):
        if self.token.type == "PLUS":
            return self.left.evaluate() + self.right.evaluate()
        elif self.token.type  =="MINUS":
            return self.left.evaluate() - self.right.evaluate()
        elif self.token.type == "MULT":
            return self.left.evaluate() * self.right.evaluate()
        elif self.token.type == "DIV":
            return self.left.evaluate() / self.right.evaluate()
        elif self.token.type == "MODULO":
            return self.left.evaluate() % self.right.evaluate()