import ply.lex as lex
import sys

tokens = ['RLNUM', 'INTNUM', 'ID', 'STRING', 'COMMENT', 'DOTADD', 'DOTSUB', 'DOTMUL', 'DOTDIV', 'ADDASSIGN',
          'SUBASSIGN', 'MULASSIGN', 'DIVASSIGN', 'LESSEQ', 'GREQ', 'NOTEQ', 'EQ']
literals = "+-*/=<>()[]{}:',;"


descriptors = {
    'if': 'IF',
    'else': 'ELSE',
    'for': 'FOR',
    'while': 'WHILE',
    'break': 'BREAK',
    'continue': 'CONTINUE',
    'return': 'RETURN',
    'eye': 'EYE',
    'zeros': 'ZEROS',
    'ones': 'ONES',
    'print': 'PRINT',
}

tokens += list(descriptors.values())

t_DOTADD = r'\.\+'
t_DOTSUB = r'\.-'
t_DOTMUL = r'\.\*'
t_DOTDIV = r'\./'
t_ADDASSIGN = r'\+='
t_SUBASSIGN = r'-='
t_MULASSIGN = r'\*='
t_DIVASSIGN = r'/='
t_LESSEQ = r'<='
t_GREQ = r'>='
t_NOTEQ = r'!='
t_EQ = r'=='


t_ignore = '  \t'


def t_RLNUM(t):
    r'(([0-9]+)(\.)([0-9])*|(\.)([0-9]+))(E[-+]?\d+)?'
    t.value = float(t.value)
    return t


def t_INTNUM(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_ID(t):
    r'[a-zA-Z_]\w*'
    t.type = descriptors.get(t.value, 'ID')
    return t


def t_STRING(t):
    r'\"([^\\\n]|(\\.))*?\"'
    t.value = t.value[1:-1]
    return t


def t_COMMENT(t):
    r'\#.*'
    pass


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1


lexer = lex.lex()

def input(text):
    global lexer
    lexer.input(text)

def token():
    global lexer
    return lexer.token()
