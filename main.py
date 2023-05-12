from Nodes.BinOp import BinOp
from Nodes.Num import Num
from Nodes.Var import Var
from Nodes.ReadInt import ReadInt
from Nodes.String import String
from Nodes.Length import Length
from Nodes.Position import Position
from Nodes.ReadStr import ReadStr
from Nodes.UnaryOp import UnaryOp
from lexerTest import Lexer
from Nodes.PrintStatement import PrintStatement
from Nodes.StatementList import StatementList
class Parser:
    def __init__(self, input):
        self.lexer = Lexer(input)
        self.current_token = None
        self.vars = {}
        self.advance()


    def advance(self):
        try:
            self.current_token = self.lexer.consume()
        except Exception:
            self.current_token = None



    def let_statement(self):
        # Parse a let statement and return an abstract syntax tree node
        # representing the statement
        pass

    def print_statement(self):
        # Parse a print statement and return an abstract syntax tree node
        # representing the statement
        pass

    def error(self, expected_token_type):
        raise Exception(f"Syntax error: expected {expected_token_type}, got {self.current_token.type} ({self.current_token.value})")
    
    def parse(self):
            """
            Parse the input and return an abstract syntax tree (AST).
            """

            ast = self.program()
            if not self.current_token is None:
                if self.current_token.type != "EOF":
                    self.error("EOF")
            return ast
    def program(self):
        node = self.statement_list()
        return node
    
    def statement_list(self):
        statements = []
        statement = self.statement()
        statements.append(statement)
        # if not self.current_token is None:
        while self.current_token.type == "SEMICOLON":
            self.eat("SEMICOLON")
            next_statement = self.statement()
            if not next_statement is None:
                statements.append(next_statement)
        return StatementList(statements)

    def statement(self):
        token_type  = self.current_token.type
        
        if token_type == "PRINT":
            return self.parse_print_statement()
        elif token_type == "IDENT":
            return self.parse_ident_statement()
        elif self.current_token.type == "EOF":
            return None
        else:
            return None

    def eat(self,token_type):
        if(self.current_token.type ==token_type):
            self.current_token = self.lexer.consume()
        else:
            raise SyntaxError(f"Invalid syntax, expected :{token_type} got {self.current_token.type}")

    
    def parse_print_statement(self):
        self.eat("PRINT")
        self.eat("LPAREN")
        value = self.expr()
        self.eat("RPAREN")
        return PrintStatement(value)
    
    def parse_ident_statement(self):
        
        node = self.current_token
        self.eat("IDENT")
        self.eat("ASSIGN")
        
        value =  self.expr()
        var = Var(node,value)
        self.vars[node.value] = var
        return var

    def expr(self):
        left = self.term()
        while self.current_token.type in ("PLUS", "MINUS"):
            op = self.current_token
            if op.type == "PLUS":
                self.eat("PLUS")
            elif op.type == "MINUS":
                self.eat("MINUS")
            right = self.term()
            left = BinOp(left, op, right)
        return left

    def term(self):
        left = self.factor()
        while self.current_token.type in ("MULT", "DIV","MODULO"):
            op = self.current_token
            if op.type == "MULT":
                self.eat("MULT")
            elif op.type == "DIV":
                self.eat("DIV")
            elif op.type == "MODULO":
                self.eat("MODULO")
            right = self.factor()
            left = BinOp(left, op, right)
        return left

    def factor(self):
        if self.current_token.type == "LPAREN":
            self.eat("LPAREN")
            expr = self.expr()
            self.eat("RPAREN")
            return expr
        elif self.current_token.type == "NUM":
            node = Num(self.current_token)
            self.eat("NUM")
            return node
        elif self.current_token.type == "IDENT":
            # Get variable from 'vars' dict
            node = self.get_variable()
            self.eat("IDENT")
            return node.value
        elif self.current_token.type == "READINT":
            node = ReadInt(self.current_token)
            self.eat("READINT")
            return node
        elif self.current_token.type == "MINUS":
            negation_node = self.current_token
            self.eat("MINUS")
            
            expr= self.factor()
            node = UnaryOp(negation_node,expr)
            return node
        elif self.current_token.type == "LENGTH":
            length_node = self.current_token
            self.eat("LENGTH")
            self.eat("LPAREN")
            node = self.str_expr()
            self.eat("RPAREN")
            return Length(length_node,node)
        else:
            raise SyntaxError("Invalid syntax")
    
    def get_variable(self):
        if(not self.current_token.value in self.vars):
            # Variable does not exist
            self.error(f"Undefined variable '{self.current_token.value}'")

        
        return self.vars[self.current_token.value]
    # # grammar rules for numerical expressions
    # def num_expr(self):
    #     node = self.t_num_expr()

    #     while self.current_token.type in ("PLUS", "MINUS"):
    #         token = self.current_token
    #         if token.type == "PLUS":
    #             self.eat("PLUS")
    #             node = BinOp(left=node, op=token, right=self.t_num_expr())
    #         elif token.type == "MINUS":
    #             self.eat("MINUS")
    #             node = BinOp(left=node, op=token, right=self.t_num_expr())

    #     return node

    # def t_num_expr(self):
    #     node = self.f_num_expr()

    #     while self.current_token.type in ("MUL", "DIV", "MOD"):
    #         token = self.current_token
    #         if token.type == "MUL":
    #             self.eat("MUL")
    #             node = BinOp(left=node, op=token, right=self.f_num_expr())
    #         elif token.type == "DIV":
    #             self.eat("DIV")
    #             node = BinOp(left=node, op=token, right=self.f_num_expr())
    #         elif token.type == "MOD":
    #             self.eat("MOD")
    #             node = BinOp(left=node, op=token, right=self.f_num_expr())

    #     return node

    # def f_num_expr(self):
    #     token = self.current_token

    #     if token.type == "NUM":
    #         self.eat("NUM")
    #         return Num(token)

    #     elif token.type == "IDENT":
    #         self.eat("IDENT")
    #         return Var(token)

    #     elif token.type == "READINT":
    #         self.eat("READINT")
    #         return ReadInt()

    #     elif token.type == "LPAREN":
    #         self.eat("LPAREN")
    #         node = self.num_expr()
    #         self.eat("RPAREN")
    #         return node

    #     elif token.type == "MINUS":
    #         self.eat("MINUS")
    #         node = self.num_expr()
    #         return UnaryOp(token, node)

    #     elif token.type == "LENGTH":
    #         self.eat("LENGTH")
    #         self.eat("LPAREN")
    #         node = self.str_expr()
    #         self.eat("RPAREN")
    #         return Length(token,node)

    #     elif token.type == "POSITION":
    #         self.eat("POSITION")
    #         self.eat("LPAREN")
    #         node1 = self.str_expr()
    #         self.eat("COMMA")
    #         node2 = self.str_expr()
    #         self.eat("RPAREN")
    #         return Position(node1, node2)

    #     else:
    #         self.error("NUM, IDENT, READINT, LPAREN, MINUS, LENGTH, POSITION")
    def str_expr(self):
        token = self.current_token
        if token.type == "STRING":
            node = String(token)
            self.eat("STRING")
            return node
    # # grammar rules for string expressions
    # def str_expr(self):
        # token = self.current_token

        # if token.type == "STRING":
        #     self.eat("STRING")
        #     return String(token)

        # elif token.type == "IDENT":
        #     self.eat("IDENT")
        #     return Var(token)

        # elif token.type == "READSTR":
        #     self.eat("READSTR")
        #     return ReadStr()

