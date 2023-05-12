class Substring:
    def __init__(self, token,string, index,length):
        self.token = token
        self.string = string
        self.index = index
        self.length = length

    def to_dict(self):
        return {"type":self.token.type,"input":self.string.to_dict(),"index":self.index.to_dict(),"length":self.length.to_dict()}
    
    def evaluate(self):
        return self.string.evaluate()[self.index.evaluate():self.index.evaluate()+self.length.evaluate()]
