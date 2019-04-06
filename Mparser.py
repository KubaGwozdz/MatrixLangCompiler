#!/usr/bin/python

import scanner
import ply.yacc as yacc
import AST

tokens = scanner.tokens

precedence = (
    ("nonassoc", 'IF'),
    ("nonassoc", 'ELSE'),
    ("nonassoc", 'ADDASSIGN', 'SUBASSIGN', 'MULASSIGN', 'DIVASSIGN'),
    ("right", '='),
    ("nonassoc", 'SMALLEREQ', 'GREATEREQ', 'NOTEQ', 'EQ'),
    ("left", '+', '-'),
    ("left", 'MATRIX_PLUS', 'MATRIX_MINUS'),
    ("left", '*', '/'),
    ("left", 'MATRIX_TIMES', 'MATRIX_DIVIDE')

)


def p_error(p):
    if p:
        print("Syntax error at line {0} : LexToken({1}, '{2}')".format(p.lineno, p.type, p.value))
    else:
        print("Unexpected end of input")


def p_program(p):
    """program : instructions_opt"""
    p[0] = p[1]


#------ instructions: ------
def p_instructions_opt(p):
    """instructions_opt : instructions
                        | """
    p[0] = p[1]


def p_instructions(p):
    """instructions : instructions instruction
                    | instruction """


def p_instr_opt(p):
    """instr_opt : '{' instructions '}'
                 | instruction"""


def p_instruction(p):
    """instruction : print_instr
                   | if_instr
                   | for_instr
                   | while_instr
                   | break_instr
                   | cont_instr
                   | return_instr
                   | assignment
                   | range_instr
                   | '{' instructions '}' """
    if(p[1] == '{'):
        expr = p[2]
        p[0] = AST.CompoundInstr(expr)
    else:
        p[0] = p[1]


def p_print_instr(p):
    """print_instr : PRINT expression ';'
                   | PRINT multi_print ';'"""
    p[0] = AST.PrintInstr(p[2])



def p_multi_print(p):
    """multi_print : expression ',' multi_print
                   | expression"""
    if(len(p) > 2):
        p[0] = p[1].append(p[3])
    else:
        p[0] = p[1]


def p_if_instr(p):
    """if_instr  : IF  '(' condition ')' instr_opt
                 | IF  '(' condition ')' instr_opt ELSE if_instr
                 | IF  '(' condition ')' instr_opt ELSE instr_opt"""
    if(len(p) > 6):
        p[0] = AST.IfInstr(p[3], p[5], p[7])
    else:
        p[0] = AST.IfInstr(p[3], p[5])


def p_for_instr(p):
    """for_instr : FOR ID '=' range_instr instr_opt"""
    p[0] = AST.ForInstr(p[2], p[4], p[5])



def p_while_instr(p):
    """while_instr : WHILE '(' condition ')' instr_opt"""
    p[0] = AST.WhileInstr(p[3], p[5])


def p_break_instr(p):
    """break_instr : BREAK ';' """
    p[0] = AST.BreakInstr()


def p_cont_instr(p):
    """cont_instr : CONTINUE ';' """
    p[0] = AST.ContinueInstr()


def p_return_instr(p):
    """return_instr : RETURN expression ';'"""
    p[0] = AST.ReturnInstr(p[2])


def p_eye_instr(p):
    """eye_instr : EYE '(' INTNUM ')'"""


def p_zeros_instr(p):
    """zeros_instr : ZEROS '(' INTNUM ')' """


def p_ones_instr(p):
    """ones_instr : ONES '(' INTNUM ')' """


def p_assignment(p):
    """assignment : ID assign_ops matrix ';'
                  | ID assign_ops expression ';'
                  | ID '[' INTNUM ',' INTNUM ']' assign_ops NUMBER ';' """


def p_assign_ops(p):
    """assign_ops : SUBASSIGN
                  | ADDASSIGN
                  | DIVASSIGN
                  | MULASSIGN
                  | '=' """


def p_range_instr(p): # var_or_id -> var\ id
    """range_instr : INTNUM ':' INTNUM
                   | INTNUM ':' ID
                   | ID ':' ID
                   | ID ':' INTNUM"""


def p_condition(p):
    """condition : expression EQ expression
                 | expression NOTEQ expression
                 | expression GREATEREQ expression
                 | expression SMALLEREQ expression
                 | expression '>' expression
                 | expression '<' expression"""


def p_cond_par(p):
    """cond_par : INTNUM
                | FLOATNUM
                | ID
                | matrix"""



#------ expressions: ------

def p_expression_group(p):
    """expression : '(' expression ')'"""
    p[0] = p[2]


def p_binary_operators(p):
    """ expression : expression '+' expression
                   | expression '-' expression
                   | expression '*' expression
                   | expression '/' expression
                   | cond_par
                   | '-' expression
                   | m_expr
                   | STRING
                   | ones_instr
                   | zeros_instr
                   | eye_instr """


def p_factor_number(p):
    """factor : cond_par"""
    p[0] = p[1]


def p_factor_expr(p):
    """factor : '(' expression ')' """
    p[0] = p[2]



#------ matrix parse: ------

def p_matrix(p):
    """matrix : '[' body ']'
              | matrix_transp
              | ID"""
    if len(p) == 4:
        p[0] = [p[2]]
    else:
        p[0] = p[1]


def p_matrix_transp(p):
    """matrix_transp : matrix "'" """


def p_body(p):
    '''body : row
            | rows_with_brackets
            | rows_with_semicolons'''
    p[0] = p[1]


def p_rows_with_brackets(p):
    '''rows_with_brackets : '[' row ']'
                         | '[' row ']' ',' rows_with_brackets'''


def p_rows_with_semicolons(p):
    '''rows_with_semicolons : row
                            | row ';' rows_with_semicolons'''


def p_row(p):
    """row : NUMBER
           | NUMBER ',' row """


def p_number(p):
    """NUMBER : INTNUM
              | FLOATNUM"""



#------ matrix operations: ------

def p_matrix_matrix_operations(p): #zamiast matrix expression
    '''m_expr : matrix MATRIX_PLUS matrix
              | matrix MATRIX_MINUS matrix
              | matrix MATRIX_TIMES matrix
              | matrix MATRIX_DIVIDE matrix'''



parser = yacc.yacc(start='program')
