import readline

from re import match

from typing import List

from os import system, name 

from lpp.ast import Program
from lpp.evaluator import evaluate
from lpp.lexer import Lexer
from lpp.object import Environment
from lpp.parser import Parser
from lpp.token import (
    Token,
    TokenType
)

EOF_TOKEN: Token = Token(TokenType.EOF, "")
ENGLISH_WORDS = ("clear", "clear()", "exit", "exit()", "history", "history()")

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


def execute_program(scanned):
    
    lexer: Lexer = Lexer(" ".join(scanned))
    parser: Parser = Parser(lexer)

    program: Program = parser.parse_program()
    env: Environment = Environment()

    if len(parser.errors) > 0:
        _print_parse_errors(parser.errors)
        return 0

    evaluated = evaluate(program, env)

    if evaluated is not None:

        print(evaluated.inspect())

    return 1


def start_repl():

    scanned: List[str] = []
    
    # Walrus operator, asigna a la vez que compara
    while (source := input(">> ")) != "salir()":

        if source == "limpiar()" or source == "limpiar":
            clear()

        elif source == "historia()" or source == "historia":
            print("\n" + "\n".join([f"{idx + 1}.- {command}" for idx, command in enumerate(scanned)]) + "\n")

        elif source in ENGLISH_WORDS:
            print("Soy un lenguaje hecho en español. Dímelo en español por favor :D")

        elif match(r"^/", source):

            command = source[1:]
            
            try:

                command_position = int(command)

                if command_position > len(scanned):
                    print(f"El comando '{command_position}' no existe")

                else:

                    source_obtained = scanned[command_position - 1]

                    scanned.append(source_obtained)
                    execute_program(scanned)
            
            except ValueError:
                print(f"La opción {command} no es un número.")

        else:
            
            scanned.append(source)
            execute_program(scanned)