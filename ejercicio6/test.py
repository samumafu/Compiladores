from antlr4 import *
from Saludo2Lexer import Saludo2Lexer
from Saludo2Parser import Saludo2Parser

# Entrada de prueba
input_stream = InputStream("buenosdias Pedro")

# Crear lexer
lexer = Saludo2Lexer(input_stream)

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
parser = Saludo2Parser(token_stream)

# Regla inicial
tree = parser.saludo()

print("\nÁRBOL SINTÁCTICO:")
print(tree.toStringTree(recog=parser))