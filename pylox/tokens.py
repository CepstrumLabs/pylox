class TokenType:

    # Single character tokens
    LEFT_PAREN = "LEFT_PAREN"
    RIGHT_PAREN = "RIGHT_PAREN"
    LEFT_BRACE = "LEFT_BRACE"
    RIGHT_BRACE = "RIGHT_BRACE"
    COMMA = "COMMA"
    DOT = "DOT"
    MINUS = "MINUS"
    PLUS = "PLUS"
    SEMICOLON = "SEMICOLON"
    SLASH = "SLASH"
    STAR = "STAR"

    # 1 or 2 character tokens
    BANG = "BANG"
    BANG_EQUAL = "BANG_EQUAL"
    EQUAL = "EQUAL"
    EQUAL_EQUAL = "EQUAL_EQUAL"
    GREATER = "GREATER"
    GREATER_EQUAL = "GREATER_EQUAL"
    LESS = "LESS"
    LESS_EQUAL = "LESS_EQUAL"

    # Literals
    IDENTIFIER = "IDENTIFIER"
    STRING = "STRING"
    NUMBER = "NUMBER"

    AND = "AND"
    CLASS = "CLASS"
    ELSE = "ELSE"
    FALSE = "FALSE"
    IF = "IF"
    FUN = "FUN"
    FOR = "FOR"
    IF = "IF"
    NIL = "NIL"
    OR = "OR"
    PRINT = "PRINT"
    RETURN = "RETURN"
    SUPER = "SUPER"
    THIS = "THIS"
    TRUE = "TRUE"
    VAR = "VAR"
    WHILE = "WHILE"
    EOF = "EOF"

    KEYWORDS = {
        "and": AND,
        "class": CLASS,
        "else": ELSE,
        "false": FALSE,
        "if": IF,
        "fun": FUN,
        "for": FOR,
        "if": IF,
        "nil": NIL,
        "or": OR,
        "print": PRINT,
        "return": RETURN,
        "super": SUPER,
        "this": THIS,
        "true": TRUE,
        "var": VAR,
        "while": WHILE,
        "eof": EOF,
    }

    TOKENS_TO_LEXEMES = {
        LEFT_PAREN: "(",
        RIGHT_PAREN: ")",
        LEFT_BRACE: "{",
        RIGHT_BRACE: "}",
        COMMA: ",",
        DOT: ".",
        MINUS: "-",
        PLUS: "+",
        SEMICOLON: ";",
        SLASH: "/",
        STAR: "*",
        BANG: "!",
        BANG_EQUAL: "!=",
        EQUAL: "=",
        EQUAL_EQUAL: "==",
        GREATER: ">",
        GREATER_EQUAL: ">=",
        LESS: "<",
        LESS_EQUAL: "<=",
        AND: "and",
        CLASS: "class",
        ELSE: "else",
        FALSE: "false",
        IF: "if",
        FUN: "fun",
        FOR: "for",
        IF: "if",
        NIL: "nil",
        OR: "or",
        PRINT: "print",
        RETURN: "return",
        SUPER: "super",
        THIS: "this",
        TRUE: "true",
        VAR: "var",
        WHILE: "while",
        EOF: "eof",
    }
