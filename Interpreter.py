import AST
import SymbolTable
from Memory import *
from Exceptions import  *
from visit import *
import sys

sys.setrecursionlimit(10000)

class Interpreter(object):


    @on('node')
    def visit(self, node):
        pass

    @when(AST.BinExpr)
    def visit(self, node):
        r1 = node.left.accept(self)
        r2 = node.right.accept(self)
        # try sth smarter than:
        # if(node.op=='+') return r1+r2
        # elsif(node.op=='-') ...
        # but do not use python eval

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