import pathlib
import sys

from pylox.expr_eval import ExpressionInterpreter as Interpreter
from pylox.logging import logger
from pylox.parser import Parser as LoxParser
from pylox.parser import ParserError
from pylox.resolver import CompilerError, Resolver
from pylox.scanner import LoxScanner

LOGO = r"""
  _     _____  __
 | |   / _ \ \/ /
 | |  | | | \  / 
 | |__| |_| /  \ 
 |_____\___/_/\_\
                 
LOX interactive interpreter
pylox v0.0.3
2022 @CepstrumLabs
    """


class LoxException(Exception):
    pass


class LoxIntepreter:
    def __init__(self):
        self.had_error = False
        self.interpreter = Interpreter()

    def run_file(self, file=None):
        if not file:
            self._run_prompt()
        else:
            filepath = pathlib.Path(file)
        if not filepath.exists():
            raise LoxException("file %s does not exist" % filepath)
        else:
            self._run_file(file=filepath)

    def _run_prompt(self):
        """Run LOX source code line by line"""
        print(LOGO)
        while True:
            line = input(">>> ")
            if line == "exit()":
                break
            if not line:
                continue
            self.run(source=line)
            # Do not kill all the interactιve session because of one line
            self.had_error = False

    def _run_file(self, file):
        """Run a file containing LOX source code

        Args:
            file (pathlib.Path): The file to run
        """
        with open(file, "r") as sourcefile:
            source = sourcefile.read()
        if self.had_error:
            sys.exit(1)
        self.run(source=source)

    def run(self, source):
        """Run raw LOX source code in the form of string

        Args:
            source (string): The LOX source code to run
        """
        scanner = LoxScanner(source=source)
        tokens = scanner.scan_tokens()

        parser = LoxParser(tokens=tokens)
        resolver = Resolver(interpreter=self.interpreter)
        statements = []
        try:
            statements = parser.parse()
        except ParserError:
            self.had_error = True
        logger.debug("Finished parsing")
        
        try:
            resolver.resolve_all(statements)
        except CompilerError as e:
            self.had_error = True
            self.error = e
        logger.debug("Finished resolving")
        result = None

        if not self.had_error:
            result = self.interpreter.interpret(statements=statements)
        else:
            print("Compiler error: " + str(self.error))
        logger.debug("Finished interpreting")

        return result
