import sys
import ply.lex as lex
import scanner  # scanner.py is a file you create, (it is not an external library)
import ply.yacc as yacc
from Mparser import Mparser
from TreePrinter import TreePrinter


if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "example4.txt"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    Mparser = Mparser()
    parser = yacc.yacc(module=Mparser)
    text = file.read()
    parser.parse(text, lexer=Mparser.scanner)



"""
if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "example3.txt"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    text = file.read()
    lexer = scanner.lexer
    lexer.input(text)  # Give the lexer some input
    par = parser.parser
    par.parse(text,lexer=lexer)

    # Tokenize
    while True:
        tok = lexer.token()
        if not tok:
            break  # No more input
        column = scanner.find_column(text, tok)
        print("(%d,%d): %s (%s)" % (tok.lineno, column, tok.type, tok.value))
"""
