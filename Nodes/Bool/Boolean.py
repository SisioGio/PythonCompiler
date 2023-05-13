class Boolean():
    def __init__(self,token):
        self.token = token
        self.value = token.value.lower() == 'true'
    
    def to_dict(self):
        return {"type":self.token.type,"value":self.value}
    
    def evaluate(self):
        return self.value