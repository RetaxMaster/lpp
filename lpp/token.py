from enum import (
    auto,
    Enum,
    unique,
)

from typing import NamedTuple


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