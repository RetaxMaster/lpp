from unittest import TestCase

from lpp.ast import (
    ExpressionStatement,
    Identifier,
    Integer,
    LetStatement,
    Program,
    ReturnStatement
)

from lpp.token import (
    Token,
    TokenType
)

class ASTTest(TestCase):

    def test_let_statement(self) -> None:

        program: Program = Program(statements=[

            LetStatement(

                token=Token(TokenType.LET, literal="variable"),

                name=Identifier(
                    token=Token(TokenType.IDENT, literal="mi_var"),
                    value="mi_var"
                ),

                value=Identifier(
                    token=Token(TokenType.IDENT, literal="otra_variable"),
                    value="otra_variable"
                )

            )

        ])

        program_str = str(program)
        self.assertEquals(program_str, "variable mi_var = otra_variable;")


    def test_return_statement(self) -> None:

        program: Program = Program(statements=[

            ReturnStatement(

                token=Token(TokenType.RETURN, literal="regresa"),

                return_value=Identifier(
                    token=Token(TokenType.IDENT, literal="mi_var"),
                    value="mi_var"
                )

            )

        ])

        program_str = str(program)
        self.assertEquals(program_str, "regresa mi_var;")

    
    def test_expression_statement(self) -> None:

        program: Program = Program(statements=[

            ExpressionStatement(

                token=Token(TokenType.IDENT, literal="foobar"),

                expression=Identifier(
                    token=Token(TokenType.IDENT, literal="foobar"),
                    value="foobar"
                )

            ),

            ExpressionStatement(

                token=Token(TokenType.INT, literal="5"),

                expression=Identifier(
                    token=Token(TokenType.INT, literal="5"),
                    value="5"
                )

            )

        ])

        program_str = str(program)
        self.assertEquals(program_str, "foobar5")