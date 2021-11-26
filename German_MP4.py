from typing import List, Tuple


class NotationConverter:
    def identify(self, expression: str) -> int:
        """Identifies the expression if it's either in infix (1), prefix (2), or postfix(3) notation"""
        expression = expression.rstrip().lstrip()
        if expression[-1] in {'+', '-', '/', '*', '^'}:
            return 3
        elif expression[0] in {'+', '-', '/', '*', '^'}:
            return 2
        elif expression[0].isalnum() or expression[0] == '(':
            return 1
        else:
            return 0

    def convert(self, expression: str, flag: int) -> Tuple[str, str]:
        """
        Converts given expression's notation into the other two notations.\n
        Parameters:
            expression: str
                expression to be converted
            flag: int
                current notation of expression

        """
        expression = expression.lstrip().rstrip()
        if flag == 1:
            return (self.__convertToPrefix(
                expression, flag), self.__convertToPostfix(expression, flag))
        elif flag == 2:
            return (self.__convertToInfix(
                expression, flag), self.__convertToPostfix(expression, flag))
        elif flag == 3:
            return (self.__convertToInfix(
                expression, flag), self.__convertToPrefix(expression, flag))
        else:
            raise ValueError(
                "Invalid expression. Cannot identify the current notation of the expression.")

    def __convertToPrefix(self, expression: str, flag: int) -> str:
        if flag == 1:
            # Infix to Prefix
            expression = ("".join(reversed(expression)).replace(
                '(', '~').replace(')', '(').replace('~', ')'))
            return "".join(list(reversed(self.__convertToPostfix(expression, flag))))

        elif flag == 3:
            # Postfix to Prefix
            i: int = 0
            stack: List[str] = []
            while i < len(expression):
                if expression[i] in {'+', '-', '/', '*', '^'}:
                    stack.append(
                        ' ' + expression[i] + stack.pop(-2) + stack.pop())
                    i = self.__lex(i)
                elif expression[i].isalnum():
                    operand = expression[i]
                    i = self.__lex(i)

                    if ' ' in expression and i < len(expression):
                        while expression[i].isalnum():
                            operand += expression[i]
                            i = self.__lex(i)

                    stack.append(' ' + operand)
                elif expression[i].isspace():
                    i = self.__lex(i)
                else:
                    raise ValueError()

            return "".join(stack[-1]).lstrip()
        else:
            raise ValueError()

    def __convertToInfix(self, expression: str, flag: int) -> str:
        if flag == 2:
            # Prefix to Infix
            stack: List[str] = []
            i: int = len(expression) - 1
            while i >= 0:
                if expression[i] in {'+', '-', '/', '*', '^'}:
                    stack.append(
                        '(' + stack.pop() + expression[i] + stack.pop() + ')')
                    i = self.__rlex(i)
                elif expression[i].isalnum():
                    operand = expression[i]
                    i = self.__rlex(i)

                    if ' ' in expression and i >= 0:
                        while expression[i].isalnum():
                            operand += expression[i]
                            i = self.__rlex(i)

                    stack.append(operand)
                elif expression[i].isspace():
                    i = self.__rlex(i)
                else:
                    raise ValueError()
            return stack[-1]

        elif flag == 3:
            # Postfix to Infix
            stack: List[str] = []
            i: int = 0
            while i < len(expression):
                if expression[i].isalnum():
                    operand = expression[i]
                    i = self.__lex(i)

                    if ' ' in expression and i < len(expression):
                        while expression[i].isalnum():
                            operand += expression[i]
                            i = self.__lex(i)

                    stack.append(operand)

                elif expression[i] in {'+', '-', '/', '*', '^'}:
                    stack.append(
                        '(' + stack.pop(-2) + expression[i] + stack.pop() + ')')
                    i = self.__lex(i)

                elif expression[i].isspace():
                    i = self.__lex(i)

                else:
                    raise ValueError()

            return stack[-1]
        else:
            raise ValueError()

    def __convertToPostfix(self, expression: str, flag: int) -> str:
        if flag == 1:
            # Infix to Postfix
            expression = "({})".format(expression)
            postfix = ""
            stack: List[str] = ['~']
            i = 0

            while i < len(expression):

                if expression[i].isalnum():

                    operand = expression[i]
                    i = self.__lex(i)

                    if ' ' in expression and i < len(expression):
                        while expression[i].isalnum():
                            operand += expression[i]
                            i = self.__lex(i)

                    postfix += ' ' + operand

                elif expression[i] == '(':

                    stack.append(expression[i])
                    i = self.__lex(i)

                elif expression[i] == ')':

                    while stack[-1] != '(':
                        postfix += ' ' + stack.pop()

                    stack.pop()
                    i = self.__lex(i)

                elif expression[i] in {'+', '-', '/', '*', '^'}:

                    if expression[i] == '^':

                        while self.__identifyTier(expression[i]) <= self.__identifyTier(stack[-1]):
                            postfix += ' ' + stack.pop()
                            i = self.__lex(i)

                    else:

                        while self.__identifyTier(expression[i]) < self.__identifyTier(stack[-1]):
                            postfix += ' ' + stack.pop()

                    stack.append(expression[i])
                    i = self.__lex(i)

                elif expression[i].isspace():

                    i = self.__lex(i)

                else:
                    raise ValueError()

            return (postfix + ' '.join(stack[1:])).lstrip()

        elif flag == 2:
            # Prefix to Postfix
            stack: List[str] = []
            i: int = len(expression) - 1

            while i >= 0:
                if expression[i] in {'+', '-', '/', '*', '^'}:
                    stack.append(stack.pop() +
                                 stack.pop() + ' ' + expression[i])
                    i = self.__rlex(i)
                elif expression[i].isalnum():
                    operand = expression[i]
                    i = self.__rlex(i)

                    if ' ' in expression and i >= 0:
                        while expression[i].isalnum():
                            operand += expression[i]
                            i = self.__rlex(i)

                    stack.append(' ' + operand)
                elif expression[i].isspace():
                    i = self.__rlex(i)
                else:
                    raise ValueError()

            return stack[-1].lstrip()
        else:
            raise ValueError()

    def __identifyTier(self, operator: str) -> int:
        """Determines the priority value of operators with accordance to PEMDAS"""
        if operator in {'+', '-'}:
            return 1
        elif operator in {'*', '/'}:
            return 2
        elif operator == '^':
            return 3
        else:
            return 0

    def __lex(self, index: int) -> int:
        return index + 1

    def __rlex(self, index: int) -> int:
        return index - 1


