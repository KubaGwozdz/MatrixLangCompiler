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
        return node.val

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
        val = node.expr.accept(self)
        return eval("-" + str(val))

    @when(AST.AssInstr)
    def visit(self, node):
        expr_accept = node.right.accept(self)
        self.memoryStack.insert(node.left.name, expr_accept)
        return expr_accept

    @when(AST.RangeInstr)
    def visit(self, node):
        return range(node.frm.accept(self), node.to.accept(self))

    @when(AST.ForInstr)
    def visit(self, node):
        my_range = node.range.accept(self)
        it_name = node.id.accept(self)
        if it_name is not None:
            print("for iterator already in use!")
        else:
            it_name = node.id.name
            self.memoryStack.insert(it_name, 0)
            my_instructions = node.instr.instructions
            for it in my_range:
                self.memoryStack.set(it_name, it)
                for instruction in my_instructions:
                    try:
                        instruction.accept(self)
                    except BreakException:
                        break
                    except ContinueException:
                        pass
            self.memoryStack.delete(it_name)

    @when(AST.WhileInstr)
    def visit(self, node):
        while node.cond.accept(self):
            try:
                node.instr.accept(self)
            except BreakException:
                break
            except ContinueException:
                pass

    @when(AST.IfInstr)
    def visit(self, node):
        if node.cond.accept(self):
            node.instr1.accept(self)
        elif node.instr2 is not None:
            node.instr2.accept(self)


    @when(AST.CondInstr)
    def visit(self, node):
        return eval(str(node.expr_l.accept(self)) + node.op + str(node.expr_r.accept(self)))


    @when(AST.PrintInstr)
    def visit(self, node):
        for expr in node.expr:
            print(expr.accept(self))

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



