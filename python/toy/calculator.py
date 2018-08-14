INTEGER, EOF = "INTEGER", "EOF"
PLUS, MINUS, MULTI, DIVID = "PLUS", "MINUS", "MULTI", "DIVID"


class Token(object):
    def __init__(self, type, value):
        # token类型：INTEGER, PLUS, EOF
        self.type = type
        # token值：0, 1, 2, 3, 4, 5, 6, 7, 8, 9, '+', '-', '*', '/' 或者 None
        self.value = value

    def __str__(self):
        """
        类实例的string表示

        例子：
            Token(INTEGER, 3)
            Token(PLUS, '+')
        """
        return 'Token({type}, {value})'.format(
                type=self.type,
                value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()


class Lexer(object):
    def __init__(self, text):
        # 输入的字符串 "3 * 5", "12 /7 * 13"
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception("Invalid character")

    def advance(self):
        # 将pos前进一步
        # 并设置current_char
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        # 将字符串解析为数字
        # 并返回数值
        result = ""
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()

        return int(result)

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())

            if self.current_char == '*':
                self.advance()
                return Token(MULTI, '*')

            if self.current_char == '/':
                self.advance()
                return Token(DIVID, '/')

            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')

            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')

        return Token(EOF, None)


class Interpreter(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception("Invalid syntax")

    def eat(self, token_type):
        """ 验证现时的token的type是否是token_type
        `token_type`是current_token应有的类型
        """
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        """返回一个INTEGER的token值
        factor: INTEGER
        """
        token = self.current_token
        self.eat(INTEGER)
        return token.value

    def term(self):
        """ 处理乘除运算
        term : factor ((MUL | DIV) factor)*
        """
        result = self.factor()
        while self.current_token.type in (MULTI, DIVID):
            token = self.current_token
            if token.type == MULTI:
                self.eat(MULTI)
                result = result * self.factor()
            elif token.type == DIVID:
                self.eat(DIVID)
                try:
                    result = result / self.factor()
                except ZeroDivisionError:
                    raise Exception("division cannot be zero")

        return result

    def expr(self):
        """算术运算解释器
        expr   : term ((PLUS | MINUS) term)*
        term   : factor ((MUL | DIV) factor)*
        factor : INTEGER
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
            text = input("calc> ")
        except EOFError:
            break
        if not text:
            continue
        lexer = Lexer(text)
        interpreter = Interpreter(lexer)
        result = interpreter.expr()
        print(result)


if __name__ == "__main__":
    main()
