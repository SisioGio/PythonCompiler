from Nodes import *

from lexer import Lexer
class Parser:
    def __init__(self):
        
        self.current_token = None
        self.vars = {}
        self.loop = False

    def advance(self):
        try:
            self.current_token = self.lexer.consume()
        except Exception:
            self.current_token = None


    def error(self, expected_token_type):
        raise SyntaxError(f"Syntax error: expected {expected_token_type}, got {self.current_token.type} ({self.current_token.value})")
    # Get the variable from the vars dict
    def get_variable(self,var_name):
        if(not var_name in self.vars):
            # Variable does not exist
            self.error(f"Undefined variable '{var_name}'")
        return self.vars[var_name]
    def parse(self,input):
            
            # Parse the input and return an abstract syntax tree (AST).
            self.lexer = Lexer(input)
            self.advance()
            
            ast = self.program()
            if not self.current_token is None:
                if self.current_token.type != "EOF":
                    self.error("EOF")
            return ast
     # Root node
    def program(self):
       
        node = self.instr()
        return node
    
    # instr = instr simple_instr ";" | epsilon ;
    # Groups all the instructions in an array.
    # The same method is used to group instructions within the begin end block ( only the name changes)
    def instr(self,name="PROGRAM"):
        
        statements = []
        statement = self.simple_instr()
        statements.append(statement)
        while self.current_token.type == "SEMICOLON":
            self.eat("SEMICOLON")
            next_statement = self.simple_instr()
            if not next_statement is None:
                statements.append(next_statement)
        return StatementList(statements,name)

    # simple_instr
    # This method works as a switch, based on the current token type, it parses specific expressions/instructions/controls
    # Each if condition rapresents a state
    def simple_instr(self):
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
        elif token_type == "BREAK" and self.loop :
            return self.parse_break_statement()
        elif token_type == "CONTINUE" and self.loop:
            return self.parse_continue_statement()
        elif token_type == "EXIT":
            return self.parse_exit_statement()
        elif self.current_token.type == "EOF":
            return None
        else:
            raise SyntaxError(f"Invalid syntax, {token_type} cannot be used to start an instruction")
    # Checks if the current token matches the expected token passed as argument 'token_type'
    # The main objective of this method is to validate the syntax, every expression/instruction has predefined expected tokens.
    # If the current token is not the expected one, a syntax error is thrown
    def eat(self,token_type):
        if(self.current_token.type ==token_type):
            self.current_token = self.lexer.consume()
        else:
            raise SyntaxError(f"Invalid syntax, expected :{token_type} got {self.current_token.type}")

    # Print statement(str_expr | num_expr)
    def parse_print_statement(self):
        token = self.current_token
        self.eat("PRINT")
        self.eat("LPAREN")
        
        value = self.str_expr() if self.is_string_expr() else self.num_expr()
        self.eat("RPAREN")
        return PrintStatement(token,value)
    

    # IDENT STATEMENT: Generates a variable ( str, int) stored as a Var object.
    def parse_ident_statement(self):
        
        node = self.current_token
        self.eat("IDENT")
        self.eat("ASSIGN")
        # Check whatever the next token rapresents a string or an numeric expression
        isString = self.is_string_expr()
        # If the variable is already defined (available in the self.vars dict), it cheks if the new assigned data type matches the current one
        if node.value in self.vars and ((isString and not self.vars[node.value].type == str) or (not isString and self.vars[node.value].type == str)):
            raise SyntaxError("Variable type mismatch")
        # Generate a value based on the next token type, if rapresents a string, then the str_expr() method is called, otherwise the num_expr().
        value =  self.str_expr() if isString else self.num_expr()
        var = Var(node,value)
        self.vars[node.value] = var
        return var
    

    # IF STATEMENT:  The same state is used for "if" bool_expr "then" simple_instr and "if" bool_expr "then" simple_instr "else" simple_instr
    # Different objects types are created based on the presence of the ELSE token.
    def parse_if_statement(self):
        node = self.current_token
        self.eat("IF")
        expr = self.bool_expr()
        self.eat("THEN")
        simple_instruction = self.simple_instr()
        
        if (self.current_token.type == "ELSE"):
            self.eat("ELSE")
            else_simple_instruction = self.simple_instr()
            return  IfElse(node,expr,simple_instruction,else_simple_instruction)
        return If(node,expr,simple_instruction)
    

    # FOR_STAT: It is generated by a sequence of tokens/expressions/instructions
    # "for"  bool_exp "then" simple_instr "else" simple_instr

    def parse_for_statement(self):
        token = self.current_token
        self.eat("FOR")
        iterator = self.parse_ident_statement()
        self.eat("TO")
        limit = self.num_expr()
        self.eat("DO")
        self.loop = True
        simple_instr = self.simple_instr()
        self.loop = False
        forLoopNode = ForLoop(token,iterator,limit,simple_instr)

        return forLoopNode
    # BEGIN DO: The body of this instruction is simply another instr node, which an array of simple_expr
    def parse_begin_do_statement(self):
        token = self.current_token
        self.eat("BEGIN")
        grouped_instructions = self.instr("BEGIN_DO")
        self.eat("END")
        node = BeginEnd(token,grouped_instructions)
        return node
    # BREAK: Breaks the loop when this is object is return from an evaluate() call.
    def parse_break_statement(self):
        token =self.current_token
        self.eat("BREAK")
        node = BreakControl(token)
        return node
    # CONTINUE: Goes to the next iteration when returned from an evaluate() call.
    def parse_continue_statement(self):
        token = self.current_token
        self.eat("CONTINUE")
        node = ContinueControl(token)
        return node
    # EXIT: Terminates the execution with status(1)
    def parse_exit_statement(self):
        token = self.current_token
        self.eat("EXIT")
        node = ExitControl(token)
        return node
    # Checks whatever the next token/var is string
    def is_string_expr(self):
        if self.current_token.type in ("STRING","CONCATENATE","SUBSTRING","READSTR"):
            return True
        if self.current_token.type == "IDENT":
            var_node = self.get_variable(self.current_token.value)
            var_value = var_node.value
            if isinstance(var_value,str):
                return True
        return False



