from main import Parser

text = """PRINT(length("ALESSIO DAJE"))"""
parser = Parser(text)
result = parser.parse()

print(result.__str__())
result.evaluate()