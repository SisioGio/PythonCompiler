import unittest
import os
import sys
from io import StringIO
# directory reach
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)


from main import Parser
from io import StringIO

class TestStringMethods(unittest.TestCase):

    def execute_command(self,command):
        
        output = StringIO()
        # Input is simulated by entering the number 2, which is ok for strings and integers
        sys.stdin = StringIO("2")
        sys.stdout = output
        parser = Parser()
        parser.parse(command).evaluate()
        output_str = output.getvalue().strip()
        sys.stdout = sys.__stdout__
        return output_str


    def test_print_number(self):
        
        self.assertEqual('ALESSIO',self.execute_command("""PRINT("ALESSIO")"""))


    def test_print_string(self):
        self.assertEqual('2',self.execute_command("""PRINT(2)"""))


    def test_print_num_expr(self):
        self.assertEqual('7',self.execute_command("""PRINT(2+5)"""))

    def test_print_complex_num_expr(self):
        self.assertEqual('44',self.execute_command("""PRINT(2+5*10-(2+3*2))"""))

    def test_print_len(self):
        self.assertEqual('4',self.execute_command("""PRINT(length("test"))"""))

    def test_print_readint(self):
        self.assertEqual(self.execute_command("""PRINT(readint)"""),'2')


    def test_print_readStr(self):
        self.assertEqual(self.execute_command("""PRINT(readstr)"""),'2')
   
    def test_print_negation(self):
        self.assertEqual(self.execute_command("""PRINT(-5)"""),'-5')
    
    def test_print_position(self):
        self.assertEqual(self.execute_command("""PRINT(position("University","ver"))"""),'3')

    def test_print_position(self):
        self.assertEqual(self.execute_command("""PRINT(position("University","ver"))"""),'3')

    def test_print_concatenate(self):
        self.assertEqual(self.execute_command("""PRINT(concatenate("DE","SK"))"""),'DESK')
    def test_print_substring(self):
        self.assertEqual(self.execute_command("""PRINT(substring("OFFICE",2,2))"""),'FI')
    
    def test_print_num_rel_equal(self):
        self.assertEqual(self.execute_command("""if(2=2) then PRINT("OK")"""),'OK')

    def test_print_num_rel_lt(self):
        self.assertEqual(self.execute_command("""if(2<5) then PRINT("OK")"""),'OK')

    def test_print_num_rel_le(self):
        self.assertEqual(self.execute_command("""if(2<=2) then PRINT("OK")"""),'OK')

    def test_print_num_rel_gt(self):
        self.assertEqual(self.execute_command("""if(3>2) then PRINT("OK")"""),'OK')

    def test_print_num_rel_ge(self):
        self.assertEqual(self.execute_command("""if(3>=3) then PRINT("OK")"""),'OK')

    def test_print_num_rel_ne(self):
        self.assertEqual(self.execute_command("""if(3<>2) then PRINT("OK")"""),'OK')

    def test_print_str_rel_eq(self):
        self.assertEqual(self.execute_command("""if("test" == "test") then PRINT("OK")"""),'OK')

    def test_print_str_rel_ne(self):
        self.assertEqual(self.execute_command("""if("test" != "test2") then PRINT("OK")"""),'OK')

    def test_print_bool_true(self):
        self.assertEqual(self.execute_command("""if(true) then PRINT("OK")"""),'OK')

    def test_print_bool_false(self):
        self.assertEqual(self.execute_command("""if(false) then PRINT("NOT OK") else PRINT("OK")"""),'OK')

    def test_print_bool_negation(self):
        self.assertEqual(self.execute_command("""if(not false) then PRINT("OK")"""),'OK')
    
    def test_print_bool_complex_num_expr(self):
        self.assertEqual(self.execute_command("""if(2*10+140/2+7=(100-80%7)) then PRINT("OK")"""),'OK')
    
    def test_print_variable(self):
        self.assertEqual(self.execute_command("""X:=1003;PRINT(X)"""),'1003')

    def test_loop(self):
        self.assertEqual(self.execute_command("""for i:=1 to 10 do PRINT(i);"""),"1\n2\n3\n4\n5\n6\n7\n8\n9")

    def test_loop_if_else(self):
        self.assertEqual(self.execute_command("""for i:=1 to 10 do if(i%2=0) then PRINT(i);"""),'2\n4\n6\n8')

    def test_loop_if_else_break(self):
        self.assertEqual(self.execute_command("""for i:=1 to 10 do if(i<6) then PRINT(i) else break;"""),'1\n2\n3\n4\n5')

    def test_loop_if_else_continue(self):
        self.assertEqual(self.execute_command("""for i:=1 to 10 do if(i%2=0) then PRINT(i) else continue"""),'2\n4\n6\n8')

    def test_loop_begin_do(self):
        self.assertEqual(self.execute_command("""for i:=1 to 2 do begin PRINT("FIRST INSTR");PRINT("SECOND INSTR") end"""),'FIRST INSTR\nSECOND INSTR')

    def test_exit(self):
        try:
            self.execute_command("""begin PRINT("FIRST INSTR");exit;PRINT("SECOND INSTR") end""")
        except SystemExit as e:
            self.assertEqual(e.code, 1)
    
    def test_invalid_identifier(self):
        try:
            self.execute_command("i=3")
        except SyntaxError as e:
            self.assertEqual(e.msg, "Invalid syntax, expected :ASSIGN got NUM_REL")

    def test_invalid_start_of_expr(self):
        try:
            self.execute_command(""" 2+"test" """)
        except SyntaxError as e:
            self.assertEqual(e.msg, "Invalid syntax, NUM cannot be used to start an instruction")

    def test_invalid_start_of_expr(self):
        try:
            self.execute_command(""" i := 2+"test" """)
        except SyntaxError as e:
            self.assertEqual(e.msg, "Invalid syntax, expected LPAREN,NUM,IDENT,READINT,MINUS,LENGTH,POSITION got STRING")

    def test_invalid_ident(self):
        try:
            self.execute_command(""" i := true """)
        except SyntaxError as e:
            self.assertEqual(e.msg, "Invalid syntax, expected LPAREN,NUM,IDENT,READINT,MINUS,LENGTH,POSITION got TRUE")
    
    def test_invalid_num_expr_args(self):
        try:
            self.execute_command(""" i := (2*"testing") """)
        except SyntaxError as e:
            self.assertEqual(e.msg, "Invalid syntax, expected LPAREN,NUM,IDENT,READINT,MINUS,LENGTH,POSITION got STRING")

    def test_invalid_variable_usage(self):
        try:
            self.execute_command(""" i := 2; PRINT(length(i)) """)
        except SyntaxError as e:
            self.assertEqual(e.msg, "Expected str got <class 'int'>")

    def test_invalid_variable_usage(self):
        try:
            self.execute_command(""" i := 2; PRINT(length(i)) """)
        except SyntaxError as e:
            self.assertEqual(e.msg, "Expected str got <class 'int'>")


    def test_invalid_variable_assignment(self):
        try:
            self.execute_command(""" i := 2;i:="test" """)
        except SyntaxError as e:
            self.assertEqual(e.msg, "Variable type mismatch")




if __name__ == '__main__':
    unittest.main()