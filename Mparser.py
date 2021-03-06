#!/usr/bin/python
from scanner import Scanner
import AST


class Mparser(object):

    def __init__(self):
        self.scanner = Scanner()
        self.scanner.build()

    tokens = Scanner.tokens

    precedence = (
        ("nonassoc", 'IF'),
        ("nonassoc", 'ELSE'),
        ("nonassoc", 'ADDASSIGN', 'SUBASSIGN', 'MULASSIGN', 'DIVASSIGN'),
        ("right", '='),
        ("nonassoc", '<', '>'),
        ("nonassoc", 'SMALLEREQ', 'GREATEREQ', 'NOTEQ', 'EQ'),
        ("left", '+', '-'),
        ("left", 'MATRIX_PLUS', 'MATRIX_MINUS'),
        ("left", '*', '/'),
        ("left", 'MATRIX_TIMES', 'MATRIX_DIVIDE'),
        ("left", '\''),
        ("left", 'UMINUS')
    )

    def p_error(self, p):
        if p:
            print("Syntax error at line {0} : LexToken({1}, '{2}')".format(p.lineno, p.type, p.value))
            #p[0] = AST.Error(p.lineno, p.type, p.value)
        else:
            print("Unexpected end of input")
            #p[0] = AST.Error

    def p_program(self, p):
        """program : instructions_opt"""
        p[0] = AST.Program(p[1])
        print(AST.Program(p[1]))

    #------ instructions: ------
    def p_instructions_opt(self, p):
        """instructions_opt : instructions
                            | """
        p[0] = p[1]

    def p_instructions(self, p):
        """instructions : instructions instruction
                        | instruction """
        if len(p) == 3:
            p[0] = AST.InstructionList() if p[1] is None else p[1]
            p[0].add_instruction(p[2])
        else:
            p[0] = AST.InstructionList()
            p[0].add_instruction(p[1])

    def p_instruction(self, p):
        """instruction : print_instr
                       | if_instr
                       | for_instr
                       | while_instr
                       | break_instr
                       | cont_instr
                       | return_instr
                       | assignment
                       | '{' instructions '}' """
        if (p[1] == '{'):
            p[0] = p[2]
        else:
            p[0] = p[1]

    def p_print_instr(self, p):
        """print_instr : PRINT multi_print ';'"""
        p[0] = AST.PrintInstr(p[2], p.lineno(1))

    def p_multi_print(self, p):
        """multi_print : multi_print ',' expression
                       | expression"""
        if (not isinstance(p[0], list)):
            p[0] = []
        if (len(p) == 4):
            p[0] = p[1]
            p[0].append(p[3])
        else:
            p[0].append(p[1])

    def p_if_instr(self, p):
        """if_instr  : IF  '(' condition ')' instruction
                     | IF  '(' condition ')' instruction ELSE instruction"""
        if(len(p) > 6):
            p[0] = AST.IfInstr(p.lineno(1), p[3], p[5], p[7])
        else:
            p[0] = AST.IfInstr(p.lineno(1), p[3], p[5])

    def p_for_instr(self, p):
        """for_instr : FOR id '=' range_instr instruction"""
        p[0] = AST.ForInstr(p[2], p[4], p[5], p.lineno(1))

    def p_while_instr(self, p):
        """while_instr : WHILE '(' condition ')' instruction"""
        p[0] = AST.WhileInstr(p[3], p[5], p.lineno(1))

    def p_break_instr(self, p):
        """break_instr : BREAK ';' """
        p[0] = AST.BreakInstr(p.lineno(1))

    def p_cont_instr(self, p):
        """cont_instr : CONTINUE ';' """
        p[0] = AST.ContinueInstr(p.lineno(1))

    def p_return_instr(self, p):
        """return_instr : RETURN expression ';'"""
        p[0] = AST.ReturnInstr(p[2],p.lineno(1))

    def p_eye_instr(self, p):
        """eye_instr : EYE '(' int ')'"""
        p[0] = AST.EyeInstr(p[3], p.lineno(1))

    def p_zeros_instr(self, p):
        """zeros_instr : ZEROS '(' int ')' """
        p[0] = AST.ZerosInstr(p[3], p.lineno(1))

    def p_ones_instr(self, p):
        """ones_instr : ONES '(' int ')' """
        p[0] = AST.OnesInstr(p[3], p.lineno(1))

    def p_assignment(self, p):
        """assignment : id assign_ops matrix ';'
                      | id assign_ops expression ';'
                      | id '[' INTNUM ',' INTNUM ']' assign_ops expression ';' """
        if(len(p)<6):
            p[0] = AST.AssInstr(p[2], p[1], p[3], p.lineno(1))
        else:
            p[0] = AST.AssTabInstr(p[7], p[1], AST.IntNum(p[3], p.lineno(1)), AST.IntNum(p[5], p.lineno(1)), p[8], p.lineno(1))

    def p_assign_ops(self, p):
        """assign_ops : SUBASSIGN
                      | ADDASSIGN
                      | DIVASSIGN
                      | MULASSIGN
                      | '=' """
        p[0] = p[1]

    def p_range_instr(self, p):
        """range_instr : int ':' int
                       | int ':' id
                       | id ':' id
                       | id ':' int"""
        p[0] = AST.RangeInstr(p[1],p[3])


    def p_int(self, p):
        """int : INTNUM"""
        p[0] = AST.IntNum(p[1], p.lineno(1))

    def p_float(self, p):
        """float : FLOATNUM"""
        p[0] = AST.FloatNum(p[1], p.lineno(1))

    def p_condition(self, p):
        """condition : expression EQ expression
                     | expression NOTEQ expression
                     | expression GREATEREQ expression
                     | expression SMALLEREQ expression
                     | expression '>' expression
                     | expression '<' expression"""
        p[0] = AST.CondInstr(p[1], p[2], p[3])

    def p_number_or_id(self, p):
        """number_or_id : int
                        | float
                        | id"""
        p[0] = p[1]
        p[0] = p[1]

    #------ expressions: ------

    def p_expression_group(self, p):
        """expression : '(' expression ')'"""
        p[0] = p[2]

    def p_binary_operators(self, p):
        """ expression : expression '+' expression
                       | expression '-' expression
                       | expression '*' expression
                       | expression '/' expression
                       | number_or_id
                       | '-' expression   %prec UMINUS
                       | m_expr
                       | string
                       | ones_instr
                       | zeros_instr
                       | eye_instr
                       | matrix """      #TODO: sprawdzic!!!
        if(len(p) == 4):
            p[0] = AST.BinExpr(p[2], p[1], p[3], p.lineno(1))
        elif(len(p) == 3):
            p[0] = AST.NegatedExpr(p[2])
        else:
            p[0] = p[1]

    def p_string(self, p):
        """ string : STRING"""
        p[0] = AST.String(p[1], p.lineno(1))

    #------ matrix parse: ------

    def p_matrix(self, p):
        """matrix : '[' body ']'
                  | matrix_transp
                  | id"""
        if len(p) == 4:
            p[0] = AST.Matrix(p[2], p.lineno(1))
        else:
            p[0] = p[1]

    def p_id(self, p):
        """id : ID"""
        p[0] = AST.Variable(p[1], p.lineno(1))

    def p_matrix_transp(self, p):
        """matrix_transp : matrix "'" """
        p[0] = AST.MatrixTransp(p[1])

    def p_body(self, p):
        '''body : rows_with_brackets
                | rows_with_semicolons'''
        p[0] = p[1]

    def p_rows_with_brackets(self, p):
        '''rows_with_brackets : '[' row ']'
                              | rows_with_brackets ',' '[' row ']' '''
        if (not isinstance(p[0], list)):
            p[0] = []
        if (len(p) != 4):
            p[0] = p[1]
            p[0].append(p[4])
        else:
            p[0].append(p[2])

    def p_rows_with_semicolons(self, p):
        '''rows_with_semicolons : row
                                | rows_with_semicolons ';' row'''
        if (not isinstance(p[0], list)):
            p[0] = []

        if (len(p) != 2):
            p[0] = p[1]
            p[0].append(p[3])
        else:
            p[0].append(p[1])

    def p_row(self, p):
        """row : NUMBER
               | row ',' NUMBER """
        if(not isinstance(p[0], list)):
            p[0] = []
        if(len(p) != 2):
            p[0] = p[1]
            p[0].append(p[3])
        else:
            p[0].append(p[1])

    def p_number(self, p):
        """NUMBER : int
                  | float"""
        p[0] = p[1]

    #------ matrix operations: ------

    def p_matrix_matrix_operations(self, p): #zamiast matrix expression
        '''m_expr : matrix MATRIX_PLUS matrix
                  | matrix MATRIX_MINUS matrix
                  | matrix MATRIX_TIMES matrix
                  | matrix MATRIX_DIVIDE matrix'''
        p[0] = AST.Matrix_bin_ops(p[1], p[2], p[3])




#parser = yacc.yacc(start='program')
