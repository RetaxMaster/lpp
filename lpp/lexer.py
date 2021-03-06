from re import match

from lpp.token import (
    Token,
    TokenType,
    lookup_token_type
)


class Lexer:

    def __init__(self, source: str) -> None:

        self._source: str = source
        self._character: str = ""
        self._read_position: int = 0
        self._position: int = 0

        self._read_character()


    def next_token(self) -> Token:

        self._skip_whitespace()
        
        if match(r"^=$", self._character):
            
            if self._peek_character() == "=":

                if self._peek_character(2) == "=":
                    token = self._make_three_character_token(TokenType.SIMILAR)
                        
                else:
                    token = self._make_two_character_token(TokenType.EQ)

            else:
                token = Token(TokenType.ASSIGN, self._character)

        elif match(r"^\+$", self._character):
            token = Token(TokenType.PLUS, self._character)

        elif match(r"^\($", self._character):
            token = Token(TokenType.LPAREN, self._character)

        elif match(r"^\)$", self._character):
            token = Token(TokenType.RPAREN, self._character)

        elif match(r"^{$", self._character):
            token = Token(TokenType.LBRACE, self._character)

        elif match(r"^}$", self._character):
            token = Token(TokenType.RBRACE, self._character)

        elif match(r"^,$", self._character):
            token = Token(TokenType.COMMA, self._character)

        elif match(r"^;$", self._character):
            token = Token(TokenType.SEMICOLON, self._character)

        elif match(r"^-$", self._character):
            token = Token(TokenType.MINUS, self._character)

        elif match(r"^/$", self._character):
            token = Token(TokenType.DIVISION, self._character)

        elif match(r"^\*$", self._character):
            token = Token(TokenType.MULTIPLICATION, self._character)

        elif match(r"^<$", self._character):

            if self._peek_character() == "=":
                token = self._make_two_character_token(TokenType.LE)

            else:
                token = Token(TokenType.LT, self._character)

        elif match(r"^>$", self._character):

            if self._peek_character() == "=":
                token = self._make_two_character_token(TokenType.GE)

            else:
                token = Token(TokenType.GT, self._character)

        elif match(r"^!$", self._character):

            if self._peek_character() == "=":

                if self._peek_character(2) == "=":
                    token = self._make_three_character_token(TokenType.DIFF)
                    
                else:
                    token = self._make_two_character_token(TokenType.NOT_EQ)

            else:
                token = Token(TokenType.NEGATION, self._character)

        elif self._is_letter(self._character):

            literal = self._read_identifier() # Nombre del token
            token_type = lookup_token_type(literal) # Tipo del token

            return Token(token_type, literal)
        
        elif self._is_number(self._character):

            literal = self._read_number() # Nombre del token

            return Token(TokenType.INT, literal)

        elif match(r"^$", self._character):
            token = Token(TokenType.EOF, self._character)

        elif match(r"^\"|'$", self._character):
            literal = self._read_string()

            return Token(TokenType.STRING, literal)

        else:
            token = Token(TokenType.ILLEGAL, self._character)

        self._read_character()

        return token


    def _is_letter(self, character: str) -> bool:

        return bool(match(r"^[a-záéíóúA-ZÁÉÍÓÚñÑ_]$", character)) # Estos son los caracteres que nuestro lenguaje conoce como letras


    def _is_number(self, character: str) -> bool:

        return bool(match(r"^\d$", character))


    def _make_three_character_token(self, token_type: TokenType) -> Token:

        first = self._character
        self._read_character()
        second = self._character
        self._read_character()
        third = self._character

        return Token(token_type, f"{first}{second}{third}")


    def _make_two_character_token(self, token_type: TokenType) -> Token:

        prefix = self._character
        self._read_character()
        suffix = self._character

        return Token(token_type, f"{prefix}{suffix}")


    def _peek_character(self, skip = 1) -> str:

        if self._read_position >= len(self._source):
            return ""
        
        return self._source[self._read_position] if skip == 1 else self._source[self._read_position + (skip - 1)] 

    
    def _read_character(self) -> None:

        if self._read_position >= len(self._source):
            self._character = ""
        else:
            self._character = self._source[self._read_position]

        self._position = self._read_position
        self._read_position += 1


    # Cuando encuentra una letra, empieza a leer toda la palabra escrita a través de este método
    def _read_identifier(self) -> str:

        initial_position = self._position

        if self._is_letter(self._character):

            while self._is_letter(self._character) or self._is_number(self._character):
                self._read_character()

        return self._source[initial_position:self._position]


    # Cuando encuentra un número, empieza a leer todo el numero escrito a través de este método
    def _read_number(self) -> str:

        initial_position = self._position

        while self._is_number(self._character):
            self._read_character()

        return self._source[initial_position:self._position]


    def _read_string(self) -> str:

        # Vemos con cuál comilla se abrió este string, así en el while podemos buscar la misma comilla de cierre
        quote_type = self._character

        # Ahorita estamos en la comilla, así que leemos un caracter para avanzar hacia el string
        self._read_character()

        initial_position = self._position

        while self._character != quote_type \
                and self._read_position <= len(self._source):

            self._read_character()

        string =  self._source[initial_position:self._position]
        self._read_character()
        return string


    #A medida que se vaya leyendo el código, si encuentra uno o muchos espacios en blanco, los "skipea"
    def _skip_whitespace(self) -> None:

        while match(r"^\s$", self._character):
            self._read_character()