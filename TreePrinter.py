import AST


INDENT_TOKEN = "| "


def addToClass(cls):
    def decorator(func):
        setattr(cls,func.__name__,func)
        return func
    return decorator


class TreePrinter:

    @addToClass(AST.Node)
    def printTree(self, indent=0):
        raise Exception("printTree not defined in class " + self.__class__.__name__)

    @addToClass(AST.InstructionList)
    def printTree(self, indent=0):
        pass

    @addToClass(AST.IntNum)
    def printTree(self, indent=0):
        return INDENT_TOKEN * indent + str(self.value) + "\n"

    @addToClass(AST.FloatNum)
    def printTree(self, indent=0):
        return INDENT_TOKEN * indent + str(self.value) + "\n"

    @addToClass(AST.Variable)
    def printTree(self, indent=0):
        return INDENT_TOKEN * indent + str(self.name) + "\n"

    @addToClass(AST.BinExpr)
    def printTree(self, indent=0):
        return INDENT_TOKEN * indent + self.op + "\n" + self.left.printTree(indent + 1) + self.right.printTree(indent + 1)

    @addToClass(AST.RelExpr)
    def printTree(self, indent=0):
        return INDENT_TOKEN * indent + self.op + "\n" + self.left.printTree(indent + 1) + self.right.printTree(indent + 1)

    @addToClass(AST.AssInstr)
    def printTree(self, indent=0):
        return INDENT_TOKEN * indent + self.op + "\n" + self.left.printTree(indent + 1) + self.right.printTree(indent + 1)

    @addToClass(AST.AssTabInstr)
    def printTree(self, indent=0):
        return INDENT_TOKEN * indent + self.op + "\n" + INDENT_TOKEN * (indent+1) + "REF" + "\n" + self.left.printTree(indent+2) + self.frm.printTree(indent+2) + self.to.printTree(indent+2) + self.right.printTree(indent+1)

    @addToClass(AST.RangeInstr)
    def printTree(self, indent=0):
        return INDENT_TOKEN * indent + "RANGE" + "\n" + self.frm.printTree(indent+1) + self.to.printTree(indent+1)

    @addToClass(AST.CondInstr)
    def printTree(self, indent=0):
        return INDENT_TOKEN * indent + self.op + "\n" + self.expr_l.printTree(indent+1) + self.expr_r.printTree(indent+1)

    @addToClass(AST.IfInstr)
    def printTree(self, indent=0):
        if self.instr2 == None:
            return INDENT_TOKEN * indent + "IF" + "\n" + self.cond.printTree(indent+1) + INDENT_TOKEN * indent + "THEN\n" + self.instr1.printTree(indent+1)
        else:
            return INDENT_TOKEN * indent + "IF" + "\n" + self.cond.printTree(indent+1) + INDENT_TOKEN * indent + "THEN\n" + self.instr1.printTree(indent+1) + INDENT_TOKEN * indent + "ELSE" + "\n" + self.instr2.printTree(indent+1)

    @addToClass(AST.WhileInstr)
    def printTree(self, indent=0):
        return INDENT_TOKEN * indent + "WHILE\n" + self.cond.printTree(indent+1) + self.instr.printTree(indent+1)

    @addToClass(AST.ForInstr)
    def printTree(self, indent=0):
        return INDENT_TOKEN * indent + "FOR\n" + self.id.printTree(indent+1) + self.range.printTree(indent+1) + self.instr.printTree(indent+1)

    @addToClass(AST.BreakInstr)
    def printTree(self, indent=0):
        return INDENT_TOKEN * indent + "BREAK\n"

    @addToClass(AST.ContinueInstr)
    def printTree(self, indent=0):
        return INDENT_TOKEN * indent + "CONTINUE\n"

    @addToClass(AST.ReturnInstr)
    def printTree(self, indent=0):
        return INDENT_TOKEN * indent + "RETURN\n" + self.expr.printTree(indent+1)

    @addToClass(AST.PrintInstr)
    def printTree(self, indent=0):
        return INDENT_TOKEN * indent + "PRINT\n" + self.expr.printTree(indent+1)

    @addToClass(AST.CompoundInstr)
    def printTree(self, indent=0):
        return INDENT_TOKEN * indent + "COMPOUND\n" + self.instr.printTree(indent+1)

    @addToClass(AST.EyeInstr)
    def printTree(self, indent=0):
        return INDENT_TOKEN * indent + "EYE\n" + self.intnum.printTree(indent+1)

    @addToClass(AST.ZerosInstr)
    def printTree(self, indent=0):
        return INDENT_TOKEN * indent + "ZEROS\n" + self.intnum.printTree(indent+1)

    @addToClass(AST.OnesInstr)
    def printTree(self, indent=0):
        return INDENT_TOKEN * indent + "ONES\n" + self.intnum.printTree(indent+1)

    @addToClass(AST.Matrix)
    def printTree(self, indent=0):
        return INDENT_TOKEN * indent + "VECTOR\n" + self.body.printTree(indent+1)

    @addToClass(AST.MatrixTransp)
    def printTree(self, indent=0):
        return INDENT_TOKEN * indent + "TRANSPOSE\n" + self.matrix.printTree(indent+1)

    @addToClass(AST.Matrix_bin_ops)
    def printTree(self, indent=0):
        return INDENT_TOKEN * indent + self.op + "\n" + self.left.printTree(indent+1) + self.right.printTree(indent+1)

    @addToClass(AST.Program)
    def printTree(self, indent=0):
        return self.instructions.printTree(indent+1)

    @addToClass(AST.Error)
    def printTree(self, indent=0):
        return INDENT_TOKEN * indent + "Syntax error at line" + str(self.lineno) + str(self.type) + " " + str(self.value) + "\n\n"