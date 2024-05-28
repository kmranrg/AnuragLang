# Author: Kumar Anurag <me@kmranrg.com>

import re

TOKEN_TYPES = [
    ('ASSUME', r'assume'),
    ('PRODUCE', r'produce'),
    ('TAKE', r'take'),
    ('INCASE', r'incase'),
    ('OTHERWISE', r'otherwise'),
    ('WHILE', r'while'),
    ('FUNCTION', r'function'),
    ('RETURN', r'return'),
    ('NUMBER', r'\d+'),
    ('IDENTIFIER', r'[a-zA-Z_]\w*'),
    ('STRING', r'"[^"\\]*(?:\\.[^"\\]*)*"'),
    ('ASSIGN', r'='),
    ('LBRACE', r'\{'),
    ('RBRACE', r'\}'),
    ('LPAREN', r'\('),
    ('RPAREN', r'\)'),
    ('LBRACKET', r'\['),
    ('RBRACKET', r'\]'),
    ('COMMA', r','),
    ('PLUS', r'\+'),
    ('MINUS', r'-'),
    ('MULTIPLY', r'\*'),
    ('DIVIDE', r'/'),
    ('GT', r'>'),
    ('LT', r'<'),
    ('EQ', r'=='),
    ('SEMICOLON', r';'),
    ('WHITESPACE', r'\s+'),
]

class Lexer:
    def __init__(self, source_code):
        self.source_code = source_code
        self.tokens = []
        self.current_position = 0
        self.line = 1
        self.column = 1

    def tokenize(self):
        line = 1
        column = 1
        while self.current_position < len(self.source_code):
            match = None
            for token_type, pattern in TOKEN_TYPES:
                regex = re.compile(pattern)
                match = regex.match(self.source_code, self.current_position)
                if match:
                    text = match.group(0)
                    if token_type != 'WHITESPACE':  # Skip whitespace
                        token = (token_type, text, line, column)
                        self.tokens.append(token)
                    self.current_position = match.end(0)
                    column += len(text)
                    break
            if not match:
                if self.source_code[self.current_position] == '#':
                    # Skip comment until the end of the line
                    while self.current_position < len(self.source_code) and self.source_code[self.current_position] != '\n':
                        self.current_position += 1
                    line += 1
                    column = 1
                else:
                    raise SyntaxError(f'Unexpected character: {self.source_code[self.current_position]}')
        return self.tokens

    def update_position(self, text):
        lines = text.split('\n')
        if len(lines) > 1:
            self.line += len(lines) - 1
            self.column = len(lines[-1]) + 1
        else:
            self.column += len(text)
