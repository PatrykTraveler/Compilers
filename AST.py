class Node(object):
    def accept(self, visitor):
        return visitor.visit(self)

class Statements(Node):
    def __init__(self):
        self.statements = []


class Constant(Node):
    def __init__(self, value):
        self.value = value


class IntNum(Constant):
    pass


class FloatNum(Constant):
    pass


class String(Constant):
    pass

class Var(Node):
    def __init__(self, id):
        self.id = id

class Val(Node):
    def __init__(self, id):
        self.id = id

class MatrixVar(Node):
    def __init__(self, id, row, col):
        self.id = id
        self.row = row
        self.col = col

class MatrixDecl(Node):
    def __init__(self):
        self.rows = []

class Ones(MatrixDecl):
    def __init__(self, n):
        super().__init__()
        self.n = n
        self.rows.extend([MatrixRow([1] * n)]*n)  

class Eye(MatrixDecl):
    def __init__(self, n):
        super().__init__()
        self.n = n
        for r in range(n):
            row = MatrixRow()
            row.values = [0] * n
            row.values[r] = 1
            self.rows.append(row)

class Zeros(MatrixDecl):
    def __init__(self, n):
        super().__init__() 
        self.n = n
        self.rows.extend([MatrixRow([0] * n)]*n)       

class MatrixRow(Node):
    def __init__(self, values=None):
        if(values == None):
            self.values = []
        else:
            self.values = values

class Assignment(Node):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right


class BinOp(Node):
    def __init__(self, left, op, right):
        self.op = op
        self.left = left
        self.right = right


class LogicOp(BinOp):
    pass


class UnOp(Node):
    def __init__(self, expression, op):
        self.op = op
        self.expression = expression


class CondStmt(Node):
    def __init__(self, condition, statements, has_else=False, else_statements=None):
        self.condition = condition
        self.statements = statements
        self.has_else = has_else
        self.else_statements = else_statements


class WhileStmt(Node):
    def __init__(self, condition, statements):
        self.condition = condition
        self.statements = statements


class ForStmt(Node):
    def __init__(self, id, start, end, statements):
        self.id = id
        self.start = start
        self.end = end
        self.statements = statements


class ReturnStmt(Node):
    def __init__(self, value):
        self.value = value


class ContinueStmt(Node):
    pass


class BreakStmt(Node):
    pass


class PrintStmt(Node):
    def __init__(self):
        self.instructions = []


class Error(Node):
    def __init__(self):
        pass