class InfixEvaluator:
    def __init__(self) -> None:
        self.converter = NotationConverter()
        self.index: int = 0

    def evaluate(self, expression: str) -> int:

        expression = expression.lstrip().rstrip()

        notation = self.converter.identify(expression)

        if notation == 1:
            expression = "({})".format(expression)
        elif notation == 2:
            expression = self.converter.convert(expression, notation)[0]
        elif notation == 3:
            expression = self.converter.convert(expression, notation)[0]
        else:
            raise ValueError()

        return self.__calculate(expression.replace(' ', ''))[0]

    def __calculate(self, expression: str):
        expressions: list = []

        while self.index < len(expression):
            operand: str = ""

            if expression[self.index] == '(':

                self.__lex()
                expressions += self.__calculate(expression)

            elif expression[self.index] == ')':

                self.__lex()
                return expressions

            elif expression[self.index].isnumeric():

                while expression[self.index].isnumeric():
                    operand += expression[self.index]
                    self.__lex()
                expressions.append(int(operand))

            elif expression[self.index] in {'+', '-', '/', '*', '^'}:
                if expression[self.index] == '+':
                    self.__lex()

                    while expression[self.index].isnumeric():
                        operand += expression[self.index]
                        self.__lex()

                    if operand.isnumeric():
                        expressions = [expressions[-1] +
                                       int(operand)]
                    else:
                        expressions = [expressions[-1] +
                                       self.__calculate(expression)[-1]]
                elif expression[self.index] == '-':
                    self.__lex()

                    while expression[self.index].isnumeric():
                        operand += expression[self.index]
                        self.__lex()

                    if operand.isnumeric():
                        expressions = [expressions[-1] -
                                       int(operand)]
                        self.__lex()
                    else:
                        expressions = [expressions[-1] -
                                       self.__calculate(expression)[-1]]

                elif expression[self.index] == '*':
                    self.__lex()

                    while expression[self.index].isnumeric():
                        operand += expression[self.index]
                        self.__lex()

                    if operand.isnumeric():
                        expressions = [expressions[-1] *
                                       int(operand)]
                        self.__lex()
                    else:
                        expressions = [expressions[-1] *
                                       self.__calculate(expression)[-1]]

                elif expression[self.index] == '/':
                    self.__lex()

                    while expression[self.index].isnumeric():
                        operand += expression[self.index]
                        self.__lex()

                    if operand.isnumeric():
                        expressions = [expressions[-1] //
                                       int(operand)]
                        self.__lex()
                    else:
                        expressions = [expressions[-1] //
                                       self.__calculate(expression)[-1]]

                elif expression[self.index] == '^':
                    self.__lex()

                    while expression[self.index].isnumeric():
                        operand += expression[self.index]
                        self.__lex()

                    if operand.isnumeric():
                        expressions = [expressions[-1] ** int(operand)]
                        self.__lex()
                    else:
                        expressions = [expressions[-1] **
                                       self.__calculate(expression)[-1]]
            else:
                raise ValueError()

        return expressions

    def __lex(self) -> None:
        self.index += 1


if __name__ == '__main__':
    n = 1

    while n > 0 and n < 3:
        expression = ""

        print("Menu:\n\t1. Convert any expression into the other two (2) notations\n\t2. Evaluate any expression\nAny key to exit\n\nSelect: ", end='')
        n = int(input())

        try:
            if n == 1:
                converter = NotationConverter()
                expression = input("\nExpression: ")
                print("\nResults:\n\t{}\n\t{}\n".format(*converter.convert(
                    expression, converter.identify(expression))))
            elif n == 2:
                evaluator = InfixEvaluator()
                expression = input("\nExpression: ")
                print("\nResult:\t{}\n".format(evaluator.evaluate(expression)))
        except ValueError:
            print("\nResult: Invalid\n")
        except IndexError:
            print("\nResult: Invalid\n")
        except Exception as e:
            e.with_traceback()
