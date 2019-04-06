class Node(object):
    pass


class IntNum(Node):
    def __init__(self, value):
        self.value = value


class FloatNum(Node):
    def __init__(self, value):
        self.value = value


class Variable(Node):
    def __init__(self, name):
        self.name = name


class BinExpr(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

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
    def __index__(self, instr):
        self.instr = instr


class Matrix(Node):
    def __init__(self):
        self.rows = []

    def add_row(self, row):
        self.rows.append(row)



# ...
# fill out missing classes
# ...

class Error(Node):
    def __init__(self):
        pass
