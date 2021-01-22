from unittest import TestCase

from typing import (
    cast
)

from lpp.ast import (
    Identifier,
    LetStatement,
    Program,
)
from lpp.lexer import Lexer
from lpp.parser import Parser

class ParserTest(TestCase):
    
    def test_parse_program(self) -> None:

        source: str = "variable x = 5;"
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)

        program: Program = parser.parse_program()

        self.assertIsNotNone(program)
        self.assertIsInstance(program, Program)


    def test_let_statements(self) -> None:

        source: str = """
            variable x = 5;
            variable y = 10;
            variable foo = 20;
        """

        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)

        program: Program = parser.parse_program()

        self.assertEqual(len(program.statements), 3)

        for statement in program.statements:

            self.assertEqual(statement.token_literal(), "variable")
            self.assertIsInstance(statement, LetStatement)


    def test_names_in_let_statements(self) -> None:

        source: str = """
            variable x = 5;
            variable y = 10;
            variable foo = 20;
        """

        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)

        program: Program = parser.parse_program()

        self.assertEqual(cast(Identifier, cast(LetStatement, program.statements[0]).name).value, "x")
        self.assertEqual(cast(Identifier, cast(LetStatement, program.statements[1]).name).value, "y")
        self.assertEqual(cast(Identifier, cast(LetStatement, program.statements[2]).name).value, "foo")


    def test_parse_errors(self) -> None:

        source: str = "variable x 5;"

        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)

        program: Program = parser.parse_program()

        self.assertEquals(len(parser.errors), 1)