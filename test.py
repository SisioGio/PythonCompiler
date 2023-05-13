from main import Parser

text = """for i := 1 to 10 do 

PRINT(i)



"""
parser = Parser(text)
result = parser.parse()

print(result.to_dict())
result.evaluate()