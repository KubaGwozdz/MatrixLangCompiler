import AST
import SymbolTable
from Memory import *
from Exceptions import  *
from visit import *
import sys
import copy

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
        if isinstance(r1,list):
            r3 = copy.deepcopy(r1)
            for i in range(len(r1)):
                for j in range(len(r1[0])):
                    r3[i][j] = AST.IntNum(eval("a" + node.op + "b", {"a": r1[i][j].accept(self), "b": r2}),node.line)
            return r3
        elif isinstance(r2,list):
            r3 = r2
            for i in range(len(r2)):
                for j in range(len(r2[0])):
                    r3[i][j] = AST.IntNum(eval("a" + node.op + "b", {"a": r1, "b": r2[i][j].accept(self)}),node.line)
            return r3
        else:
            return eval("a" + node.op + "b", {"a": r1, "b": r2})

    @when(AST.NegatedExpr)
    def visit(self,node):
        val = node.expr.accept(self)
        return eval("-" + str(val))

    @when(AST.AssInstr)
    def visit(self, node):
        r_val = node.right.accept(self)
        if node.op == "=":
            self.memoryStack.insert(node.left.name, copy.deepcopy(r_val))
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
            proceed = True
            for it in my_range:
                self.memoryStack.set(it_name, it)
                if proceed:
                    for instruction in my_instructions:
                        try:
                            instruction.accept(self)
                        except BreakException:
                            proceed = False
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
        if isinstance(matrix[row][col].accept(self),int):
            matrix[row][col] = AST.IntNum(expr_accept,line)
        elif isinstance(matrix[row][col].accept(self), float):
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
        matrix = node.matrix.accept(self)
        result = copy.deepcopy(matrix)
        size = len(matrix)
        for row in range(size):
            for column in range(size):
                result[row][column] = matrix[column][row]
        return result


    @when(AST.Matrix_bin_ops)
    def visit(self, node):
        r1 = node.left.accept(self)
        r2 = node.right.accept(self)
        result = copy.deepcopy(r1)
        r_size = len(r1)
        c_size = len(r1[0])
        if node.op == ".+":
            for row in range(r_size):
                for col in range(c_size):
                    result[row][col].value += r2[row][col].accept(self)
            return result
        elif node.op == ".-":
            for row in range(r_size):
                for col in range(c_size):
                    result[row][col].value -= r2[row][col].accept(self)
            return result
        elif node.op == ".*":
            result = []
            for row in range(r_size):
                result.append([])
                for col in range(r_size):
                    result[row].append(AST.IntNum(0,0))
            for row in range(r_size):
                for col in range(r_size):
                    for el in range(c_size):
                        result[row][col].value += r1[row][el].accept(self) * r2[el][col].accept(self)
            return result
        elif node.op == "./":
            for row in range(r_size):
                for col in range(c_size):
                    result[row][col].value /= r2[row][col].accept(self)
            return result

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
        eye = 0
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



