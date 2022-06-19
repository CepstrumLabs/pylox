from datetime import datetime
from pathlib import Path

NEWLINE = "\n"
TAB = "\t"


class Writer:
    def __init__(self, path):
        self.path = path

    def write(self, content):
        with open(self.path, "w") as outfile:
            outfile.write(content)


def define_ast(output_dir, base_name, types, imports=None):
    name = base_name.lower()
    path = Path(output_dir) / f"{name}.py"
    writer = Writer(path)
    source = _add_autogenerated_banner()
    if imports:
        for imported_item in imports:
            source += imported_item + NEWLINE
    source += "from pylox.scanner import LoxToken as Token" + 2 * NEWLINE
    source += create_abstract_class(name=base_name)
    source += _add_abstract_method(name="accept", class_name=base_name)
    for type_ in types:
        class_name = type_.split(":")[0].strip()
        class_fields = type_.split(":")[1].strip()
        source += (
            define_type(
                parent_class_name=base_name, class_name=class_name, fields=class_fields
            )
            + NEWLINE
        )
    writer.write(source)
    return source


def _add_autogenerated_banner():
    _date = datetime.now().strftime("%B %d, %Y %H:%M:%S")
    source = "# This file was autogenerated by pylox" + NEWLINE
    source += f"# on {_date}" + NEWLINE
    return source


def _add_abstract_method(name, class_name):
    source = TAB + f"def {name}(self, visitor: '{class_name}Visitor'):" + NEWLINE
    source += (
        2 * TAB
        + "raise NotImplementedError('Subclasses should implement this method')"
        + 2 * NEWLINE
    )
    return source


def create_abstract_class(name):
    return f"class {name}:{NEWLINE}{TAB}{NEWLINE}"


def define_type(parent_class_name, class_name, fields):
    field_defs = [part.split() for part in fields.split(",")]
    source = f"class {class_name}({parent_class_name}):" + 2 * NEWLINE
    source += _add_init_method(field_defs)
    source += _add_accept_method(parent_class_name, class_name)
    source += _add_repr_method(class_name, field_defs)
    source += _add_eq_method(class_name, field_defs)
    return source


def _add_eq_method(class_name, field_defs):
    source = TAB + "def __eq__(self, other):" + NEWLINE
    return_line = 2 * TAB + "return isinstance(other, self.__class__)"
    for field_def in field_defs:
        return_line += " and self.%s==other.%s" % (field_def[1], field_def[1])
    return source + return_line + 2 * NEWLINE


def _add_repr_method(class_name, field_defs):
    source = TAB + "def __repr__(self):" + NEWLINE
    return_line = 2 * TAB + "return f'{%s}(" % "self.__class__.__name__"
    for field_def in field_defs:
        return_line += "%s={self.%s}, " % (field_def[1], field_def[1])
    return_line = return_line[:-2]
    return_line += ")'"
    return source + return_line + 2 * NEWLINE


def _add_init_method(field_defs):
    source = (
        TAB
        + "def __init__(self, "
        + ", ".join([f"{field_def[1]}: '{field_def[0]}'" for field_def in field_defs])
        + "):"
        + NEWLINE
    )
    for field_def in field_defs:
        source += 2 * TAB + f"self.{field_def[1]} = {field_def[1]}" + NEWLINE
    source += NEWLINE
    return source


def _add_accept_method(parent_class_name, class_name):
    source = TAB + f"def accept(self, visitor: '{parent_class_name}Visitor'):" + NEWLINE
    source += (
        2 * TAB
        + f"return visitor.visit_{class_name.lower()}_{parent_class_name.lower()}(self)"
        + 2 * NEWLINE
    )
    return source


def generate_ast(directory):
    output_dir = directory
    base_name = "Expr"
    TYPES = [
        "Binary: Expr left, Token operator, Expr right",
        "Unary: Token operator, Expr right",
        "Literal: object value",
        "Logical: Token operator, Expr left, Expr right",
        "Variable: Token name",
        "Grouping: Expr expression",
        "Assign: Token assign_to, Expr to_assign",
        "Call: Expr callee, List[Expr] arguments",
    ]

    define_ast(output_dir=output_dir, base_name=base_name, types=TYPES)

    base_name = "Stmt"
    imports = ["from typing import List"]
    TYPES = [
        "Expression: Expr expression",
        "Print: Expr expression",
        "Var: Token name, Expr initialiser",
        "Block: List[Stmt] statements",
        "If: Expr condition, Stmt then_branch, Stmt else_branch",
        "While: Expr condition, Stmt statement",
        "Function: Token name, List[Stmt] body, List[Token] params",
    ]

    define_ast(output_dir=output_dir, base_name=base_name, types=TYPES, imports=imports)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    directory = Path(args.output_dir)
    if not directory.exists():
        raise OSError(f"Directory {directory} does not exist")
    source = generate_ast(directory=directory)
