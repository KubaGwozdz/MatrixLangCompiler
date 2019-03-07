tokens = ( 'FLOATNUM', 'INTNUM', 'ID', 'MATRIX_PLUS', 'MATRIX_MINUS', 'MATRIX_TIMES' 'MATRIX_DIVIDE', 'INCREMENT', 'DECREMENT',
           'MULTIPLY', 'DIVIDE', 'SMALLEREQ', 'GREATEREQ', 'NOTEQ', 'EQ', 'STRING')

t_MATRIX_PLUS    = r'\.+'
t_MATRIX_MINUS   = r'.-'
t_MATRIX_TIMES   = r'\.*'
t_MATRIX_DIVIDE  = r'./'
t_INCREMENT      = r'+='
t_DECREMENT      = r'-='
t_MULTIPLY       = r'*='
t_DIVIDE         = r'/='
t_SMALLEREQ      = r'<='
t_GREATEREQ      = r'>='
t_NOTEQ          = r'!='
t_EQ             = r'=='

reserved = {
    'if'      : 'IF',
    'else'    : 'ELSE',
    'for'     : 'FOR',
    'while'   : 'WHILE',
    'break'   : 'BREAK',
    'continue': 'CONTINUE',
    'return'  : 'RETURN',
    'eye'     : 'EYE',
    'zeros'   : 'ZEROS',
    'ones'    : "ONES",
    'print'   : 'PRINT'
}

literals = "+-*/()[]{}=:',;<>"


def t_FLOATNUM(t):
    r'd+.d+'
    t.value = float(t.value)
    return t

def t_INTNUM(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STRING(t):
    r'".+"'
    return t

def t_ID(t):
    r'[a-zA-Z][a-zA-Z_0-9]*|_[a-zA-Z0-9]\w*'
    return t


