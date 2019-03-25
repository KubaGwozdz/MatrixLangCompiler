#!/usr/bin/python

import ply.lex as lex;
import ply.yacc as yacc


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

tokens = [] + \
         ['MATRIX_PLUS', 'MATRIX_MINUS', 'MATRIX_TIMES', 'MATRIX_DIVIDE',
           'INCREMENT', 'DECREMENT',
           'MULTIPLY', 'DIVIDE',
           'SMALLEREQ', 'GREATEREQ', 'NOTEQ', 'EQ',
          'FLOATNUM', 'INTNUM', 'ID', 'STRING'] + list(reserved.values())

t_MATRIX_PLUS    = r'\.\+'
t_MATRIX_MINUS   = r'\.\-'
t_MATRIX_TIMES   = r'\.\*'
t_MATRIX_DIVIDE  = r'\.\/'
t_INCREMENT      = r'\+='
t_DECREMENT      = r'\-='
t_MULTIPLY       = r'\*='
t_DIVIDE         = r'/='
t_SMALLEREQ      = r'<='
t_GREATEREQ      = r'>='
t_NOTEQ          = r'!='
t_EQ             = r'=='


literals = "+-*/()[]{}=:',;<>"

# [0-9]+.[0-9]+
def t_FLOATNUM(t):
    r'\d*((\d\.|\.\d)\d*([Ee][+-]?\d+)?|\d([Ee][+-]?\d+))'
    t.value = float(t.value)
    return t

# [0-9]+
def t_INTNUM(t):
    r'\d+'
    t.value = int(t.value)
    return t

# "whatever 123"
def t_STRING(t):
    r'".+?"'        #[^\"]+
    return t

# begnis with a letter or _ (_123whatever | whatever)
def t_ID(t):
    r'[_a-zA-Z]\w*'
    t.type = reserved.get(t.value,'ID')
    return t


t_ignore = ' \t'
t_ignore_COMMENT = r'\#.*'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t) :
    print("Illegal character ", t.value[0])
    t.lexer.skip(1)


# Compute column.
#     input is the input text string (our file)
#     token is a token instance
def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1

lexer = lex.lex()


