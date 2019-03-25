#!/usr/bin/python

import scanner
import ply.yacc as yacc

tokens = scanner.tokens

precedence = (
    # to fill ...
    ("right", "="),
    ("left", '+', '-'),
    ("left", '*', '/')
    # to fill ...
)


def p_error(p):
    if p:
        print("Syntax error at line {0} : LexToken({1}, '{2}')".format(p.lineno, p.type, p.value))
    else:
        print("Unexpected end of input")


def p_program(p):
    """program : instructions_opt"""


def p_instructions_opt_1(p):
    """instructions_opt : instructions """


def p_instructions_opt_2(p):
    """instructions_opt : """


def p_instructions_1(p):
    """instructions : instructions instruction """


def p_instructions_2(p):
    """instructions : instruction """


def p_matrix(p):
    """matrix               : '[' body ']'
       body                 : row
                            | rows_with_brackets
                            | rows_with_semicolons
       rows_with_brackes    : '[' row ']'
                            |'[' row ']' ',' rows
       rows_with_semicolons : row
                            | row ';' rows
       row                  : number
                            | number ',' row"""



def p_body(p):

def p_rows_with_brackets(p):


def p_rows_with_semicolons(p):


def p_row(p):


def p_binary_operators(p):
    '''expression : expression '+' term
                  | expression '-' term
       term       : term '*' factor
                  | term '/' factor'''

    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]
    elif p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        p[0] = p[1] / p[3]


def p_matrix_operators(p):
    ''''''


# to finish the grammar
# ....


parser = yacc.yacc()
