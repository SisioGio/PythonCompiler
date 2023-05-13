from Nodes import *

from lexer import Lexer
class Parser:
    def __init__(self, input):
        self.lexer = Lexer(input)
        curr_token = None
        self.vars = {}
        self.advance()


    def advance(self):
        try:
            self.current_token = self.lexer.consume()
        except Exception:
            self.current_token = None


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
        # if not curr_token is None:
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
        elif token_type == "IF":
            return self.parse_if_statement()
        elif token_type == "FOR":
            return self.parse_for_statement()
        elif token_type == "BEGIN":
            return self.parse_begin_do_statement()
        elif token_type == "BREAK" :
            return self.parse_break_statement()
        elif token_type == "CONTINUE":
            return self.parse_continue_statement()
        elif token_type == "EXIT":
            return self.parse_exit_statement()
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
        token = self.current_token
        self.eat("PRINT")
        self.eat("LPAREN")
        
        value = self.str_expr() if self.is_string_expr() else self.expr()
        self.eat("RPAREN")
        return PrintStatement(token,value)
    
    def parse_ident_statement(self):
        
        node = self.current_token
        self.eat("IDENT")
        self.eat("ASSIGN")
        
        value =  self.str_expr() if self.is_string_expr() else self.expr()
        var = Var(node,value)
        self.vars[node.value] = var
        return var
    def parse_if_statement(self):
        node = self.current_token
        self.eat("IF")
        expr = self.bool_expr()
        self.eat("THEN")
        simple_instruction = self.statement()
        if (self.current_token.type == "ELSE"):
            self.eat("ELSE")
            else_simple_instruction = self.statement()
            return  IfElse(node,expr,simple_instruction,else_simple_instruction)
        return If(node,expr,simple_instruction)
    
    def parse_for_statement(self):
        token = self.current_token
        self.eat("FOR")
        iterator = self.parse_ident_statement()
        self.eat("TO")
        limit = self.expr()
        self.eat("DO")
        simple_instr = self.statement()

        forLoopNode = ForLoop(token,iterator,limit,simple_instr)

        return forLoopNode

    def parse_begin_do_statement(self):
        token = self.current_token
        self.eat("BEGIN")
        grouped_instructions = self.statement_list()
        self.eat("END")
        node = BeginEnd(token,grouped_instructions)
        return node
    
    def parse_break_statement(self):
        token =self.current_token
        self.eat("BREAK")
        node = BreakControl(token)
        return node
    def parse_continue_statement(self):
        token = self.current_token
        self.eat("CONTINUE")
        node = ContinueControl(token)
        return node
    def parse_exit_statement(self):
        token = self.current_token
        self.eat("EXIT")
        node = ExitControl(token)
        return node
    # Checks whatever the next token/var is string
    def is_string_expr(self):
        if self.current_token.type in ("STRING","CONCATENATE","SUBSTRING"):
            return True
        if self.current_token.type == "IDENT":
            var_node = self.get_variable(self.current_token.value)
            var_value = var_node.value
            if isinstance(var_value,str):
                return True
        return False

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
        curr_token = self.current_token
        if curr_token.type == "LPAREN":
            self.eat("LPAREN")
            expr = self.expr()
            self.eat("RPAREN")
            return expr
        elif curr_token.type == "NUM":
            node = Num(curr_token)
            self.eat("NUM")
            return node
        elif curr_token.type == "IDENT":
            # Get variable from 'vars' dict
            node = self.get_variable(curr_token.value)
            self.eat("IDENT")
            return node
        elif curr_token.type == "READINT":
            node = ReadInt(curr_token)
            self.eat("READINT")
            return node
        elif curr_token.type == "MINUS":
        
            self.eat("MINUS")
            expr= self.factor()
            node = UnaryOp(curr_token,expr)
            return node
        elif curr_token.type == "LENGTH":
         
            self.eat("LENGTH")
            self.eat("LPAREN")
            node = self.str_expr()
            self.eat("RPAREN")
            return Length(curr_token,node)
        elif curr_token.type == "POSITION":
            
            self.eat("POSITION")
            self.eat("LPAREN")
            input_expr = self.str_expr()
            self.eat("COMMA")
            sub_expr = self.str_expr()
            self.eat("RPAREN")
            node = Position(curr_token,input_expr,sub_expr)
            return node

        else:
            raise SyntaxError("Invalid syntax")
    
    def get_variable(self,var_name):
        if(not var_name in self.vars):
            # Variable does not exist
            self.error(f"Undefined variable '{var_name}'")

        
        return self.vars[var_name]

    def str_expr(self):
        token = self.current_token
        if token.type == "STRING":
            node = String(token)
            self.eat("STRING")
            return node
        if token.type == "CONCATENATE":
                
                self.eat("CONCATENATE")
                self.eat("LPAREN")
                left = self.str_expr()
                self.eat("COMMA")
                right = self.str_expr()
              
                self.eat("RPAREN")
                node = Concatenate(token,left,right)
                return node
        if token.type == "SUBSTRING":
            self.eat("SUBSTRING")
            self.eat("LPAREN")
            str_expr = self.str_expr()
            self.eat("COMMA")
            start_index = self.expr()
            self.eat("COMMA")
            length_expr = self.expr()
            self.eat("RPAREN")
            node = Substring(token,str_expr,start_index,length_expr)
            return  node
        elif token.type == "IDENT":
            # Get variable from 'vars' dict
            node = self.get_variable(token.value)
            self.eat("IDENT")
            return node.value
        
    def bool_expr(self):
        left = self.t_bool_expr()
        token = self.current_token
        while token.type == "OR":
            self.eat("OR")
            right = self.t_bool_expr()
            left = Or(token,left,right)
        return left
    
    def t_bool_expr(self):
        left = self.f_bool_expr()
        token = self.current_token
        while token.type == "AND":
            self.eat("AND")
            right = self.f_bool_expr()
            left = And(token,left,right)

        return left
    def f_bool_expr(self):
        token = self.current_token
        if token.type == "LPAREN":
            self.eat("LPAREN")
            bool_expr = self.bool_expr()
            self.eat("RPAREN")
            return bool_expr
        if token.type == "NOT":
            not_token = token
            self.eat("NOT")
            bool_expr = self.bool_expr()
            node = Not(not_token,bool_expr)
            return node
        is_string = self.is_string_expr()

        if  is_string:
            left = self.str_expr()
            str_rel = self.current_token
            self.eat("STR_REL")
            right = self.str_expr()
            node = StringComparison(str_rel,left,right)
            return node
        if not is_string:
            left = self.expr()
            num_rel = self.current_token
            self.eat("NUM_REL")
            right = self.expr()
            node = NumComparison(num_rel,left,right)
            return node
        if token.type == "TRUE":
            node = Boolean(token)
            self.eat("TRUE")
            return node
        if token.type == "FALSE":
            node = Boolean(token)
            self.eat("FALSE")
            return node
        
        else:
            raise SyntaxError("Invalid syntax")
    

