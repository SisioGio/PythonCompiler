import sys
from io import StringIO
class ReadStr():
    def __init__(self,token):
        self.token = token
    
    def to_dict(self):
        return {"type": self.token.type }  
    def evaluate(self):
        try:
            user_input = input()
            return user_input
        
        except ValueError as e:
            
            raise Exception("Invalid input: expected a string")
        
