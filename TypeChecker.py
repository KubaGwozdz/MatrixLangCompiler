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

for op in ['.+','.-','./','.*']:
    ttype[op]['matrix']['matrix'] = 'matrix'

for op in ['+','*']:
    ttype[op]['matrix']['int'] = 'matrix'
    ttype[op]['matrix']['float'] = 'matrix'
    ttype[op]['int']['matrix'] = 'matrix'


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
        definition = table.get(node.name)
        if definition is None:
            return definition
        else:
            return definition.type

    def visit_BinExpr(self, node, table):
        lhs = self.visit(node.left, table)
        rhs = self.visit(node.right, table)
        op = node.op
        if ttype[op][lhs][rhs] is None:
            self.isValid = False
            print("Bad expression {} in line {}".format(node.op, node.left.line))
        return ttype[op][lhs][rhs]

    def visit_NegatedExpr(self, node, table):
        pass

    def visit_AssInstr(self, node, table):
        definition = self.visit(node.left, table)
        type = self.visit(node.right, table)
        if definition is None:
            if type == 'matrix':
                if hasattr(node.right, "body"):
                    table.put(node.left.name, MatrixSymbol(node.left.name, type, len(node.right.body), len(node.right.body[0])))
                else:
                    table.put(node.left.name, MatrixSymbol(node.left.name, type, node.right.intnum, node.right.intnum))
            else:
                table.put(node.left.name, VariableSymbol(node.left.name, type))
        elif type != definition or (definition != "float" and definition != "int" and definition != "string" and definition != "matrix"):
            self.isValid = False
            print("Bad assignment of {} to {} in line {}.".format(type, definition, node.left.line))

    def visit_AssTabInstr(self, node, table):
        definition = self.visit(node.left, table)
        if definition is None:
            self.isValid = False
            print("Trying to modify unknown matrix: {} in line {}.".format(node.left, node.left.line))
        else:
            row, column = table.getMatrixSize(node.left.name)
            if node.frm.value >= row.value:
                self.isValid = False
                print("Row out of matrix bounds: line {}".format(node.left.line))
            if node.to.value >= column.value:
                self.isValid = False
                print("Column out of matrix bounds: line {}".format(node.left.line))

    def visit_RangeInstr(self, node, table):
        frm_t = self.visit(node.frm, table)
        to_t = self.visit(node.to, table)
        if frm_t != to_t:
            self.isValid = False
            print("Unmatching range types of: {} and {} in line {}.".format(frm_t, to_t, node.parent.line))
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
        if type(node.instr) == list:
            for child in node.instr:
                child.setParent(node)
        else:
            node.instr.setParent(node)
        self.visit(node.instr, table)

    def visit_ForInstr(self, node, table):
        temp_var = False
        id_t = self.visit(node.id, table)
        node.range.setParent(node)
        range_t = self.visit(node.range, table)
        if id_t is not None:
            print("Iterator {} already in use, line: {}".format(node.id, node.line))
            self.isValid = False
        else:
            table.put(node.id.name, VariableSymbol(node.id.name, range_t))
            temp_var = True
        if type(node.instr) == list:
            for child in node.instr:
                child.setParent(node)
        else:
            node.instr.setParent(node)
        self.visit(node.instr, table)
        if temp_var:
            table.delete(node.id.name)

    def visit_BreakInstr(self, node, table):
        if node.parent is not None:
            pass
        else:
            print("Break without loop: line {}".format(node.line))
            self.isValid = False

    def visit_ContinueInstr(self, node, table):
        if node.parent is not None:
            pass
        else:
            print("Continue without loop: line {}".format(node.line))
            self.isValid = False

    def visit_ReturnInstr(self, node, table):
        if node.parent is not None:
            pass
        else:
            print("Return without loop: line {}".format(node.line))
            self.isValid = False

    def visit_PrintInstr(self, node, table):
        return self.visit(node.expr, table)

    def visit_EyeInstr(self, node, table):
        type = self.visit(node.intnum, table)
        if type == "int":
            pass
        else:
            print("Wrong argument to eye instruction: line {}".format(node.line))
            self.isValid = False
        return "matrix"


    def visit_ZerosInstr(self, node, table):
        type = self.visit(node.intnum, table)
        if type == "int":
            pass
        else:
            print("Wrong argument to zeros instruction: line {}".format(node.line))
        return "matrix"

    def visit_OnesInstr(self, node, table):
        type = self.visit(node.intnum, table)
        if type == "int":
            pass
        else:
            print("Wrong argument to ones instruction: line {}".format(node.line))
        return "matrix"

    def visit_Matrix(self, node, table):
        length = len(node.body[0])
        for i in node.body:
            if len(i) != length:
                print("Implementing matrix with diffrent size vectors: line {}".format(node.line))
                break
        return "matrix"

    def visit_MatrixTransp(self, node, table):
        type = self.visit(node.matrix, table)
        if type != 'matrix':
            print("Trying to transpose not matrix: line {}".format(node.matrix.line))

    def visit_Matrix_bin_ops(self, node, table):
        lhs = self.visit(node.left,table)
        rhs = self.visit(node.right,table)
        if ttype[node.op][lhs][rhs] is None:
            self.isValid = False
            print("Bad matrix expression {} in line {}".format(node.op, node.left.line))
        else:
            lr,lc = table.getMatrixSize(node.left.name)
            rr,rc = table.getMatrixSize(node.right.name)
            if node.op == '.*':
                if lc != rr:
                    self.isValid = False
                    print("Trying to {} matrixes with wrong sizes in line {}".format(node.op, node.left.line))
            elif node.op == '.+' or node.op == '.-':
                if lc != rc or lr != rr:
                    self.isValid = False
                    print("Trying to {} matrixes with wrong sizes in line {}".format(node.op, node.left.line))
            elif node.op == './':
                if lc != lr or rc != rr:
                    self.isValid = False
                    print("Trying to {} matrixes with wrong sizes in line {}".format(node.op, node.left.line))
        return ttype[op][lhs][rhs]

    '''def visit_Error(self, node, table):
        pass'''
