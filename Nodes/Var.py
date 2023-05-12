class Var:
    def __init__(self, token,value):
        self.name = token.value
        self.value = value
        self.type = token.type
    def to_dict(self):
        return {"type": self.type, "name":self.name,"value":self.value.to_dict() }
    def evaluate(self):
        return self.value.evaluate()