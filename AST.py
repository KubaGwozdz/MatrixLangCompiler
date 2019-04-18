class Node(object):
    def __str__(self):
        return self.printTree()


class Program(Node):
    def __init__(self, instructions):
        self.instructions = instructions


class InstructionList(Node):
    def __init__(self):
        self.instructions = []

    def add_instruction(self, instr):
        self.instructions.append(instr)


class IntNum(Node):
    def __init__(self, value):
        self.value = value


class FloatNum(Node):
    def __init__(self, value):
        self.value = value


class String(Node):
    def __init__(self, val):
        self.val = val


class Variable(Node):
    def __init__(self, name):
        self.name = name


class BinExpr(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right


class NegatedExpr(Node):
    def __init__(self, expr):
        self.expr = expr


class RelExpr(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right


class AssInstr(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right


class AssTabInstr(Node):
    def __init__(self, op, left, frm, to, right):
        self.op = op
        self.left = left
        self.frm = frm
        self.to = to
        self.right = right


class RangeInstr(Node):
    def __init__(self, frm, to):
        self.frm = frm
        self.to = to


class CondInstr(Node):
    def __init__(self, expr_l, op, expr_r):
        self.expr_l = expr_l
        self.expr_r = expr_r
        self.op = op


class IfInstr(Node):
    def __init__(self, cond, instr1, instr2 = None):
        self.cond = cond
        self.instr1 = instr1
        self.instr2 = instr2


class WhileInstr(Node):
    def __init__(self, cond, instr):
        self.cond = cond
        self.instr = instr


class ForInstr(Node):
    def __init__(self, id, range, instr):
        self.id = id
        self.range = range
        self.instr = instr


class BreakInstr(Node):
    pass


class ContinueInstr(Node):
    pass


class ReturnInstr(Node):
    def __init__(self, expr):
        self.expr = expr


class PrintInstr(Node):
    def __init__(self, expr):
        self.expr = expr


class CompoundInstr(Node):
    def __init__(self, instr):
        self.instr = instr


class EyeInstr(Node):
    def __init__(self, intnum):
        self.intnum = intnum


class ZerosInstr(Node):
    def __init__(self, intnum):
        self.intnum = intnum


class OnesInstr(Node):
    def __init__(self, intnum):
        self.intnum = intnum


class Matrix(Node):
    def __init__(self, body):
        self.body = body


class MatrixTransp(Node):
    def __init__(self, matrix):
        self.matrix = matrix


class Matrix_bin_ops(Node):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right


class Error(Node):
    def __init__(self, lineno=None, type=None, value=None):
        self.lineno = lineno
        self.type = type
        self.value = value
