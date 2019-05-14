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
        r_val = node.right.accept(self)
        if node.op == "=":
            self.memoryStack.insert(node.left.name, r_val)
            return r_val
        else:
            val = node.left.accept(self)
            if node.op == "-=":
                val -= r_val
            elif node.op == "*=":
                val *= r_val
            elif node.op == "/=":
                val /= r_val
            elif node.op == "+=":
                val += r_val
            self.memoryStack.set(node.left.name, val)
            return val

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
            my_instructions = []
            if hasattr(node.instr, "instructions"):
                my_instructions = node.instr.instructions
            else:
                my_instructions.append(node.instr)
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

    @when(AST.AssTabInstr)
    def visit(self,node):
        expr_accept = node.right.accept(self)
        matrix = self.memoryStack.get(node.left.name)
        row = node.frm.accept(self)
        col = node.to.accept(self)
        line = matrix[row][col].line
        if isinstance(matrix[row][col].value,int):
            matrix[row][col] = AST.IntNum(expr_accept,line)
        elif isinstance(matrix[row][col].value, float):
            matrix[row][col] = AST.FloatNum(expr_accept, line)
        self.memoryStack.insert(node.left.name, expr_accept)
        self.memoryStack.set(node.left.name, matrix)
        return expr_accept

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
            ex = expr.accept(self)
            if type(ex) == list:
                for row in ex:
                    for val in row:
                        print(str(val.accept(self)), end=', ')
                    print()
                print()
            else:
                print(ex)

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


# ------------  Matrix  ------------

    @when(AST.Matrix)
    def visit(self,node):
        return node.body

    @when(AST.MatrixTransp)
    def visit(self, node):
        return node.matrix

    @when(AST.Matrix_bin_ops)
    def visit(self, node):
        r1 = node.left.accept(self)
        r2 = node.right.accept(self)
        r3 = r1
        if node.op == ".+":
            for row in r2:
                for col in row:
                    r3[row][col].value += r2[row][col].accept(self) #?
            return r3
        elif node.op == ".-":
            for row in r2:
                for col in row:
                    r3[row][col].value -= r2[row][col].value
            return r3
        elif node.op == ".*":
            for row in r3:
                for col in r3:
                    r3[row][col].value = 0
            for row in r1:
                for col in r1:
                    r3[row][col].value += r1[row][col].value * r2[col][row].value
            return r3
        elif node.op == "./":
            r1 += r2
        else:
            return eval("a" + node.op + "b", {"a": r1, "b": r2})


    @when(AST.ZerosInstr)
    def visit(self, node):
        body = []
        size = node.intnum.accept(self)
        for row in range(size):
            column = [AST.IntNum(0, 0) for x in range(size)]
            body.append(column)
        return body

    @when(AST.OnesInstr)
    def visit(self, node):
        body = []
        size = node.intnum.accept(self)
        for row in range(size):
            column = [AST.IntNum(1, 0) for x in range(size)]
            body.append(column)
        return body

    @when(AST.EyeInstr)
    def visit(self, node):
        body = []
        size = node.intnum.accept(self)
        eye = 0;
        for row in range(size):
            column = []
            for element in range(size):
                if element == eye:
                    column.append(AST.IntNum(1,0))
                else:
                    column.append((AST.IntNum(0,0)))
            eye += 1
            body.append(column)
        return body

    @when(AST.Program)
    def visit(self, node):
        node.instructions.accept(self)

    @when(AST.InstructionList)
    def visit(self, node):
        for instruction in node.instructions:
            instruction.accept(self)



