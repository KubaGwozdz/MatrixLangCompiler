import AST
import SymbolTable
from Memory import *
from Exceptions import  *
from visit import *
import sys

sys.setrecursionlimit(10000)


class Interpreter(object):

    def __init__(self):
        self.memoryStack = MemoryStack()

    @on('node')
    def visit(self, node):
        pass

    @when(AST.IntNum)
    def visit(self,node):
        return int(node.value)

    @when(AST.FloatNum)
    def visit(self, node):
        return float(node.value)

    @when(AST.String)
    def visit(self, node):
        return int(node.val)

    @when(AST.Variable)
    def visit(self, node):
        return self.memoryStack.get(node.name)

    @when(AST.BinExpr)
    def visit(self, node):
        r1 = node.left.accept(self)
        r2 = node.right.accept(self)
        return eval("a" + node.op + "b", {"a": r1, "b": r2})

    @when(AST.NegatedExpr)
    def visit(self,node):
        return 0

    


    @when(AST.AssInstr)
    def visit(self, node):
        return 0
    #
    #

    # simplistic while loop interpretation
    @when(AST.WhileInstr)
    def visit(self, node):
        r = None
        while node.cond.accept(self):
            r = node.body.accept(self)
        return r

    @when(AST.BreakInstr)
    def visit(self, node):
        raise BreakException()

    @when(AST.ContinueInstr)
    def visit(self, node):
        raise ContinueException()

    @when(AST.ReturnInstr)
    def visit(self, node):
        value = node.expression.accept(self)
        raise ReturnValueException(value)

    @when(AST.Program)
    def visit(self, node):
        node.instructions.accept(self)

    @when(AST.InstructionList)
    def visit(self, node):
        for instruction in node.instructions:
            instruction.accept(self)



