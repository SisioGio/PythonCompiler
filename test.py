from main import Parser

text = """exit



"""
parser = Parser(text)
result = parser.parse()

print(result.to_dict())
result.evaluate()