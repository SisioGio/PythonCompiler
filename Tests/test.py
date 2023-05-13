import unittest
import os
import sys
# directory reach
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)


from main import Parser
from io import StringIO

class TestStringMethods(unittest.TestCase):

    def execute_command(self,command):
        output = StringIO()
        sys.stdout = output
        parser = Parser()
        parser.parse(command).evaluate()
        output_str = output.getvalue().strip()
        sys.stdout = sys.__stdout__
        return output_str
    # Test PRINT("ALESSIO")
    def test_print_number(self):
        
        self.assertEqual('ALESSIO',self.execute_command("""PRINT("ALESSIO")"""))

    # Test PRINT(2)
    def test_print_string(self):
        self.assertEqual('2',self.execute_command("""PRINT(2)"""))

    # Test PRINT(num_expr)
    def test_print_num_expr(self):
        self.assertEqual('7',self.execute_command("""PRINT(2+5)"""))
   # Test PRINT(complex_expr) includes (num_expr) , - num_expr
    def test_print_complex_num_expr(self):
        self.assertEqual('44',self.execute_command("""PRINT(2+5*10-(2+3*2))"""))
   # Test PRINT(length)
    def test_print_len(self):
        self.assertEqual('4',self.execute_command("""PRINT(length("test"))"""))

    # Uncomment to test readInt
    # Test PRINT(readint (10))
    # def test_print_readint(self):
    #     self.assertEqual('10',self.execute_command("""PRINT(readint)"""))
    # Test PRINT(NEGATION (10))
    def test_print_negation(self):
        self.assertEqual('-5',self.execute_command("""PRINT(-5)"""))
    
    def test_print_position(self):
        self.assertEqual('3',self.execute_command("""PRINT(position("University","ver"))"""))

    def test_print_position(self):
        self.assertEqual('3',self.execute_command("""PRINT(position("University","ver"))"""))

    def test_print_concatenate(self):
        self.assertEqual('DESK',self.execute_command("""PRINT(concatenate("DE","SK"))"""))
    def test_print_substring(self):
        self.assertEqual('FI',self.execute_command("""PRINT(substring("OFFICE",2,2))"""))
    
    def test_print_num_rel_equal(self):
        self.assertEqual('OK',self.execute_command("""if(2=2) then PRINT("OK")"""))
    def test_print_num_rel_lt(self):
        self.assertEqual('OK',self.execute_command("""if(2<5) then PRINT("OK")"""))
    def test_print_num_rel_le(self):
        self.assertEqual('OK',self.execute_command("""if(2<=2) then PRINT("OK")"""))
    def test_print_num_rel_gt(self):
        self.assertEqual('OK',self.execute_command("""if(3>2) then PRINT("OK")"""))
    def test_print_num_rel_ge(self):
        self.assertEqual('OK',self.execute_command("""if(3>=3) then PRINT("OK")"""))
    def test_print_num_rel_ne(self):
        self.assertEqual('OK',self.execute_command("""if(3<>2) then PRINT("OK")"""))

if __name__ == '__main__':
    unittest.main()