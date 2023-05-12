class String:
    def __init__(self, token):
        self.value = token.value.replace('"',"")
        self.type =token.type
    def to_dict(self):
        return {"type":self.type,"value":self.value}
    def evaluate(self):
        return self.value