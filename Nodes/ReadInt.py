class ReadInt():
    def __init__(self,token):
        self.token = token
    
    def to_dict(self):
        return {"type": self.token.type }  
    def evaluate(self):
        try:
            return int(input("\nEnter an integer value and press Enter:\n"))
        except ValueError:
            raise Exception("Invalid input: expected an integer")
