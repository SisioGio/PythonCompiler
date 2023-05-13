class Boolean():
    def __init__(self,token):
        self.token = token
        self.value = bool(token.value)
    
    def to_dict(self):
        return {"type":self.token.type,"value":self.value}
    
    def evaluate(self):
        return self.value