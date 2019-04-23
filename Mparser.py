import ply.yacc as yacc
import scanner
import AST


class Parser:

    def __init__(self):
        self.scanner = scanner
        self.parser = None

    def parse(self, text):
        self.parser = yacc.yacc(module=self)
        return self.parser.parse(text, lexer=self.scanner.lexer)

    tokens = scanner.tokens

    precedence = (
        ("nonassoc", 'IF'),
        ("nonassoc", 'ELSE'),
        ("right", '=', "ADDASSIGN", "SUBASSIGN", "MULASSIGN", "DIVASSIGN"),
        ("nonassoc", '<', '>', 'EQ', 'NOTEQ', 'LESSEQ', 'GREQ'),
        ("left", '+', '-', 'DOTADD', 'DOTSUB'),
        ("left", '*', '/', 'DOTMUL', 'DOTDIV'),
        ("left", 'UMINUS'),
        ("right", '\'')
    )

    def p_error(self, p):
        self.no_error = False
        if p:
            print("Syntax error at line {}: token({}, '{}')".format(
                p.lineno, p.type, p.value))
        else:
            print("Unexpected end of input")

    def p_program(self, p):
        """program : statements"""
        p[0] = p[1]

    def p_statements(self, p):
        """statements : '{' statements '}'
                               | statements statement
                               | statement
                               | statements '{' statements '}'"""
        if len(p) == 2:
            p[0] = AST.Statements()
            p[0].statements.append(p[1])
        elif len(p) == 3:
            p[1].statements.append(p[2])
            p[0] = p[1]
        elif len(p) == 4:
            p[0] = p[2]
        elif len(p) == 5:
            p[1].statements.extend(p[3].statements)
            p[0] = p[1]


    def p_statement(self, p):
        """statement : assignment
                     | flow_control """
        p[0] = p[1]

    def p_assignment(self, p):
        """assignment : var asgmt_type expr ';'
                      | matrix_var asgmt_type simple_expr ';'"""

        p[0] = AST.Assignment(p[1], p[2], p[3])

    def p_asgmt_type(self, p):
        """asgmt_type : '=' 
                      | ADDASSIGN 
                      | SUBASSIGN 
                      | MULASSIGN
                      | DIVASSIGN"""
        p[0] = p[1]

    def p_expr(self, p):
        """expr : simple_expr
                | matrix_decl"""
        p[0] = p[1]

    def p_simple_expr(self, p):
        """simple_expr : var
                       | constant
                       | bin_op
                       | un_op
                       | logic_op
                       | '(' expr ')'"""

        if isinstance(p[1], AST.Constant):
            p[0] = p[1]
        elif p[1] == '(':
            p[0] = p[2]
        elif isinstance(p[1], str):
            p[0] = AST.Var(p[1])
        else:
            p[0] = p[1]

    def p_constant(self, p):
        """constant : INTNUM
                    | RLNUM
                    | STRING"""
        if isinstance(p[1], int):
            p[0] = AST.IntNum(p[1])
        if isinstance(p[1], float):
            p[0] = AST.FloatNum(p[1])
        if isinstance(p[1], str):
            p[0] = AST.String(p[1])

    def p_var(self, p):
        """var : ID"""
        p[0] = AST.Var(p[1])

    def p_val(self, p):
        """val : var
               | matrix_decl
               | constant"""
        p[0] = AST.Val(p[1])

    def p_matrix_var(self, p):
        """matrix_var : ID '[' INTNUM ',' INTNUM ']'"""

        p[0] = AST.MatrixVar(p[1], p[3], p[5])

    def p_matrix_decl(self, p):
        """matrix_decl : EYE '(' INTNUM ')'
                       | ZEROS '(' INTNUM ')'
                       | ONES '(' INTNUM ')'
                       | '[' matrix_row ']'"""
        if p[1] == 'eye':
            p[0] = AST.Eye(p[3])
        elif p[1] == 'zeros':
            p[0] = AST.Zeros(p[3])
        elif p[1] == 'ones':
            p[0] = AST.Ones(p[3])
        else:
            p[0] = AST.MatrixDecl()
            p[0].rows = p[2]

    def p_matrix_row(self, p):
        """matrix_row : matrix_row ',' val
                       | val"""
        if len(p) == 2:
            p[0] = AST.MatrixRow()
            p[0].values.append(p[1])
        else:
            p[1].values.append(p[3])
            p[0] = p[1]

    def p_bin_op(self, p):
        """bin_op : expr '+' expr
                  | expr '*' expr
                  | expr '-' expr
                  | expr '/' expr
                  | expr DOTADD expr
                  | expr DOTSUB expr
                  | expr DOTMUL expr
                  | expr DOTDIV expr"""
        p[0] = AST.BinOp(p[1], p[2], p[3])

    def p_logic_op(self, p):
        """logic_op : expr EQ expr
                  | expr NOTEQ expr
                  | expr '>' expr
                  | expr '<' expr
                  | expr LESSEQ expr
                  | expr GREQ expr"""
        p[0] = AST.LogicOp(p[1], p[2], p[3])

    def p_un_op(self, p):
        """un_op : expr "'"
                 | '-' expr %prec UMINUS"""
        if p[1] == '-':
            p[0] = AST.UnOp(p[2], p[1])
        else:
            p[0] = AST.UnOp(p[1], p[2])

    def p_flow_control(self, p):
        """flow_control : conditional_statement
                        | while_stmt
                        | for_stmt
                        | return_stmt
                        | break_stmt
                        | continue_stmt
                        | print_stmt"""
        p[0] = p[1]

    def p_conditional_statement(self, p):
        """conditional_statement : IF '(' logic_op ')' conditional_instructions %prec IF
                                 | IF '(' logic_op ')' conditional_instructions ELSE conditional_instructions """
        if len(p) == 6:
            p[0] = AST.CondStmt(p[3], p[5])
        else:
            p[0] = AST.CondStmt(p[3], p[5], True, p[7])

    def p_conditional_instructions(self, p):
        """conditional_instructions : statement
                                    | '{' statements '}'"""
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = p[2]

    def p_while_stmt(self, p):
        """while_stmt : WHILE '(' logic_op ')' conditional_instructions"""
        p[0] = AST.WhileStmt(p[3], p[5])

    def p_for_stmt(self, p):
        """for_stmt : FOR ID '=' expr ':' expr conditional_instructions"""
        p[0] = AST.ForStmt(p[2], p[4], p[6], p[7])

    def p_return_stmt(self, p):
        """return_stmt : RETURN expr ';' """
        p[0] = AST.ReturnStmt(p[2])

    def p_continue_stmt(self, p):
        """continue_stmt : CONTINUE ';' """
        p[0] = AST.ContinueStmt()

    def p_break_stmt(self, p):
        """break_stmt : BREAK ';' """
        p[0] = AST.BreakStmt()

    def p_print_stmt(self, p):
        """print_stmt : PRINT instructions ';' """
        p[0] = p[2]

    def p_instructions(self, p):
        """instructions : instructions ',' expr
                        | expr"""
        if len(p) == 2:
            p[0] = AST.PrintStmt()
            p[0].instructions.append(p[1])
        else:
            p[1].instructions.append(p[3])
            p[0] = p[1]
