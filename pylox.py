import pathlib

class LoxException(Exception):
    pass

def run_file(file=None):
    if not file:
        _run_prompt()
    else:
        filepath = pathlib.Path(file)
    if not filepath.exists():
        raise LoxException("file %s does not exist" % filepath)
    else:
        _run_file(file=filepath)

def _run_prompt():
    """Run LOX source code line by line
    """
    print("""  _     _____  __
 | |   / _ \ \/ /
 | |  | | | \  / 
 | |__| |_| /  \ 
 |_____\___/_/\_\\
                 
LOX interactive interpreter
pylox v0.0.1
2022 @CepstrumLabs
    """)
    while True:
        line = input(">>> ")
        if line == "exit()":
            break
        if not line:
            break
        run(source=line)


def _run_file(file):
    """Run a file containing LOX source code

    Args:
        file (pathlib.Path): The file to run
    """
    with open(file, "r") as sourcefile:
        source = sourcefile.read()
    run(source=source)

def run(source):
    """Run raw LOX source code in the form of string

    Args:
        source (string): The LOX source code to run
    """
    scanner = LoxScanner(source=source)
    tokens = scanner.scan_tokens()

    for token in tokens:
        print(token)


class LoxScanner:

    def __init__(self, source):
        self.source = source
        self.tokens = []
    
    def scan_tokens(self):
        """
        """
        return self.tokens


class LoxToken:

    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"{self.__class__.__name__}(type_={self.type}, value={self.value})"

if __name__ == "__main__":
    USAGE = """
    pylox [script.lox]
    """
    import sys
    if len(sys.argv) == 1:
        _run_prompt()
    elif len(sys.argv) == 2:
        run_file(file=sys.argv[1])
    else:
        raise LoxException(USAGE)
