#!/usr/bin/python
from collections import defaultdict
import AST
from SymbolTable import *

MATRIX_TYPE = "matrix"

ttype = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: None)))
for op in ['+', '-', '*', '/', '%', '<', '>', '<<', '>>', '|', '&', '^', '<=', '>=', '==', '!=']:
    ttype[op]['int']['int'] = 'int'

for op in ['+', '-', '*', '/']:
    ttype[op]['int']['float'] = 'float'
    ttype[op]['float']['int'] = 'float'
    ttype[op]['float']['float'] = 'float'

for op in ['<', '>', '<=', '>=', '==', '!=']:
    ttype[op]['int']['float'] = 'int'
    ttype[op]['float']['int'] = 'int'
    ttype[op]['float']['float'] = 'int'

ttype['+']['string']['string'] = 'string'
ttype['*']['string']['int'] = 'string'

for op in ['<', '>', '<=', '>=', '==', '!=']:
    ttype[op]['string']['string'] = 'int'


class NodeVisitor(object):

    def visit(self, node, table=None):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node, table)

    def generic_visit(self, node, table):  # Called if no explicit visitor function exists for a node.
        if isinstance(node, list):
            for elem in node:
                self.visit(elem, table)
        else:
            for child in node.children:
                if isinstance(child, list):
                    for item in child:
                        if isinstance(item, AST.Node):
                            self.visit(item, table)
                elif isinstance(child, AST.Node):
                    self.visit(child, table)
                else:
                    print(node)

    # simpler version of generic_visit, not so general
    # def generic_visit(self, node):
    #    for child in node.children:
    #        self.visit(child)


class TypeChecker(NodeVisitor):
    def __init__(self):
        self.isValid = True

    def visit_Program(self, node, table):
        table = SymbolTable(None,'root')
        self.visit(node.instructions, table)

    def visit_InstructionList(self, node, table):
        self.visit(node.instructions, table)

    def visit_IntNum(self, node, table):
        return 'int'

    def visit_FloatNum(self, node, table):
        return 'float'

    def visit_String(self, node, table):
        return 'String'

    def visit_Variable(self, node, table):
        '''table.put(node.name, VariableSymbol(node.name, node.type))
        return node.type'''
        definition = table.getGlobal(node.name)
        if definition is None:
            self.isValid = False
            print("Undefined symbol {} in line {}".format(node.name, node.line))
        else:
            return definition.type

    def visit_BinExpr(self, node, table):       #TODO: czemu linia z parsera = 0?
        lhs = self.visit(node.left)
        rhs = self.visit(node.right)
        op = node.op
        if ttype[op][lhs][rhs] is None:
            self.isValid = False
            print("Bad expression {} in line {}".format(node.op, node.line))
        return ttype[op][lhs][rhs]

    def visit_NegatedExpr(self, node, table):
        pass

    '''def visit_RelExpr(self, node, table):
        pass'''

    def visit_AssInstr(self, node, table):
        definition = table.getGlobal(node.left)
        type = self.visit(node.right)
        if definition is None:
            table.put(node.left, VariableSymbol(node.left, type))
        elif type != definition.type and (definition.type != "float" and definition != "int" and definition != "string"):
            self.isValid = False
            print("Bad assignment of {} to {} in line {}.".format(type, definition.type, node.line))


    def visit_AssTabInstr(self, node, table):
        definition = table.getGlobal(node.left)
        #type = self.visit(node.right)
        if definition is None:
            self.isValid = False
            print("Trying to modify unknown matrix: {} in line {}.".format(node.left, node.line))


    def visit_RangeInstr(self, node, table):
        frm_t = self.visit(node.frm)
        to_t = self.visit(node.to)
        if frm_t != to_t:
            node.isValid = False
            print("Unmatching range types of: {} in line {}.".format(node.left, node.parent.line))
        return frm_t

    def visit_CondInstr(self, node, table):
        type_l = self.visit(node.expr_l, table)
        type_r = self.visit(node.expr_r, table)
        if ttype[node.op][type_l][type_r] is None:
            self.isValid = False
            return(False,"Trying to compare: {} and {} ".format(type_l, type_r))
        else:
            return True,""

    def visit_IfInstr(self, node, table):
        state, msg = self.visit(node.cond, table)
        if state == False:
            print(msg + "in line {}.".format(node.line))
        self.visit(node.instr1, table)
        if node.instr2 is not None:
            self.visit(node.instr2, table)


    def visit_WhileInstr(self, node, table):
        state, msg = self.visit(node.cond, table)
        if state == False:
            print(msg + "in line {}.".format(node.line))
        self.visit(node.instr, table)

    def visit_ForInstr(self, node, table):
        id_t = table.getGlobal(node.id)
        range_t = self.visit(node.range)
        if id_t is not None:
            print("Iterator {} already in use, line: ".format(node.id, node.line))
        else:
            table.put(node.id, VariableSymbol(node.id, range_t))

        self.visit(node.instr, table)




    def visit_BreakInstr(self, node, table):
        pass

    def visit_ContinueInstr(self, node, table):
        pass

    def visit_ReturnInstr(self, node, table):
        pass

    def visit_PrintInstr(self, node, table):
        return self.visit(node.instructions, table)

    def visit_EyeInstr(self, node, table):
        pass

    def visit_ZerosInstr(self, node, table):
        pass

    def visit_OnesInstr(self, node, table):
        pass

    def visit_Matrix(self, node, table):
        pass

    def visit_MatrixTransp(self, node, table):
        pass

    def visit_Matrix_bin_ops(self, node, table):
        pass

    def visit_Error(self, node, table):
        pass
