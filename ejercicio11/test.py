from antlr4 import *
from Expr1Lexer import Expr1Lexer
from Expr1Parser import Expr1Parser

input_stream = InputStream("1+2+3")

lexer = Expr1Lexer(input_stream)
token_stream = CommonTokenStream(lexer)
token_stream.fill()

print("TOKENS:")

for token in token_stream.tokens:
    if token.type != Token.EOF:
        if token.type < len(lexer.symbolicNames) and lexer.symbolicNames[token.type] is not None:
            token_name = lexer.symbolicNames[token.type]
        else:
            token_name = token.text
        print(f"Texto: {token.text}  Tipo: {token_name}")

parser = Expr1Parser(token_stream)

tree = parser.expr()

print("\nÁRBOL SINTÁCTICO:")
print(tree.toStringTree(recog=parser))