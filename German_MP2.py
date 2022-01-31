import string


class ExpressionParser:
    def __init__(self, string: str) -> None:
        self.string = string  # String to be parsed
        self.length = len(string)
        self.index = 0  # Current Index
        self.open = 0  # Current Number of Open Expressions
        # Current token being examined
        self.currentToken = self.string[self.index]

        # Statement below checks whether string has a variable and an operator
        try:
            # Next token to be examined
            self.nextToken = self.string[self.index + 1]
        except IndexError:
            raise ValueError()

        self.start()  # Starts parsing

    def lex(self):
        """Updates the current token with the next token in string"""
        self.index += 1
        if self.index < self.length:
            self.currentToken = self.string[self.index]
        if self.index + 1 < self.length:
            self.nextToken = self.string[self.index + 1]

    def start(self):
        """Initiates parsing procedure"""
        self.expression()
        # Checks if current token is the $ terminal and if there are no open expressions
        if self.index == self.length and self.open == 0:
            return True
        else:
            raise ValueError()

    def expression(self):
        """Implements <expr> ::= <term>+<expr> | <term>-<expr> | <term>"""
        if self.currentToken in {'+', '-'}:
            self.lex()
            self.expression()
        else:
            self.term()

    def term(self):
        """Implements <term> ::= (<expr>) | ~<variable> | <variable>"""
        if self.currentToken == '(':
            self.open += 1
            self.lex()
            self.expression()
        elif self.currentToken == ')':
            self.open -= 1
            self.lex()
        elif self.currentToken == '~':
            self.lex()
            self.variable()
        else:
            self.variable()

    def variable(self):
        """Implements <variable> ::= x | y | z"""
        if self.currentToken in {'x', 'y', 'z'}:
            self.lex()
            if self.currentToken in {'+', '-'}:
                self.expression()
            elif self.currentToken == ')':
                self.term()
        else:
            raise ValueError()


class PalindromeParser:
    def __init__(self, string: str) -> None:
        self.string = string.lower().replace(' ', '')
        self.index = 0
        self.length = len(self.string)
        self.currentToken = self.string[self.index]

        if self.length > 1:
            self.lastToken = self.string[self.length - 1]
            self.start()

    def lex(self):
        """Updates the current token with the next token in string"""
        self.index += 1
        if self.index < self.length:
            self.currentToken = self.string[self.index]
            self.lastToken = self.string[(self.length - 1) - self.index]

    def start(self):
        """Initiates parsing procedure"""
        self.palindrome()
        # Checks if current token is the $ terminal and if there are no open expressions
        if self.index == self.length // 2:
            return True
        else:
            raise ValueError()

    def palindrome(self):
        """Implements <palindrome> ::= a | aa | a<palindrome>a | ... | z | zz | z<palindrome>z """
        if self.length > 2:
            if self.currentToken in string.ascii_letters and self.currentToken == self.lastToken:
                self.lex()
                if self.index < self.length // 2:
                    self.palindrome()
            else:
                raise ValueError()

        elif self.length == 1 and self.currentToken in string.ascii_letters:
            self.lex()
        elif self.currentToken == self.lastToken and self.currentToken in string.ascii_letters:
            self.lex()
        else:
            raise ValueError()


if __name__ == '__main__':
    n = 1
    while n > 0 and n < 3:
        print("Menu:\n\t1. Expression Parser\n\t2. Palindrome Parser\nAny key to exit\n\nSelect: ", end='')
        n = int(input())
        try:
            if n == 1:
                if ExpressionParser(input("\nInput: ")):
                    print("\nResult: Valid\n")
            elif n == 2:
                if PalindromeParser(input("\nInput: ")):
                    print("\nResult: Valid\n")
        except ValueError:
            print("\nResult: Invalid\n")
        except Exception as e:
            e.with_traceback()
