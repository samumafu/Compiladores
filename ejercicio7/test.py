from antlr4 import *
from ListaNumerosLexer import ListaNumerosLexer
from ListaNumerosParser import ListaNumerosParser

input_stream = InputStream("1 2 3 5 10 15")

lexer = ListaNumerosLexer(input_stream)
token_stream = CommonTokenStream(lexer)
token_stream.fill()

print("TOKENS:")

for token in token_stream.tokens:
    if token.type != Token.EOF:
        token_name = lexer.symbolicNames[token.type]

        if token_name is None:
            token_name = lexer.literalNames[token.type]

        print(f"Texto: {token.text}  Tipo: {token_name}")

parser = ListaNumerosParser(token_stream)

tree = parser.lista()

print("\nÁRBOL SINTÁCTICO:")
print(tree.toStringTree(recog=parser))