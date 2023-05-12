class Num:
    def __init__(self, node):
        self.type = node.type
        self.value =int(node.value)
    def to_dict(self):
        return {"type": self.type, "value":self.value }
    def evaluate(self):
        return self.value