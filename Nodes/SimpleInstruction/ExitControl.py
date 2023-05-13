class ExitControl():
    def __init__(self,token):
        self.token = token
    def to_dict(self):
        return { "type":self.token.type}
    def evaluate(self):
        print("Terminating process...")
        return exit()