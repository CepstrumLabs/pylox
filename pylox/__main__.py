from pylox.pylox import LoxException, LoxIntepreter

if __name__ == "__main__":
    USAGE = """
    pylox [script.lox]
    """
    import sys

    interpreter = LoxIntepreter()
    if len(sys.argv) == 1:
        interpreter._run_prompt()
    elif len(sys.argv) == 2:
        interpreter.run_file(file=sys.argv[1])
    else:
        raise LoxException(USAGE)
