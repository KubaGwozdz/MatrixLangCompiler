#!/usr/bin/python
import ply.lex as lex
import ply.yacc as yacc


class Scanner(object):

    def build(self):
        self.lexer = lex.lex(object = self)

    def input(self, text):
        self.lexer.input(text)

    def token(self):
        return self.lexer.token()


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
               'ADDASSIGN', 'SUBASSIGN',
               'DIVASSIGN', 'MULASSIGN',
               'SMALLEREQ', 'GREATEREQ', 'NOTEQ', 'EQ',
              'FLOATNUM', 'INTNUM', 'ID', 'STRING'] + list(reserved.values())

    t_MATRIX_PLUS    = r'\.\+'
    t_MATRIX_MINUS   = r'\.\-'
    t_MATRIX_TIMES   = r'\.\*'
    t_MATRIX_DIVIDE  = r'\.\/'
    t_ADDASSIGN      = r'\+='
    t_SUBASSIGN      = r'\-='
    t_MULASSIGN      = r'\*='
    t_DIVASSIGN      = r'/='
    t_SMALLEREQ      = r'<='
    t_GREATEREQ      = r'>='
    t_NOTEQ          = r'!='
    t_EQ             = r'=='


    literals = "+-*/()[]{}=:',;<>"

    # [0-9]+.[0-9]+
    #\d+\.\d*|.\d+
    def t_FLOATNUM(self, t):
        r'\d*((\d\.|\.\d)\d*([Ee][+-]?\d+)?|\d([Ee][+-]?\d+))'
        t.value = float(t.value)
        return t

    # [0-9]+
    def t_INTNUM(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    # "whatever 123"
    def t_STRING(self, t):
        r'".+?"'        #[^\"]+
        return t

    # begnis with a letter or _ (_123whatever | whatever)
    def t_ID(self, t):
        r'[_a-zA-Z]\w*'
        t.type = Scanner.reserved.get(t.value,'ID')
        return t


    t_ignore = ' \t'
    t_ignore_COMMENT = r'\#.*'

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)


    def t_error(self, t) :
        print("Illegal character ", t.value[0])
        t.lexer.skip(1)


    # Compute column.
    #     input is the input text string (our file)
    #     token is a token instance
    def find_column(input, token):
        line_start = input.rfind('\n', 0, token.lexpos) + 1
        return (token.lexpos - line_start) + 1


