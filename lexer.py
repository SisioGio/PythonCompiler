import re
from tokens import TOKENS
import itertools
from Nodes.Generic.Token import Token
# Define the token patterns using regular expressions

# Combine all the token patterns into a single regular expression
PATTERN = '|'.join('(?P<%s>%s)' % pair for pair in TOKENS)

class Lexer:
    def __init__(self, text):
        self.tokens = list(re.finditer(PATTERN, text))
        self.current_token_index = 0
        self.current_token = None

    def consume(self):
        if(self.current_token_index < len(self.tokens)):
            next_token = self.tokens[self.current_token_index]
            self.current_token_index += 1
            token = Token(next_token.lastgroup,next_token.group())
           
            self.current_token = token
            return self.current_token
        else:
            token = Token("EOF",'END OF FILE')
            self.current_token = token
            return self.current_token
    
    def peek(self):
        if(self.current_token_index < len(self.tokens)):

            next_token = self.tokens[self.current_token_index]
            token = Token(next_token.lastgroup,next_token.group())
            return token
        token = Token("EOF",'END OF FILE')
        self.current_token = token
        return self.current_token



# lexer = Lexer("2 + 4")

# lexer.consume()
# lexer.consume()
# lexer.consume()
# lexer.consume()