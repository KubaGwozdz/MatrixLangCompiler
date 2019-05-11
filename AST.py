class Node(object):
    def __init__(self,parent=None):
        self.parent = parent

    def __str__(self):
        return self.printTree()

    def accept(self, visitor, table=None):
        return visitor.visit(self)

    def setParent(self, parent):
        self.parent = parent


class Program(Node):
    def __init__(self, instructions):
        self.instructions = instructions
        super().__init__()


class InstructionList(Node):
    def __init__(self):
        self.instructions = []
        self.children = []
        super().__init__()

    def add_instruction(self, instr):
        self.instructions.append(instr)
        self.children.append(instr)
        super().__init__()


class IntNum(Node):
    def __init__(self, value, line):
        self.value = value
        self.line = line
        super().__init__()


class FloatNum(Node):
    def __init__(self, value, line):
        self.value = value
        self.line = line
        super().__init__()


class String(Node):
    def __init__(self, val, line):
        self.val = val
        self.line = line
        super().__init__()


class Variable(Node):
    def __init__(self, name, line):
        self.name = name
        self.line = line
        super().__init__()


class BinExpr(Node):
    def __init__(self, op, left, right, line):
        self.op = op
        self.left = left
        self.right = right
        self.line = line
        super().__init__()


class NegatedExpr(Node):
    def __init__(self, expr):
        self.expr = expr
        super().__init__()


class RelExpr(Node):
    def __init__(self, op, left, right, line):
        self.op = op
        self.left = left
        self.right = right
        self.line = line
        super().__init__()


class AssInstr(Node):
    def __init__(self, op, left, right, line):
        self.op = op
        self.left = left
        self.right = right
        self.line = line
        super().__init__()


class AssTabInstr(Node):
    def __init__(self, op, left, frm, to, right, line):
        self.op = op
        self.left = left
        self.frm = frm
        self.to = to
        self.right = right
        self.line = line
        super().__init__()


class RangeInstr(Node):
    def __init__(self, frm, to):
        self.frm = frm
        self.to = to
        super().__init__()


class CondInstr(Node):
    def __init__(self, expr_l, op, expr_r):
        self.expr_l = expr_l
        self.expr_r = expr_r
        self.op = op
        super().__init__()


class IfInstr(Node):
    def __init__(self, line, cond, instr1, instr2=None):
        self.line = line
        self.cond = cond
        self.instr1 = instr1
        self.instr2 = instr2
        super().__init__()


class WhileInstr(Node):
    def __init__(self, cond, instr, line):
        self.cond = cond
        self.instr = instr
        self.line = line
        super().__init__()


class ForInstr(Node):
    def __init__(self, id, range, instr, line):
        self.id = id
        self.range = range
        self.instr = instr
        self.line = line
        super().__init__()


class BreakInstr(Node):
    def __init__(self, line):
        self.line = line
        super().__init__()


class ContinueInstr(Node):
    def __init__(self, line):
        self.line = line
        super().__init__()


class ReturnInstr(Node):
    def __init__(self, expr, line):
        self.expr = expr
        self.line = line
        super().__init__()


class PrintInstr(Node):
    def __init__(self, expr, line):
        self.expr = expr
        self.line = line
        super().__init__()


#class CompoundInstr(Node):
#    def __init__(self, instr):
#        self.instr = instr


class EyeInstr(Node):
    def __init__(self, intnum, line):
        self.intnum = intnum
        self.line = line
        super().__init__()


class ZerosInstr(Node):
    def __init__(self, intnum, line):
        self.intnum = intnum
        self.line = line
        super().__init__()


class OnesInstr(Node):
    def __init__(self, intnum, line):
        self.intnum = intnum
        self.line = line
        super().__init__()


class Matrix(Node):
    def __init__(self, body, line):
        self.body = body
        self.line = line
        super().__init__()


class MatrixTransp(Node):
    def __init__(self, matrix):
        self.matrix = matrix
        super().__init__()


class Matrix_bin_ops(Node):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right
        super().__init__()

"""
class Error(Node):
    def __init__(self, lineno=None, type=None, value=None):
        self.lineno = lineno
        self.type = type
        self.value = value
        super().__init__()
"""