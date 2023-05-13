class PrintStatement():
    def __init__(self,token, value):
        self.token = token
        self.value = value

    
    def to_dict(self):
        return {"type": "PRINT", "output":self.value.to_dict()}    
    def evaluate(self):
        print(self.value.evaluate())
        return None