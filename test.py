from main import Parser

text = """PRINT(substring("Alessio",2,2))"""
parser = Parser(text)
result = parser.parse()

print(result.__str__())
result.evaluate()