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
    def printTree(self, indent = 0):
        return INDENT_TOKEN * indent + self.op + "\n" + self.left.printTree(indent + 1) + self.right.printTree(indent + 1)













    @addToClass(AST.Error)
    def printTree(self, indent=0):
        return INDENT_TOKEN * indent + "Syntax error at line" + str(self.lineno) + str(self.type) + " " + str(self.value) + "\n\n"



