import re
from tokens import TOKENS
# Define the token patterns using regular expressions

# Combine all the token patterns into a single regular expression
PATTERN = '|'.join('(?P<%s>%s)' % pair for pair in TOKENS)

class Lexer:
    def __init__(self, text):
        self.tokens = re.finditer(PATTERN, text)
        print(self.tokens)
        self.current_token = None

    def get_next_token(self):
            if self.current_token is None:
                self.current_token = next(self.tokens, None)
            while self.current_token is not None and self.current_token.lastindex is None:
                self.current_token = next(self.tokens, None)
            if self.current_token is None:
                return None
            token = (self.current_token.lastgroup, self.current_token.group())
            self.current_token = next(self.tokens, None)
            return token
    def __next__(self):
        if self.current_token is None:
            self.current_token = next(self.tokens, None)
            print(self.current_token)
        while self.current_token is not None and self.current_token.lastindex is None:
            self.current_token = next(self.tokens, None)
            print(self.current_token)
        if self.current_token is None:
            raise StopIteration
        token = (self.current_token.lastgroup, self.current_token.group())
        self.current_token = next(self.tokens, None)
        return token
    
input_text = """
let x = 10;
let y = 20;
print(x + y);
"""

lexer = Lexer(input_text)

# for token in lexer:
#     print(token)

token1 = next(lexer)
token2 = next(lexer)
token3 = next(lexer)
print(token1, token2, token3)
