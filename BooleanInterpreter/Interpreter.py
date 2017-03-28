EOF, EOF_VAL = 'EOF', '.'
TRUE, TRUE_VAL = 'TRUE', 'T'
FALSE, FALSE_VAL = 'FALSE', 'F'
AND, AND_VAL = 'AND', '^'
OR, OR_VAL = 'OR', 'v'
IMPLY, IMPLY_VAL1, IMPLY_VAL2 = 'IMPLIES', '-', '>'
NOT, NOT_VAL = 'NOT', '~'
LPAREN, LPAREN_VAL = 'LPAREN', '('
RPAREN, RPAREN_VAL = 'RPAREN', ')'
EMPTY, EMPTY_VAL = 'EMPTY', 'e'


class Token(object):
    """ A representation of a (Non)terminal and its value.

    `Token` is used to represent Non terminals and terminals as type-pair objects.

    Attributes:
            :type: the token type represents the (non)terminal's type in the
            grammar rules it belongs to
            :value: the token value is the value of the token
    """

    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        """String representation of a Token object"""
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=self.value
        )


class Lexer(object):
    """Lexical analyzer used to parse input string and break into tokens

    Converts the input string into Tokens for the interpreter as needed
    until EOF type token is hit.

    Arguments:
        :text: the input string to be analyzed
    """

    def __init__(self, text):
        self.text = text
        self.pos = 0  # self.pos used to index text
        self.current_char = text[self.pos]  # set the current_char to the first character in the text

    def error(self, msg):
        raise Exception("Invalid character: {msg}".format(
            msg=msg
        ))

    def advance(self):
        """Advance the `pos` pointer and set the `current_char` variable"""
        self.pos += 1
        if self.pos <= len(self.text) - 1:
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None

    def implies(self):
        result = self.current_char
        self.advance()
        if self.current_char == IMPLY_VAL2:
            result += self.current_char
            self.advance()
            return result
        else:
            self.error("expected {end_of_implies} got {char}".format(
                end_of_implies=IMPLY_VAL2,
                char=self.current_char
            ))

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def get_next_token(self):
        """Lexical analyzer

        This method is responsible for breaking an input string apart
        into tokens one at a time.
        """
        while self.current_char is not EOF_VAL:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char == AND_VAL:
                self.advance()
                return Token(AND, AND_VAL)

            if self.current_char == OR_VAL:
                self.advance()
                return Token(OR, OR_VAL)

            if self.current_char == IMPLY_VAL1:
                return Token(IMPLY, self.implies())

            if self.current_char == NOT_VAL:
                self.advance()
                return Token(NOT, NOT_VAL)

            if self.current_char == TRUE_VAL:
                self.advance()
                return Token(TRUE, TRUE_VAL)

            if self.current_char == FALSE_VAL:
                self.advance()
                return Token(FALSE, FALSE_VAL)



        return Token(EOF, EOF_VAL)


class Interpreter(object):
    """Interpret the value of the expressions

    The interpreter evaluates partial and whole expressions that are
    in the forms of tokens. Expressions must be Lexically analyzed before
    interpreted.

    Arguments:
        :lexer: the lexical analyzer, used for retrieving tokens
                to be used in evaluation
    """

    def __init__(self, lexer):
        self.lexer = lexer
        # set current token to the first token taken from input
        self.current_token = self.lexer.get_next_token()
        self.stack = []


    def error(self, expecting, got):
        if expecting is not None and got is not None:
            raise Exception('Expecting {expecting}, got {got} instead. VALUE: {val}'.format(
                expecting=expecting,
                got=got,
                val=self.current_token.value
            ))
        else:
            raise Exception('Syntax error')

    def eat(self, token_type):
        """Consume the token if the current token matches the passed token

        Compares the input's token type to the expected token that is passed.
        If they match, the token is consumed and `self.current_token` is set to the
        next token.
        Arguments:
            :token_type: the type of token that the interpreter expects
        Raises:
            Exception: an Exception describing invalid syntax (the token in the input
            string did not match the expected token
        """
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error(expecting=token_type, got=self.current_token.type)

    def bool_term(self):
        if self.imply_term():
            if self.current_token.value == EOF_VAL:
                return True
            else:
                return False
        else:
            self.error(expecting='BOOL TERM', got=self.current_token.type)

    def imply_term(self):
        if self.or_term():
            if self.imply_tail():
                return True
            else:
                return False
        else:
            self.error(expecting='IMPLY TERM', got=self.current_token.type)
            return False

    def imply_tail(self):
        if self.current_token.value == IMPLY_VAL1 + IMPLY_VAL2:
            self.current_token = self.lexer.get_next_token()
            if self.or_tail():
                if self.imply_tail():
                    return True
                else:
                    return False
            else:
                return False
        elif self.current_token.value in (EOF_VAL, RPAREN_VAL):
            self.current_token == self.lexer.get_next_token()
            return True
        else:
            self.error(expecting='IMPLY TAIL', got=self.current_token.type)
            return False

    def or_term(self):
        if self.and_term():
            if self.or_tail():
                return True
            else:
                return False
        else:
            self.error(expecting='OR TERM', got=self.current_token.type)

    def or_tail(self):
        if self.current_token.value == OR_VAL:
            self.current_token = self.lexer.get_next_token()
            if self.and_term():
                if self.or_tail():
                    return True
                else:
                    return False
            else:
                return False
        elif self.current_token.value in (IMPLY_VAL1+IMPLY_VAL2, EOF_VAL):
            self.current_token = self.lexer.get_next_token()
            return True
        else:
            self.error(expecting='OR TAIL', got=self.current_token.type)
            return False

    def and_term(self):
        if self.literal():
            if self.and_tail():
                return True
            else:
                return False
        else:
            self.error(expecting='AND TERM', got=self.current_token.type)
            return False

    def and_tail(self):
        if self.current_token.value == AND_VAL:
            self.current_token = self.lexer.get_next_token()
            if self.literal():
                if self.and_tail():
                    return True
                else:
                    return False
            else:
                return False
        elif self.current_token.value in (EOF_VAL, RPAREN_VAL, OR_VAL, IMPLY_VAL1+IMPLY_VAL2):
            self.current_token = self.lexer.get_next_token()
            return True
        else:
            self.error(expecting='AND TAIL', got=self.current_token.type)
            return False



    def literal(self):
        if self.current_token.value == NOT_VAL:
            self.current_token = self.lexer.get_next_token()
            if self.literal():
                temp = self.stack.pop()
                self.stack.append(not temp)
                return True
            else:
                return False
        elif self.atom():
            return True
        else:
            self.error(expecting='LITERAL', got=self.current_token.type)
            return False

    def atom(self):
        if self.current_token.value == TRUE_VAL:
            self.stack.append(True)
            self.current_token = self.lexer.get_next_token()
            return True
        elif self.current_token.value == FALSE_VAL:
            self.stack.append(False)
            self.current_token = self.lexer.get_next_token()
            return True
        elif self.current_token.value == LPAREN_VAL:
            if self.imply_term():
                if self.current_token.value == RPAREN_VAL:
                    self.current_token = self.lexer.get_next_token()
                    return True
                else:
                    return False
            else:
                return False
        else:
            self.error(expecting='ATOM', got=self.current_token.type)
            return False



    def eval(self):
        """Boolean expression parser / interpreter

            T ^ F

        """
        if self.bool_term():
            print(str(self.stack))


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
        result = interpreter.eval()
        print(result)


if __name__ == '__main__':
    main()