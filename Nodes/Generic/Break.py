class Break:
    def __init__(self, token):
        self.token = token
    def to_dict(self):
        return {"type": self.token.type }    
    def evalute(self):
        return None