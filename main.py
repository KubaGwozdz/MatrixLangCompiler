import sys
import ply.lex as lex
import scanner  # scanner.py is a file you create, (it is not an external library)
import ply.yacc as yacc
from Mparser import Mparser
from TreePrinter import TreePrinter
from TypeChecker import TypeChecker
from Interpreter import Interpreter



if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "examples/example7.txt"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    Mparser = Mparser()
    parser = yacc.yacc(module=Mparser)
    text = file.read()
    ast = parser.parse(text, lexer=Mparser.scanner)
    typeChecker = TypeChecker()
    typeChecker.visit(ast)
    if typeChecker.isValid:
        print("interpreting...")
        ast.accept(Interpreter())
        print("finished.")
    else:
        print("Errors found..")


