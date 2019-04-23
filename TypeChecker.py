import AST
from collections import defaultdict

op_results = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: None)))

for operator in ['.+', '.-', '.*', './']:
    op_results[operator]['matrix']['matrix'] = 'matrix'

for operator in ['*=', '*', '/=', '/']:
    op_results[operator]['matrix']['int'] = 'matrix'
    op_results[operator]['matrix']['float'] = 'matrix'

for operator in ['<', '>', '<=', '>=', '==', '!=']:
    op_results[operator]['int']['float'] = 'int'
    op_results[operator]['float']['int'] = 'int'
    op_results[operator]['float']['float'] = 'int'
    op_results[operator]['int']['int'] = 'int'

for operator in ['+', '-', '*', '/', '+=', '-=', '*=', '/=']:
    op_results[operator]['int']['float'] = 'float'
    op_results[operator]['float']['int'] = 'float'
    op_results[operator]['float']['float'] = 'float'
    op_results[operator]['matrix']['matrix'] = 'matrix'
    op_results[operator]['int']['int'] = 'int'

op_results['\'']['matrix'][None] = 'matrix'
op_results['-']['matrix'][None] = 'matrix'
op_results['-']['int'][None] = 'int'
op_results['-']['float'][None] = 'float'

op_results['+']['string']['string'] = 'string'

class NodeVisitor(object):
    
    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)


    def generic_visit(self, node):        # Called if no explicit visitor function exists for a node.
        if isinstance(node, list):
            for elem in node:
                self.visit(elem)
        else:
            for child in node.children:
                if isinstance(child, list):
                    for item in child:
                        if isinstance(item, AST.Node):
                            self.visit(item)
                elif isinstance(child, AST.Node):
                    self.visit(child)


class TypeChecker(NodeVisitor):

    def visit_BinExpr(self, node):
                                          # alternative usage,
                                          # requires definition of accept method in class Node
        type1 = self.visit(node.left)     # type1 = node.left.accept(self) 
        type2 = self.visit(node.right)    # type2 = node.right.accept(self)
        op    = node.op
        # ... 
        #
 

    def visit_Variable(self, node):
        pass
        
