from antlr4 import *
from SumaRestaLexer import SumaRestaLexer
from SumaRestaParser import SumaRestaParser

# Entrada de prueba
input_stream = InputStream("5+3")

# Crear lexer
lexer = SumaRestaLexer(input_stream)

# Crear stream de tokens
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

# Crear parser
parser = SumaRestaParser(token_stream)

# Regla inicial
tree = parser.expr()

print("\nÁRBOL SINTÁCTICO:")
print(tree.toStringTree(recog=parser))