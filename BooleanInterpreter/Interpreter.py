EOF, EOF_VAL = 'EOF', '.'
TRUE, TRUE_VAL = 'TRUE', 'T'
FALSE, FALSE_VAL = 'FALSE', 'F'
AND, AND_VAL = 'AND', '^'
OR, OR_VAL = 'OR', 'v'
IMPLY, IMPLY_VAL, IMPLY_VAL1, IMPLY_VAL2 = 'IMPLIES', '->','-', '>'
NOT, NOT_VAL = 'NOT', '~'
LPAREN, LPAREN_VAL = 'LPAREN', '('
RPAREN, RPAREN_VAL = 'RPAREN', ')'

BOOL_LIST = '~ , T, F, or ('
IMPLY_LIST = '~, T, F ('
IMPLY_TAIL_LIST = '->, ., )'
OR_LIST = '~, T, F, ('
OR_TAIL_LIST = 'v, ->, ., )'
AND_LIST = '~, T, F, ('
AND_TAIL_LIST = '^, v, ->, ., )'
LITERAL_LIST = 'T, F, (, ~'
ATOM_LIST = 'T, F, ~, ('



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

    @staticmethod
    def error(expecting=None, got=None):
        """Raise a detailed Invalid character error
            Can be called with all, one, or no parameters.
        """
        if expecting is not None:
            raise Exception('Expecting \'{expecting}\', got \'{got}\' instead.'.format(
                expecting=expecting,
                got=got,
            ))
        else:
            raise Exception('Invalid character: \'{got}\''.format(got=got))

    def advance(self):
        """Advance the `pos` pointer and set the `current_char` variable"""
        self.pos += 1
        if self.pos <= len(self.text) - 1:
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None

    def implies(self):
        """Creates an imply '->' character for a Token
            object from the input string.
            error() otherwise
        """
        result = self.current_char
        self.advance()
        result += self.current_char
        if result == IMPLY_VAL:
            self.advance()
            return result
        else:
            self.error(expecting=IMPLY_VAL, got=result)

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def get_next_token(self):
        """Lexical analyzer

        This method is responsible for breaking an input string apart
        into tokens one at a time, until the EOF value is found.

        Valid Tokens:
                '.' (EOF)
                ' ' (whitespace)
                '^' (and)
                'v' (or)
                '->' (implies)
                '~' (not)
                'T' (true)
                'F' (false)
                '(' (left parenthesis)
                ')' (right parenthesis)
        error otherwise
        """
        while self.current_char is not EOF_VAL:

            # EOF missing
            if self.current_char is None:
                self.error(expecting=EOF_VAL, got=self.current_char)

            elif self.current_char.isspace():
                self.skip_whitespace()
                continue

            elif self.current_char == AND_VAL:
                self.advance()
                return Token(AND, AND_VAL)

            elif self.current_char == OR_VAL:
                self.advance()
                return Token(OR, OR_VAL)

            elif self.current_char == IMPLY_VAL1:
                return Token(IMPLY, self.implies())

            elif self.current_char == NOT_VAL:
                self.advance()
                return Token(NOT, NOT_VAL)

            elif self.current_char == TRUE_VAL:
                self.advance()
                return Token(TRUE, TRUE_VAL)

            elif self.current_char == FALSE_VAL:
                self.advance()
                return Token(FALSE, FALSE_VAL)

            elif self.current_char == LPAREN_VAL:
                self.advance()
                return Token(LPAREN, LPAREN_VAL)

            elif self.current_char == RPAREN_VAL:
                self.advance()
                return Token(RPAREN, RPAREN_VAL)
            else:
                self.error(got=self.current_char)   # invalid character (?)

        return Token(EOF, EOF_VAL)  # EOF reached


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

    @staticmethod
    def error(expecting, got):
        """Raise a detailed Syntax error exception"""
        if expecting is not None and got is not None:
            raise Exception('Expecting \'{expecting}\', got \'{got}\' instead.'.format(
                expecting=expecting,
                got=got,
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

    def bool_stmt(self):
        """Bool_stmt non-terminal method

        <B> := <IT>.
        where <B> is Bool_stmt

        :return: True if `self.current_token` starts and completes one of the RHS of an Bool_stmt rule above,
                false otherwise
        """
        if self.imply_term():
            if self.current_token.type == EOF:
                return True
            else:
                return False
        else:
            self.error(expecting=BOOL_LIST, got=self.current_token.value)
            return False

    def imply_term(self):
        """Imply_term non-terminal method

        <IT> := -> <OT><IT_Tail>
                  :=
        where <IT> is Imply_term

        :return: True if `self.current_token` starts and completes one of the RHS of an Imply_term rule above,
                false otherwise
        """
        if self.or_term():
            if self.imply_tail():
                return True
            else:
                return False
        else:
            self.error(expecting=IMPLY_LIST, got=self.current_token.value)
            return False

    def imply_tail(self):
        """Imply_tail non-terminal method

        <IT_Tail> := -> <OT><IT_Tail>
                  :=
        where <IT_Tail> is Imply_tail

        :return: True if `self.current_token` starts and completes one of the RHS of an Imply_tail rule above,
                false otherwise
        """
        if self.current_token.type == IMPLY:
            self.eat(IMPLY)
            if self.or_term():
                if self.imply_tail():
                    temp2 = self.stack.pop()     # the second argument is at the top of the stack
                    temp1 = self.stack.pop()
                    self.stack.append((not temp1) or temp2)     # T->F is equivalent to ~T or F
                    return True
                else:
                    return False
            else:
                return False
        elif self.current_token.type in (EOF, RPAREN):  # selection set
            return True
        else:
            self.error(expecting=IMPLY_TAIL_LIST, got=self.current_token.value)
            return False

    def or_term(self):
        """Or_term non-terminal method

        <OT> := <AT> <OT_Tail>
        where <OT> is Or_term

        :return: True if `self.current_token` starts and completes one of the RHS of an Or_term rule above,
                false otherwise
        """
        if self.and_term():
            if self.or_tail():
                return True
            else:
                return False
        else:
            self.error(expecting=OR_LIST, got=self.current_token.value)
            return False

    def or_tail(self):
        """Or_tail non-terminal method

        <OT_Tail> := v<AT> <OT_Tail>
                  :=
        where <OT_Tail> is Or_tail

        :return: True if `self.current_token` starts and completes one of the RHS of an Or_tail rule above,
                false otherwise
        """
        if self.current_token.type == OR:
            self.eat(OR)
            if self.and_term():
                if self.or_tail():
                    temp2 = self.stack.pop()
                    temp1 = self.stack.pop()
                    self.stack.append(temp1 or temp2)
                    return True
                else:
                    return False
            else:
                return False
        elif self.current_token.type in (IMPLY, EOF, RPAREN):   # selection set
            return True
        else:
            self.error(expecting=OR_TAIL_LIST, got=self.current_token.value)
            return False

    def and_term(self):
        """And_term non-terminal method

        <AT> := <L><AT_Tail>
        where <AT> is And_term

        :return: True if `self.current_token` starts and completes one of the of an And_term rule above,
                false otherwise
        """
        if self.literal():
            if self.and_tail():
                return True
            else:
                return False
        else:
            self.error(expecting=AND_LIST, got=self.current_token.value)
            return False

    def and_tail(self):
        """And_tail non-terminal method

        <AT_Tail> := ^ <L> <AT_Tail>
                  :=
        where <AT_Tail> is And_tail

        :return: True if `self.current_token` starts and completes one of the RHS of an And_tail rule above,
                false otherwise
        """
        if self.current_token.type == AND:
            self.eat(AND)
            if self.literal():
                temp2 = self.stack.pop()    # the second argument is at the top of the stack
                temp1 = self.stack.pop()
                self.stack.append(temp1 and temp2)
                if self.and_tail():
                    return True
                else:
                    return False
            else:
                return False
        elif self.current_token.type in (EOF, RPAREN, OR, IMPLY):   # selection set
            return True
        else:
            self.error(expecting=AND_TAIL_LIST, got=self.current_token.value)
            return False

    def literal(self):
        """Literal non-terminal method

        <L> := <A>
            := ~<L>
        where <L> is Literal

        :return: True if `self.current_token`starts and completes one of the of a Literal rule above,
                false otherwise
        """
        if self.current_token.type == NOT:
            self.eat(NOT)
            if self.literal():
                temp = self.stack.pop()
                self.stack.append(not temp)
                return True
            else:
                return False
        elif self.atom():
            return True
        else:
            self.error(expecting=LITERAL_LIST, got=self.current_token.value)
            return False

    def atom(self):
        """Atom non-terminal method
        <A> := T
            := F
            := (<IT>)
        where <A> is Atom

        :return: True if `self.current_token` starts and completes one of the RHS of an Atom rule above,
                false otherwise
        """
        if self.current_token.type == TRUE:
            self.eat(TRUE)
            self.stack.append(True)
            return True
        elif self.current_token.type == FALSE:
            self.eat(FALSE)
            self.stack.append(False)
            return True
        elif self.current_token.type  == LPAREN:
            self.eat(LPAREN)
            if self.imply_term():
                if self.current_token.type == RPAREN:
                    self.eat(RPAREN)
                    return True
                else:
                    return False
            else:
                return False
        else:
            self.error(expecting=ATOM_LIST, got=self.current_token.value)
            return False



    def eval(self):
        """Boolean expression parser / interpreter

            Valid boolean statements must start with a <B> and end
            with a '.'

            See grammar rules of each individual non-terminal method above

        """
        if self.bool_stmt():
            return str(self.stack)


def main():
    while True:
        try:
            text = input('boolean expression> ')
        except EOFError:
            break
        if not text:
            continue
        lexer = Lexer(text)
        interpreter = Interpreter(lexer)
        try:
            result = interpreter.eval()
            print(result)
        except Exception as e:
            print(str(e))


if __name__ == '__main__':
    main()