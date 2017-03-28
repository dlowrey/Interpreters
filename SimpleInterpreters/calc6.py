# Constants

INTEGER = 'INTEGER'
LPAREN = '('
RPAREN = ')'
PLUS = 'PLUS'
MINUS = 'MINUS'
MULTIPLICATION = 'MULTIPLICATION'
DIVISION = 'DIVISION'
EOF = 'EOF'


class Token:
    def __init__(self, type, value):
        # Token type
        self.type = type
        # Token value
        self.value = value

    def __str__(self):
        """
        String representation of the class instance.
        :return: Example: Token(INTEGER, 3)
        """
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=self.value
        )


class Lexer:
    def __init__(self, text):
        self.text = text  # the input string expression
        self.pos = 0  # pos used to index the text
        self.current_char = self.text[self.pos]  # current character in text

    def error(self):
        """ Raise an Exception"""
        raise Exception('Invalid character')

    def advance(self):
        """
        Advance the `pos` pointer and set the `current_char` variable.
        """
        self.pos += 1
        if self.pos <= len(self.text) - 1:
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None  # End of input

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        """ Return a (multidigit?) integer consumed from input"""
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def get_next_token(self):
        """ Lexical analyzer

            This method is responsible for breaking a sentence down into tokens
            one at a time
        """
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())

            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')

            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')

            if self.current_char == '*':
                self.advance()
                return Token(MULTIPLICATION, '*')

            if self.current_char == '/':
                self.advance()
                return Token(DIVISION, '/')

            if self.current_char == '(':
                self.advance()
                return Token(LPAREN, '(')

            if self.current_char == ')':
                self.advance()
                return Token(RPAREN, ')')

            self.error()

        return Token(EOF, None)


class Interpreter:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()  # set current token ot first token taken from input

    def error(self, error):
        raise Exception('Invalid syntax: ' + error)

    def eat(self, token_type):
        """
        Compare the `self.current_token.type` with the passed `token_type`
        and if they match, "eat" the `self.current_token` and assign
        the next token to `self.current_token`
        :param token_type: the token type we expect

        """
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error('EAT: Got {curr_token_type} but was expecting {expecting}'.format(
                curr_token_type=self.current_token.type,
                expecting=token_type)
            )

    def factor(self):
        """ factor: INTEGER | LPAREN expr RPAREN """
        token = self.current_token
        if token.type == INTEGER:
            self.eat(INTEGER)  # a factor is an INTEGER
            return token.value
        elif token.type == LPAREN:
            self.eat(LPAREN)
            result = self.expr()
            self.eat(RPAREN)
            return result

    def term(self):
        """
        term: factor MUL factor
            : factor DIV factor
            : factor

        """
        result = self.factor()  # term must start with a factor

        while self.current_token.type in (MULTIPLICATION, DIVISION):
            token = self.current_token
            if token.type == MULTIPLICATION:
                self.eat(MULTIPLICATION)
                result = result * self.factor()
            elif token.type == DIVISION:
                self.eat(DIVISION)
                result = result / self.factor()

        return result

    def expr(self):
        """
        Arethmetic expression parser / interpreter
        Using grammar:

            expr: term PLUS term
                : term MINUS term
                : term
            term: factor MULTIPLICATION factor
                : factor DIVISION factor
                : factor
            factor: INTEGER

        """

        result = self.term()

        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
                result = result + self.term()
            elif token.type == MINUS:
                self.eat(MINUS)
                result = result - self.term()

        return result


def main():
    while True:
        try:
            text = input('calc> ')
        except EOFError:
            break
        if not text:
            continue
        lexer = Lexer(text)
        interpreter = Interpreter(lexer)
        result = interpreter.expr()
        print(result)


if __name__ == '__main__':
    main()
