import readline

from typing import List

from os import system, name 

from lpp.ast import Program
from lpp.evaluator import evaluate
from lpp.lexer import Lexer
from lpp.parser import Parser
from lpp.token import (
    Token,
    TokenType
)

EOF_TOKEN: Token = Token(TokenType.EOF, "")
ENGLISH_WORDS = ("clear", "clear()", "exit", "exit()")

def clear(): 
  
    # for windows 
    if name == 'nt': 
        _ = system('cls') 
  
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear') 


def _print_parse_errors(errors: List[str]):

    for error in errors:
        print(error)


def start_repl():
    
    # Walrus operator, asigna a la vez que compara
    while (source := input(">> ")) != "salir()":

        if source == "limpiar()" or source == "limpiar":
            clear()

        elif source in ENGLISH_WORDS:
            print("Soy un lenguaje hecho en español. Dímelo en español por favor :D")

        else:
        
            lexer: Lexer = Lexer(source)
            parser: Parser = Parser(lexer)

            program: Program = parser.parse_program()

            if len(parser.errors) > 0:
                _print_parse_errors(parser.errors)
                continue

            evaluated = evaluate(program)

            if evaluated is not None:

                print(evaluated.inspect())