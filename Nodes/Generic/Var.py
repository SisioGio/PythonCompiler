class Var:
    def __init__(self, token,value):
        self.name = token.value
        self.value = value.evaluate()
        self.type = token.type
        self.children = value
    def to_dict(self):
        return {"type": self.type, "name":self.name,"value":self.value,"children":self.children.to_dict() }
    def evaluate(self):
        return self.value
    def increase_by(self,i):
        self.value = self.value + i