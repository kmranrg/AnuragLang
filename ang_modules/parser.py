# Author: Kumar Anurag <me@kmranrg.com>

class Parser:
    def __init__(self, tokens, source_code):
        self.tokens = tokens
        self.source_code = source_code
        self.current_token_index = 0

    def parse(self):
        statements = []
        while not self.is_at_end():
            statements.append(self.statement())
        return statements

    def statement(self):
        token_type, token_value, line, column = self.peek()
        if token_type == 'ASSUME':
            return self.assignment_statement()
        elif token_type == 'PRODUCE':
            return self.produce_statement()
        elif token_type == 'TAKE':
            return self.take_statement()
        elif token_type == 'INCASE':
            return self.incase_statement()
        elif token_type == 'WHILE':
            return self.while_statement()
        elif token_type == 'FUNCTION':
            return self.function_statement()
        elif token_type == 'RETURN':
            return self.return_statement()
        else:
            raise SyntaxError(f'Unexpected token: {token_type} at line {line}, column {column}')

    def assignment_statement(self):
        self.consume('ASSUME')
        var_name = self.consume('IDENTIFIER')
        self.consume('ASSIGN')
        value = self.expression()
        self.consume('SEMICOLON')
        return ('assignment', var_name, value)

    def produce_statement(self):
        self.consume('PRODUCE')
        self.consume('LPAREN')
        value = self.expression()
        self.consume('RPAREN')
        self.consume('SEMICOLON')
        return ('produce', value)

    def take_statement(self):
        self.consume('TAKE')
        self.consume('LPAREN')
        var_name = self.consume('IDENTIFIER')
        self.consume('RPAREN')
        self.consume('SEMICOLON')
        return ('take', var_name)

    def incase_statement(self):
        self.consume('INCASE')
        self.consume('LPAREN')
        condition = self.expression()
        self.consume('RPAREN')
        self.consume('LBRACE')
        true_branch = self.block()
        self.consume('RBRACE')
        self.consume('OTHERWISE')
        self.consume('LBRACE')
        false_branch = self.block()
        self.consume('RBRACE')
        return ('incase', condition, true_branch, false_branch)

    def while_statement(self):
        self.consume('WHILE')
        self.consume('LPAREN')
        condition = self.expression()
        self.consume('RPAREN')
        self.consume('LBRACE')
        body = self.block()
        self.consume('RBRACE')
        return ('while', condition, body)

    def function_statement(self):
        self.consume('FUNCTION')
        func_name = self.consume('IDENTIFIER')
        self.consume('LPAREN')
        parameters = []
        if not self.check('RPAREN'):
            parameters.append(self.consume('IDENTIFIER'))
            while self.match('COMMA'):
                parameters.append(self.consume('IDENTIFIER'))
        self.consume('RPAREN')
        self.consume('LBRACE')
        body = self.block()
        self.consume('RBRACE')
        return ('function', func_name, parameters, body)

    def return_statement(self):
        self.consume('RETURN')
        value = self.expression()
        self.consume('SEMICOLON')
        return ('return', value)

    def block(self):
        statements = []
        while not self.check('RBRACE'):
            statements.append(self.statement())
        return statements

    def expression(self):
        return self.binary_expression()

    def binary_expression(self):
        expr = self.term()
        while self.match('PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE', 'GT', 'LT', 'EQ'):
            operator = self.previous()
            right = self.term()
            expr = ('binary', operator, expr, right)
        return expr

    def term(self):
        expr = self.factor()
        while self.match('PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE', 'GT', 'LT', 'EQ'):
            operator = self.previous()
            right = self.factor()
            expr = ('binary', operator, expr, right)
        return expr

    def factor(self):
        expr = self.primary()
        while self.match('PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE', 'GT', 'LT', 'EQ'):
            operator = self.previous()
            right = self.primary()
            expr = ('binary', operator, expr, right)
        return expr

    def primary(self):
        if self.match('NUMBER'):
            return ('number', self.previous()[1])
        if self.match('STRING'):
            return ('string', self.previous()[1])
        if self.match('IDENTIFIER'):
            expr = ('variable', self.previous()[1])
            while self.match('LBRACKET'):
                index = self.expression()
                self.consume('RBRACKET')
                expr = ('index', expr, index)
            if self.match('LPAREN'):
                arguments = []
                if not self.check('RPAREN'):
                    while True:
                        arguments.append(self.expression())
                        if not self.match('COMMA'):
                            break
                self.consume('RPAREN')
                return ('call', expr, arguments)
            return expr
        if self.match('LPAREN'):
            expr = self.expression()
            self.consume('RPAREN')
            return expr
        if self.match('LBRACKET'):
            elements = []
            if not self.check('RBRACKET'):
                while True:
                    elements.append(self.expression())
                    if not self.match('COMMA'):
                        break
            self.consume('RBRACKET')
            return ('array', elements)
        raise SyntaxError(f'Expected expression, found {self.peek()[0]} at line {self.peek()[2]}, column {self.peek()[3]}')

    def function_call(self):
        func_name = self.previous()[1]
        self.consume('LPAREN')
        arguments = []
        if not self.check('RPAREN'):
            arguments.append(self.expression())
            while self.match('COMMA'):
                arguments.append(self.expression())
        self.consume('RPAREN')
        return ('call', func_name, arguments)

    def match(self, *token_types):
        for token_type in token_types:
            if self.check(token_type):
                self.advance()
                return True
        return False

    def consume(self, expected_type):
        if self.check(expected_type):
            return self.advance()[1]
        raise SyntaxError(f'Expected token {expected_type}, but got {self.peek()[0]} at line {self.peek()[2]}, column {self.peek()[3]}')

    def check(self, token_type):
        if self.is_at_end():
            return False
        return self.peek()[0] == token_type

    def advance(self):
        if not self.is_at_end():
            self.current_token_index += 1
        return self.previous()

    def is_at_end(self):
        return self.current_token_index >= len(self.tokens)

    def peek(self):
        if self.is_at_end():
            return None, None, None, None
        token_type, token_value, line, column = self.tokens[self.current_token_index]
        return token_type, token_value, line, column

    def previous(self):
        return self.tokens[self.current_token_index - 1]
