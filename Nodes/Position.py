class Position:
    def __init__(self, str_expr1, str_expr2):
        self.str_expr1 = str_expr1
        self.str_expr2 = str_expr2

    def __repr__(self):
        return f"Position({self.str_expr1}, {self.str_expr2})"
