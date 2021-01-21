from enum import (
    auto,
    Enum,
    unique,
)

from typing import (
    Dict,
    NamedTuple
)

@unique
class TokenType(Enum):

    ASSIGN = auto()
    COMMA = auto()
    EOF = auto() # Enf Of File
    FUNCTION = auto()
    IDENT = auto() # Identificador
    ILLEGAL = auto() # Cuando un caracter no pertenece al lenguaje
    INT = auto()
    LBRACE = auto() # Llave izquierda {
    LET = auto() # Definición de variables
    LPAREN = auto() # Paréntesis izquierdo (
    PLUS = auto() # Suma
    RBRACE = auto() # Llave derecha 
    RPAREN = auto() # Paréntesis drecho )
    SEMICOLON = auto() # PUnto y coma


class Token(NamedTuple):

    token_type: TokenType
    literal: str

    def __str__(self) -> str:
            return f"Type {self.token_type}, Literal: {self.literal}"


def lookup_token_type(literal: str) -> TokenType:
    
    # Una variable keyword que es un diccionario que tiene como llaves strngs y como valores TokenType
    keywords: Dict[str, TokenType] = {
        "variable": TokenType.LET,
        "funcion": TokenType.FUNCTION,
    }

    # Miramos si es una palabra reservada de nuestro lenguaje, si no lo es, entonces es un identificadir (un nombre de variable p.ej)
    return keywords.get(literal, TokenType.IDENT)