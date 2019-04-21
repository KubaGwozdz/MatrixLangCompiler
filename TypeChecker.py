#!/usr/bin/python
import AST
from SymbolTable import *


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

    # simpler version of generic_visit, not so general
    # def generic_visit(self, node):
    #    for child in node.children:
    #        self.visit(child)


class TypeChecker(NodeVisitor):

    def visit_Program(self,node, table):
        symbolTable = SymbolTable(None,'global')
        self.visit(node.instructions, symbolTable)

    def visit_InstructionList(self, node, table):
        self.visit(node.instructions, table)

    def visit_IntNum(self, node, table):
        table.put('int', node.value)

    def visit_FloatNum(self, node, table):
        table.put('float', node.value)

    def visit_String(self, node, table):
        table.put('string', node.val)

    def visit_Variable(self, node, table):
        table.put('var', node.name)

    def visit_BinExpr(self, node, table):
        # alternative usage,
        # requires definition of accept method in class Node
        type1 = self.visit(node.left, table)  # type1 = node.left.accept(self)
        type2 = self.visit(node.right, table)  # type2 = node.right.accept(self)
        table.put('var', node.op)
        # ...
        #

    def visit_NegatedExpr(self, node, table):
        pass

    def visit_RelExpr(self, node, table):
        pass

    def visit_AssInstr(self, node, table):
        pass

    def visit_AssTabInstr(self, node, table):
        pass

    def visit_RangeInstr(self, node, table):
        pass

    def visit_CondInstr(self, node, table):
        pass

    def visit_IfInstr(self, node, table):
        pass

    def visit_WhileInstr(self, node, table):
        pass

    def visit_ForInstr(self, node, table):
        pass

    def visit_BreakInstr(self, node, table):
        pass

    def visit_ContinueInstr(self, node, table):
        pass

    def visit_ReturnInstr(self, node, table):
        pass

    def visit_PrintInstr(self, node, table):
        return self.visit(node.instructions, table)

    def visit_EyeInstr(self, node, table):
        pass

    def visit_ZerosInstr(self, node, table):
        pass

    def visit_OnesInstr(self, node, table):
        pass

    def visit_Matrix(self, node, table):
        pass

    def visit_MatrixTransp(self, node, table):
        pass

    def visit_Matrix_bin_ops(self, node, table):
        pass

    def visit_Error(self, node, table):
        pass
