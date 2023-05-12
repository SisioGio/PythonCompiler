from main import Parser

text = """PRINT(position("ALESSIO","IO"))"""
parser = Parser(text)
result = parser.parse()

print(result.__str__())
result.evaluate()