from unittest import TestCase
from typing import List

from lpp.token import (
    Token,
    TokenType
)

from lpp.lexer import Lexer


class LexerTest(TestCase):

    def test_illegal(self) -> None:

        source: str = "@¡¿"
        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []

        for i in range(len(source)):
            tokens.append(lexer.next_token())
    
        expected_tokens: List[Token] = [
            Token(TokenType.ILLEGAL, "@"),
            Token(TokenType.ILLEGAL, "¡"),
            Token(TokenType.ILLEGAL, "¿"),
        ]

        self.assertEquals(tokens, expected_tokens)


    def test_one_character_operator(self) -> None:

        source: str = "=+-/*<>!"
        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []

        for i in range(len(source)):

            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [
            Token(TokenType.ASSIGN, "="),
            Token(TokenType.PLUS, "+"),
            Token(TokenType.MINUS, "-"),
            Token(TokenType.DIVISION, "/"),
            Token(TokenType.MULTIPLICATION, "*"),
            Token(TokenType.LT, "<"),
            Token(TokenType.GT, ">"),
            Token(TokenType.NEGATION, "!"),
        ]

        self.assertEquals(tokens, expected_tokens)

    
    def test_line_break(self) -> None:

        # Iician pegadas a las comillas de apertura porque es la línea 1, las comillas de cierre están abajo porque hay un caracter \n que igual es contado por el lexer, por eso expectamos 21 tokens
        source: str = """variable cinco = 5;
                        variable seis = 6;
                        variable siete = 7;
                        variable ocho = 8;
                        """

        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []

        for i in range(21):
            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [

            Token(TokenType.LET, "variable", 1),
            Token(TokenType.IDENT, "cinco", 1),
            Token(TokenType.ASSIGN, "=", 1),
            Token(TokenType.INT, "5", 1),
            Token(TokenType.SEMICOLON, ";", 1),

            Token(TokenType.LET, "variable", 2),
            Token(TokenType.IDENT, "seis", 2),
            Token(TokenType.ASSIGN, "=", 2),
            Token(TokenType.INT, "6", 2),
            Token(TokenType.SEMICOLON, ";", 2),

            Token(TokenType.LET, "variable", 3),
            Token(TokenType.IDENT, "siete", 3),
            Token(TokenType.ASSIGN, "=", 3),
            Token(TokenType.INT, "7", 3),
            Token(TokenType.SEMICOLON, ";", 3),

            Token(TokenType.LET, "variable", 4),
            Token(TokenType.IDENT, "ocho", 4),
            Token(TokenType.ASSIGN, "=", 4),
            Token(TokenType.INT, "8", 4),
            Token(TokenType.SEMICOLON, ";", 4),

            Token(TokenType.EOF, "", 5),

        ]

        self.assertEquals(tokens, expected_tokens)


    def test_eof(self) -> None:

        source: str = "+"
        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []

        for i in range(len(source) + 1):

            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [
            Token(TokenType.PLUS, "+"),
            Token(TokenType.EOF, ""),
        ]

        self.assertEquals(tokens, expected_tokens)


    def test_delimiters(self) -> None:

        source: str = "(){},;"
        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []

        for i in range(len(source)):

            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [
            Token(TokenType.LPAREN, "("),
            Token(TokenType.RPAREN, ")"),
            Token(TokenType.LBRACE, "{"),
            Token(TokenType.RBRACE, "}"),
            Token(TokenType.COMMA, ","),
            Token(TokenType.SEMICOLON, ";"),
        ]

        self.assertEquals(tokens, expected_tokens)


    def test_assignment(self) -> None:
        
        source: str = "variable cinco = 5;"
        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []

        for i in range(5):

            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [
            Token(TokenType.LET, "variable"),
            Token(TokenType.IDENT, "cinco"),
            Token(TokenType.ASSIGN, "="),
            Token(TokenType.INT, "5"),
            Token(TokenType.SEMICOLON, ";"),
        ]

        self.assertEquals(tokens, expected_tokens)


    def test_function_declaration(self) -> None:
        
        source: str = """
            variable suma = funcion(x, y) {
                x + y;
            };
        """

        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []

        for i in range(16):

            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [
            Token(TokenType.LET, "variable", 2),
            Token(TokenType.IDENT, "suma", 2),
            Token(TokenType.ASSIGN, "=", 2),
            Token(TokenType.FUNCTION, "funcion", 2),
            Token(TokenType.LPAREN, "(", 2),
            Token(TokenType.IDENT, "x", 2),
            Token(TokenType.COMMA, ",", 2),
            Token(TokenType.IDENT, "y", 2),
            Token(TokenType.RPAREN, ")", 2),
            Token(TokenType.LBRACE, "{", 2),
            Token(TokenType.IDENT, "x", 3),
            Token(TokenType.PLUS, "+", 3),
            Token(TokenType.IDENT, "y", 3),
            Token(TokenType.SEMICOLON, ";", 3),
            Token(TokenType.RBRACE, "}", 4),
            Token(TokenType.SEMICOLON, ";", 4),
        ]

        self.assertEquals(tokens, expected_tokens)


    def test_function_call(self) -> None:
        
        source: str = """variable resultado = suma(dos, tres);"""

        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []

        for i in range(10):

            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [
            Token(TokenType.LET, "variable"),
            Token(TokenType.IDENT, "resultado"),
            Token(TokenType.ASSIGN, "="),
            Token(TokenType.IDENT, "suma"),
            Token(TokenType.LPAREN, "("),
            Token(TokenType.IDENT, "dos"),
            Token(TokenType.COMMA, ","),
            Token(TokenType.IDENT, "tres"),
            Token(TokenType.RPAREN, ")"),
            Token(TokenType.SEMICOLON, ";"),
        ]

        self.assertEquals(tokens, expected_tokens)


    def test_control_statement(self) -> None:
        
        source: str = """
            si (5 < 10) {
                regresa verdadero;
            } si_no {
                regresa falso;
            }
        """

        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []

        for i in range(17):

            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [
            Token(TokenType.IF, "si", 2),
            Token(TokenType.LPAREN, "(", 2),
            Token(TokenType.INT, "5", 2),
            Token(TokenType.LT, "<", 2),
            Token(TokenType.INT, "10", 2),
            Token(TokenType.RPAREN, ")", 2),
            Token(TokenType.LBRACE, "{", 2),
            Token(TokenType.RETURN, "regresa", 3),
            Token(TokenType.TRUE, "verdadero", 3),
            Token(TokenType.SEMICOLON, ";", 3),
            Token(TokenType.RBRACE, "}", 4),
            Token(TokenType.ELSE, "si_no", 4),
            Token(TokenType.LBRACE, "{", 4),
            Token(TokenType.RETURN, "regresa", 5),
            Token(TokenType.FALSE, "falso", 5),
            Token(TokenType.SEMICOLON, ";", 5),
            Token(TokenType.RBRACE, "}", 6),
        ]

        self.assertEquals(tokens, expected_tokens)

    
    def test_two_character_operator(self) -> None:
        
        source: str = """
            10 == 10;
            10 != 9;
            10 <= 9;
            10 >= 9;
        """

        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []

        for i in range(16):

            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [
            Token(TokenType.INT, "10", 2),
            Token(TokenType.EQ, "==", 2),
            Token(TokenType.INT, "10", 2),
            Token(TokenType.SEMICOLON, ";", 2),

            Token(TokenType.INT, "10", 3),
            Token(TokenType.NOT_EQ, "!=", 3),
            Token(TokenType.INT, "9", 3),
            Token(TokenType.SEMICOLON, ";", 3),

            Token(TokenType.INT, "10", 4),
            Token(TokenType.LE, "<=", 4),
            Token(TokenType.INT, "9", 4),
            Token(TokenType.SEMICOLON, ";", 4),

            Token(TokenType.INT, "10", 5),
            Token(TokenType.GE, ">=", 5),
            Token(TokenType.INT, "9", 5),
            Token(TokenType.SEMICOLON, ";", 5),
        ]

        self.assertEquals(tokens, expected_tokens)


    def test_three_character_operator(self) -> None:
        
        source: str = """
            10 === 10;
            10 !== 9;
        """

        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []

        for i in range(8):

            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [
            Token(TokenType.INT, "10", 2),
            Token(TokenType.SIMILAR, "===", 2),
            Token(TokenType.INT, "10", 2),
            Token(TokenType.SEMICOLON, ";", 2),
            
            Token(TokenType.INT, "10", 3),
            Token(TokenType.DIFF, "!==", 3),
            Token(TokenType.INT, "9", 3),
            Token(TokenType.SEMICOLON, ";", 3),
        ]

        self.assertEquals(tokens, expected_tokens)


    def test_mixed_character_operator(self) -> None:
        
        source: str = """
            10 === 10;
            10 !== 9;
            10 == 10;
            10 != 9;
        """

        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []

        for i in range(16):

            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [
            Token(TokenType.INT, "10", 2),
            Token(TokenType.SIMILAR, "===", 2),
            Token(TokenType.INT, "10", 2),
            Token(TokenType.SEMICOLON, ";", 2),

            Token(TokenType.INT, "10", 3),
            Token(TokenType.DIFF, "!==", 3),
            Token(TokenType.INT, "9", 3),
            Token(TokenType.SEMICOLON, ";", 3),

            Token(TokenType.INT, "10", 4),
            Token(TokenType.EQ, "==", 4),
            Token(TokenType.INT, "10", 4),
            Token(TokenType.SEMICOLON, ";", 4),

            Token(TokenType.INT, "10", 5),
            Token(TokenType.NOT_EQ, "!=", 5),
            Token(TokenType.INT, "9", 5),
            Token(TokenType.SEMICOLON, ";", 5),
        ]

        self.assertEquals(tokens, expected_tokens)
