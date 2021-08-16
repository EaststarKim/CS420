from ply import lex

class MyLexer:

    def __init__(self):
        self.pretok = {
            'if': 'IF',
            'for': 'FOR',
            'return': 'RETURN',
            'int': 'INT',
            'float': 'FLOAT',
            'void' : 'VOID'
        }
        self.tokens = [
            "INT",
            "FLOAT",
            "VOID",
            "ID",
            "NUMBER",
            "PLUS",
            "MINUS",
            "STAR",
            "DIVIDE",
            "ASSIGN",
            "EQUAL",
            "NOTEQUAL",
            "LGREATER",
            "RGREATER",
            "LGREQUAL",
            "RGREQUAL",
            "INCREMENT",
            "SEMICOLON",
            "COMMA",
            "STRING",
            "RETURN",
            "IF",
            "FOR",
            "LPAR",
            "RPAR",
            "LBRA",
            "RBRA",
            "LBRAC",
            "RBRAC",
        ]       
        self.lexer = None

    def t_ID(self, tok):
        r"([a-zA-Z_][0-9a-zA-Z_]*)"
        tok.type = self.pretok.get(tok.value, 'ID')
        return tok

    t_NUMBER = r"((0|[1-9][0-9]*)(\.[0-9]+)?)"
    t_PLUS = r"\+"
    t_MINUS = r"-"
    t_STAR = r"\*"
    t_DIVIDE = r"/"
    t_ASSIGN = r"="
    t_EQUAL = r"=="
    t_NOTEQUAL = r"!="
    t_LGREATER = r">"
    t_RGREATER = r"<"
    t_LGREQUAL = r"<="
    t_RGREQUAL = r">="
    t_INCREMENT = r"\+\+"
    t_SEMICOLON = r";"
    t_COMMA = r","
    t_STRING = r"\".*\""
    t_LPAR = r"\("
    t_RPAR = r"\)"
    t_LBRA = r"\{"
    t_RBRA = r"\}"
    t_LBRAC = r"\["
    t_RBRAC = r"\]"
    t_ignore = " \t"

    def t_newline(self, tok):
        r'\n+'
        tok.lexer.lineno += len(tok.value)

    def t_error(self, tok):
        print("Lex error '%s'" % tok.value[0])
        tok.lexer.skip(1)

    def build(self, **args):
        self.lexer = lex.lex(object=self, **args)
        return self.lexer
