class ReadInt():
    def __init__(self,token):
        self.token = token
    
    def to_dict(self):
        return {"type": self.token.type }  
    def evaluate(self):
        try:
            return int(input())
        except ValueError:
            raise Exception("Invalid input: expected an integer")
