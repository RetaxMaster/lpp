from lpp.lexer import Lexer
from lpp.token import (
    Token,
    TokenType
)

EOF_TOKEN: Token = Token(TokenType.EOF, "")


def start_repl():
    
    # Walrus operator, asigna a la vez que compara
    while (source := input(">> ")) != "salir()":
        
        lexer: Lexer = Lexer(source)

        while (token := lexer.next_token()) != EOF_TOKEN:
            
            print(token)