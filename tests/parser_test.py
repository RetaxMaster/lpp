from unittest import TestCase

from typing import (
    Any,
    cast,
    List,
    Tuple,
    Type
)

from lpp.ast import (
    Block,
    Boolean,
    Expression,
    ExpressionStatement,
    Identifier,
    If,
    Infix,
    Integer,
    LetStatement,
    Prefix,
    Program,
    ReturnStatement
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


    def test_return_statements(self) -> None:

        source: str = """
            regresa  5;
            regresa foo;
        """

        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)

        program: Program = parser.parse_program()

        self.assertEqual(len(program.statements), 2)

        for statement in program.statements:

            self.assertEqual(statement.token_literal(), "regresa")
            self.assertIsInstance(statement, ReturnStatement)


    def test_identifier_expression(self) -> None:
        
        source: str = "foobar;"
        
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)

        program: Program = parser.parse_program()

        self._test_program_statements(parser, program)
        expression_statement = cast(ExpressionStatement, program.statements[0])
        assert expression_statement.expression is not None

        self._test_literal_expression(expression_statement.expression, "foobar")


    def test_integer_expressions(self) -> None:

        source: str = "5;"

        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)

        program: Program = parser.parse_program()

        self._test_program_statements(parser, program)
        expression_statement = cast(ExpressionStatement, program.statements[0])
        assert expression_statement.expression is not None

        self._test_literal_expression(expression_statement.expression, 5)


    def test_prefix_expression(self) -> None:
        
        source: str = "!5; -15; -verdadero; -falso"

        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)

        program: Program = parser.parse_program()

        self._test_program_statements(parser, program, expected_statement_count=4)

        for statement, (expected_operator, expected_value) in zip(
            program.statements, [("!", 5), ("-", 15), ("-", True), ("-", False)]):

            statement = cast(ExpressionStatement, statement)
            self.assertIsInstance(statement.expression, Prefix)

            prefix = cast(Prefix, statement.expression)
            self.assertEquals(prefix.operator, expected_operator)

            assert prefix.right is not None
            self._test_literal_expression(prefix.right, expected_value)


    def test_infix_expression(self) -> None:
        
        source: str = """
            5 + 5;
            5 - 5;
            5 * 5;
            5 / 5;
            5 > 5;
            5 < 5;
            5 == 5;
            5 === 5;
            5 != 5;
            5 !== 5;
            verdadero == verdadero
            verdadero === verdadero
            falso != falso
            falso !== falso
        """

        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)

        program: Program = parser.parse_program()

        self._test_program_statements(parser, program, expected_statement_count=14)

        expected_operators_and_values: List[Tuple[Any, str, Any]] = [
            (5, "+", 5),
            (5, "-", 5),
            (5, "*", 5),
            (5, "/", 5),
            (5, ">", 5),
            (5, "<", 5),
            (5, "==", 5),
            (5, "===", 5),
            (5, "!=", 5),
            (5, "!==", 5),
            (True, "==", True),
            (True, "===", True),
            (False, "!=", False),
            (False, "!==", False),
        ]

        for statement, (expected_left, expected_operator, expected_right) in zip(
            program.statements, expected_operators_and_values):

            statement = cast(ExpressionStatement, statement)

            assert statement.expression is not None

            self.assertIsInstance(statement.expression, Infix)

            self._test_infix_expression(statement.expression,
                                        expected_left,
                                        expected_operator,
                                        expected_right)

                                    
    def test_boolean_expresion(self) -> None:

        source: str = "verdadero; falso;"

        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)

        program: Program = parser.parse_program()

        self._test_program_statements(parser, program, expected_statement_count=2)

        expected_values: List[bool] = [True, False]

        for statement, expected_value in zip(program.statements, expected_values):

            expression_statement = cast(ExpressionStatement, statement)
            
            assert expression_statement.expression is not None

            self._test_literal_expression(expression_statement.expression, expected_value)


    def test_operator_precedence(self) -> None:

        # El primer string representa el programa inicial
        # El segundo string representa cuál debería ser el órden de precedencia
        # El tercer int representa cuántos statements esperamos que tenga el programa
        test_sources: List[Tuple[str, str, int]] = [
            ('-a * b;', '((-a) * b)', 1),
            ('!-a;', '(!(-a))', 1),
            ('a + b + c;', '((a + b) + c)', 1),
            ('a + b - c;', '((a + b) - c)', 1),
            ('a * b * c;', '((a * b) * c)', 1),
            ('a * b / c;', '((a * b) / c)', 1),
            ('a + b / c;', '(a + (b / c))', 1),
            ('a + b * c + d / e - f;', '(((a + (b * c)) + (d / e)) - f)', 1),
            ('3 + 4; -5 * 5;', '(3 + 4)((-5) * 5)', 2),
            ('5 > 4 == 3 < 4;', '((5 > 4) == (3 < 4))', 1),
            ('5 < 4 != 3 > 4;', '((5 < 4) != (3 > 4))', 1),
            ('3 + 4 * 5 == 3 * 1 + 4 * 5;', '((3 + (4 * 5)) == ((3 * 1) + (4 * 5)))', 1),
            ('verdadero;', 'verdadero', 1),
            ('falso;', 'falso', 1),
            ('3 > 5 == verdadero;', '((3 > 5) == verdadero)', 1),
            ('3 < 5 == falso;', '((3 < 5) == falso)', 1),
            ('1 + (2 + 3) + 4;', '((1 + (2 + 3)) + 4)', 1),
            ('(5 + 5) * 2;', '((5 + 5) * 2)', 1),
            ('2 / (5 + 5);', '(2 / (5 + 5))', 1),
            ('-(5 + 5);', '(-(5 + 5))', 1),
        ]

        for source, expected_result, expected_statement_count in test_sources:

            lexer: Lexer = Lexer(source)
            parser: Parser = Parser(lexer)

            program: Program = parser.parse_program()
            
            self._test_program_statements(parser, program, expected_statement_count)
            self.assertEquals(str(program), expected_result)


    def test_if_expression(self) -> None:

        source: str = "si (x < y) { z }"

        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)

        program: Program = parser.parse_program()

        self._test_program_statements(parser, program, 1)

        # Test correct node types
        if_expression = cast(If, cast(ExpressionStatement, program.statements[0]).expression)
        self.assertIsInstance(if_expression, If)

        # Test condition
        assert if_expression.condition is not None
        self._test_infix_expression(cast(Expression, if_expression.condition), "x", "<", "y")

        # Test consequence
        assert if_expression.consequence is not None
        self.assertIsInstance(if_expression.consequence, Block)
        self.assertEquals(len(if_expression.consequence.statements), 1)

        consequence_statement = cast(ExpressionStatement, 
                                    if_expression.consequence.statements[0])

        assert consequence_statement.expression is not None
        self._test_identifier(consequence_statement.expression, "z")

        # Test alternative
        self.assertIsNone(if_expression.alternative)


    def _test_boolean(self, 
                        expression: Expression,
                        expected_value: bool) -> None:

        self.assertIsInstance(expression, Boolean)
        
        boolean = cast(Boolean, expression)
        self.assertEquals(boolean.value, expected_value)
        self.assertEquals(boolean.token.literal, "verdadero" if expected_value else "falso")


    def _test_infix_expression(self,
                                expression: Expression,
                                expected_left: Any,
                                expected_operator: str,
                                expected_right: Any):

        infix = cast(Infix, expression)

        assert infix.left is not None
        self._test_literal_expression(infix.left, expected_left)

        self.assertEquals(infix.operator, expected_operator)

        assert infix.right is not None
        self._test_literal_expression(infix.right, expected_right)


    def _test_program_statements(self,
                                parser: Parser,
                                program: Program,
                                expected_statement_count: int = 1) -> None:

        if parser.errors:
            print(parser.errors)

        self.assertEquals(len(parser.errors), 0)
        self.assertEquals(len(program.statements), expected_statement_count)
        self.assertIsInstance(program.statements[0], ExpressionStatement)


    def _test_literal_expression(self, 
                                expression: Expression,
                                expected_value: Any) -> None:

        value_type: Type = type(expected_value)

        if value_type == str:
            self._test_identifier(expression, expected_value)

        elif value_type == int:
            self._test_integer(expression, expected_value)

        elif value_type == bool:
            self._test_boolean(expression, expected_value)

        else:
            self.fail(f"Undefined type of expression. Got={value_type}")


    def _test_identifier(self, 
                        expression: Expression,
                        expected_value: str) -> None:

        self.assertIsInstance(expression, Identifier)
        
        identifier = cast(Identifier, expression)
        self.assertEquals(identifier.value, expected_value)
        self.assertEquals(identifier.token.literal, expected_value)


    def _test_integer(self, 
                        expression: Expression,
                        expected_value: int) -> None:

        self.assertIsInstance(expression, Integer)
        
        integer = cast(Integer, expression)
        self.assertEquals(integer.value, expected_value)
        self.assertEquals(integer.token.literal, str(expected_value))