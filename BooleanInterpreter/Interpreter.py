EOF = 'EOF'
TRUE = 'T'
FALSE = 'F'
LPAREN = '('
RPAREN = ')'


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
        return 'Token({type}, {value}'.format(
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

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def get_next_token(self):
        """Lexical analyzer

        This method is responsible for breaking an input string apart
        into tokens one at a time.
        """
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            pass
        return Token(EOF, None)


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

    def error(self, msg):
        raise Exception("Invalid syntax: {msg}".format(
            msg=msg
        ))

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
            self.error("{token_type} expected, {current_token_type} found".format(
                token_type=token_type,
                current_token_type=self.current_token.type
            ))

    def eval(self):
        """Boolean expression parser / interpreter


        """
        pass
