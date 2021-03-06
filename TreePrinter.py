from __future__ import print_function
import AST


def addToClass(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func

    return decorator


class TreePrinter:

    @addToClass(AST.Node)
    def printTree(self, indent=0):
        raise Exception("printTree not defined in class " + self.__class__.__name__)

    @addToClass(AST.Val)
    def printTree(self, depth):
        if hasattr(self.id, "printTree"):
            return self.id.printTree(depth)
        else:
            return depth + str(self.id) + "\n"

    @addToClass(AST.Constant)
    def printTree(self, depth):
        return depth + str(self.value) + "\n"

    @addToClass(AST.Var)
    def printTree(self, depth):
        if hasattr(self.id, "printTree"):
            return self.id.printTree(depth)
        else:
            return depth + str(self.id) + "\n"

    @addToClass(AST.MatrixVar)
    def printTree(self, depth):
        result = depth + "REF\n"
        result += depth + "| " + str(self.id) + "\n"
        result += depth + "| " + str(self.row) + "\n"
        result += depth + "| " + str(self.col) + "\n"
        return result

    @addToClass(AST.Statements)
    def printTree(self, depth):
        result = ""
        for block in self.statements:
            result += block.printTree(depth)
        return result

    @addToClass(AST.Assignment)
    def printTree(self, depth):
        result = depth + str(self.op) + "\n"
        result += self.left.printTree(depth + "| ")
        result += self.right.printTree(depth + "| ")
        return result

    @addToClass(AST.BinOp)
    def printTree(self, depth):
        result = depth + str(self.op) + "\n"
        result += self.left.printTree(depth + "| ")
        result += self.right.printTree(depth + "| ")
        return result

    @addToClass(AST.UnOp)
    def printTree(self, depth):
        name = ""
        if self.op == "'":
            name = "TRANSPOSE"
        else:
            name = "NEGATION"
        result = depth + name + "\n"
        result += self.expression.printTree(depth + "| ")
        return result

    @addToClass(AST.PrintStmt)
    def printTree(self, depth):
        result = depth + "PRINT\n"
        for instruction in self.instructions:
            result += instruction.printTree(depth + "| ")
        return result

    @addToClass(AST.CondStmt)
    def printTree(self, depth):
        result = depth + "IF\n"
        result += self.condition.printTree(depth + "| ")
        result += depth + "THEN\n"
        result += self.statements.printTree(depth + "| ")
        if self.has_else:
            result += depth + "ELSE\n"
            result += self.else_statements.printTree(depth + "| ")
        return result

    @addToClass(AST.WhileStmt)
    def printTree(self, depth):
        result = depth + "WHILE\n"
        result += depth + "| COND\n"
        result += self.condition.printTree(depth + "| ")
        result += depth + "| DO\n"
        result += self.statements.printTree(depth + "| ")
        return result

    @addToClass(AST.ForStmt)
    def printTree(self, depth):
        result = depth + "FOR\n"
        result += depth + "| " + self.id + "\n"
        result += depth + "| RANGE\n"
        result += self.start.printTree(depth + "| | ")
        result += self.end.printTree(depth + "| | ")
        result += self.statements.printTree(depth + "| ")
        return result

    @addToClass(AST.ReturnStmt)
    def printTree(self, depth):
        result = depth + "RETURN\n"
        result += self.value.printTree(depth + "| ")
        return result

    @addToClass(AST.ContinueStmt)
    def printTree(self, depth):
        return depth + "CONTINUE\n"

    @addToClass(AST.BreakStmt)
    def printTree(self, depth):
        return depth + "BREAK\n"

    @addToClass(AST.MatrixDecl)
    def printTree(self, depth):
        result = self.rows.printTree(depth)
        return result

    @addToClass(AST.MatrixRow)
    def printTree(self, depth):
        result = depth + "VECTOR\n"
        for val in self.values:
            result += val.printTree(depth + "| ")
        return result

    @addToClass(AST.Ones)
    def printTree(self, depth):
        result = depth + "ONES\n"
        result += depth + "| " + str(self.n) + "\n"
        return result

    @addToClass(AST.Eye)
    def printTree(self, depth):
        result = depth + "EYE\n"
        result += depth + "| " + str(self.n) + "\n"
        return result

    @addToClass(AST.Zeros)
    def printTree(self, depth):
        result = depth + "ZEROS \n"
        result += depth + "| " + str(self.n) + "\n"
        return result