# Numeric expressions (num_expr) are generated using a recursive approach in order to split the types of expressions by priority.

# EXAMPLE FOR THE NUM_EXPR = 2+3*2

#______________________________BinOp(+)___________________________________
#_____________________________/________\__________________________________
#____________________________/__________\_________________________________
#___________________________/____________\________________________________
#_____________f_num_expr(2)____________BinOp(x)____________________________
#__________________________________________/\______________________________
#_________________________________________/__\_______________________________
#________________________________________/____\______________________________
#___________________________f_num_expr(3)______f_num_expr(2)_______________
    #
    # When evaluting BinOp(), we perform the operation between the two children.
    # f_num_expr gives immediately 2
    # BinOp(x) performs a multiplication between the two children f_num_expr(3) and f_num_expr(2) and returns the value.
    
    # The parantheses do not have any node, they simply restart from the num_expr node trying to generate a new 'sub-tree' ( which in the basic case can be a num value)


    def num_expr(self):
        left = self.t_num_expr()
        while self.current_token.type in ("PLUS", "MINUS"):
            op = self.current_token
            if op.type == "PLUS":
                self.eat("PLUS")
            elif op.type == "MINUS":
                self.eat("MINUS")
            right = self.t_num_expr()
            left = BinOp(left, op, right)
        return left
    # T_NUM_EXPR
    def t_num_expr(self):
        left = self.f_num_expr()
        while self.current_token.type in ("MULT", "DIV","MODULO"):
            op = self.current_token
            if op.type == "MULT":
                self.eat("MULT")
            elif op.type == "DIV":
                self.eat("DIV")
            elif op.type == "MODULO":
                self.eat("MODULO")
            right = self.f_num_expr()
            left = BinOp(left, op, right)
        return left
    # F_NUM_EXPR: Used to generated the last nodes in the hierarchy of a numeric expression.
    # When evaluating/executing the programs, the last nodes to be executed are generated by this method.
    # When 'LPAREN' is the current value, the body must be generated again from the num_expr recursively.
    # Recursion is needed so that we can parse very complex numeric expression with the right logic.

    def f_num_expr(self):
        curr_token = self.current_token
        if curr_token.type == "LPAREN":
            self.eat("LPAREN")
            expr = self.num_expr()
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
            # Check variable data type
            if node.datatype != int:
                raise SyntaxError(f"Expected int got {node.datatype}")
            return node
        elif curr_token.type == "READINT":
            node = ReadInt(curr_token)
            self.eat("READINT")
            return node
        elif curr_token.type == "MINUS":
        
            self.eat("MINUS")
            expr= self.f_num_expr()
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
            raise SyntaxError(f"Invalid syntax, expected LPAREN,NUM,IDENT,READINT,MINUS,LENGTH,POSITION got {curr_token.type}")

    #  STR_EXPR: All expressions have the same priority so there is no need to build a specific hierarchy.
    # Recursion is as well applied only to create a sub-tree of str_exprr such as SUBSTRING(CONCATENATE("A","BCDEF"),2,1)

    #_________________________SUBSTRING_____________________________________
    # _______________________/_____\___\____________________________________
    #_______________________/______ 2 _ 1 __________________________________
    # _________________CONCATENATE__________________________________________
    # ________________/___________\_________________________________________
    # _____________ A _________ BCDEF ______________________________________



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
            start_index = self.num_expr()
            self.eat("COMMA")
            length_expr = self.num_expr()
            self.eat("RPAREN")
            node = Substring(token,str_expr,start_index,length_expr)
            return  node
        elif token.type == "IDENT":
            # Get variable from 'vars' dict
            node = self.get_variable(token.value)
            if node.datatype != str:
                raise SyntaxError(f"Expected str got {node.datatype}")
            # To do: Check if type is str
            self.eat("IDENT")
            return node
        elif token.type == "READSTR":
            self.eat("READSTR")
            node = ReadStr(token)
            # To do: Check if type is str
            
            return node
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
        if token.type == "TRUE":
            node = Boolean(token)
            self.eat("TRUE")
            return node
        if token.type == "FALSE":
            node = Boolean(token)
            self.eat("FALSE")
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
            left = self.num_expr()
            num_rel = self.current_token
            self.eat("NUM_REL")
            right = self.num_expr()
            node = NumComparison(num_rel,left,right)
            return node

        
        else:
            raise SyntaxError("Invalid syntax")
    
if __name__ == '__name__':
    parser = Parser()
