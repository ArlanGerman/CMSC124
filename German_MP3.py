
class ArithmeticParser:
    def __init__(self, string: str) -> None:
        self.string = string  # String to be parsed
        self.index = 0  # Current Index
        self.open = 0  # Current Number of Open Expressions
        # Current token being examined
        self.currentToken = self.string[self.index]

        # Statement below checks whether string has an expression by not starting with the $ terminal
        try:
            # Next token to be examined
            self.nextToken = self.string[self.index + 1]
        except IndexError:
            raise ValueError()

        self.start()  # Starts parsing

    def lex(self):
        """Updates the current token with the next token in string"""
        self.index += 1
        if self.index < len(self.string):
            self.currentToken = self.string[self.index]
        if self.index + 1 < len(self.string):
            self.nextToken = self.string[self.index + 1]

    def start(self):
        """Initiates parsing procedure"""
        self.expression()
        # Checks if current token is the $ terminal and if there are no open expressions
        if self.currentToken == '$' and self.open == 0:
            return True
        else:
            raise ValueError()

    def expression(self):
        """Implementation of <expr> ::= <expr>+<term> | <expr>-<term> | <term>"""
        if self.nextToken in {'+', '-'}:
            self.term()
            self.lex()
            self.expression()
        elif self.currentToken in ['+', '-'] and self.index > 0:
            self.lex()
            self.expression()
        else:
            self.term()

    def term(self):
        """Implementation of <term> ::= <term>*<factor> | <term>/<factor> | <factor>"""
        if self.nextToken in {'*', '/'}:
            self.factor()
            self.lex()
            self.term()
        elif self.currentToken in ['+', '-'] and self.index > 0:
            self.lex()
            self.expression()
        elif self.currentToken in ['*', '/'] and self.index > 0:
            self.lex()
            self.term()
        else:
            self.factor()

    def factor(self):
        """Implementation of <factor> ::= (<expr>) |<digit>"""
        if self.currentToken == '(':
            self.open += 1
            self.lex()
            self.expression()
            if self.currentToken == ')' and self.open > 0:
                self.open -= 1
                self.lex()
            if self.open == 0 and self.currentToken in {'+', '-'}:
                self.expression()
            elif self.open == 0 and self.currentToken in {'*', '/'}:
                self.term()
        else:
            self.digit()

    def digit(self):
        """Implementation of <digit> ::= 0|1|2|3"""
        if self.currentToken in {'0', '1', '2', '3'}:
            self.lex()
        else:
            raise ValueError()


class DigitsParser:
    def __init__(self, string: str) -> None:
        self.string = string  # String to be parsed
        self.index = 0  # Current Index
        # Current token being examined
        self.currentToken = self.string[self.index]

        # Statement below checks whether string has an expression by not starting with the $ terminal
        if len(self.string) > 1 and self.string.index('$') > 0:
            self.start()
        else:
            raise ValueError

    def lex(self):
        """Updates the current token with the next token in string"""
        self.index += 1
        if self.index < len(self.string):
            self.currentToken = self.string[self.index]

    def start(self):
        """Initiates parsing procedure"""
        self.expression()
        if self.currentToken == '$':
            return True
        else:
            raise ValueError()

    def expression(self):
        """Implementation of <expr> ::= +<num> | -<num> | <num>"""
        if self.currentToken in {'+', '-'}:
            self.lex()
            self.num()
        else:
            self.num()

    def num(self):
        """Implementation of <num> ::= <num><digits> | <digits>"""
        while self.currentToken != '$':
            self.digits()

    def digits(self):
        """<digits> ::= <digit> | <digit>.<digit>"""
        if self.currentToken == '.':
            self.lex()
            while self.currentToken != '$':
                self.digit()
        else:
            self.digit()

    def digit(self):
        """<digit> ::= 0|1|2|3|4|5|6|7|8|9"""
        if self.currentToken in {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}:
            self.lex()
        else:
            raise ValueError


if __name__ == '__main__':
    n = 1
    while n > 0 and n < 3:
        print("Menu:\n\t1. Arithmetic Parser\n\t2. Digits Parser\nAny key to exit\n\nSelect: ", end='')
        n = int(input())
        try:
            if n == 1:
                if ArithmeticParser(input("\nInput: ")):
                    print("\nResult: Valid\n")
            elif n == 2:
                if DigitsParser(input("\n\nInput: ")):
                    print("\nResult: Valid\n")
        except ValueError:
            print("\nResult: Invalid\n")
        except Exception as e:
            e.with_traceback()
