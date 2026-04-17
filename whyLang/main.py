import sys
from antlr4 import *
from WhileLangLexer import WhileLangLexer
from WhileLangParser import WhileLangParser
from SemanticVisitor import SemanticVisitor

def main():
    if len(sys.argv) < 2:
        print("Uso: python main.py <archivo>")
        return

    input_file = sys.argv[1]

    input_stream = FileStream(input_file)
    lexer = WhileLangLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = WhileLangParser(stream)

    tree = parser.program()

    visitor = SemanticVisitor()
    visitor.visit(tree)

if __name__ == '__main__':
    main()