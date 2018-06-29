# token类型
#
# EOF token被用来表示再没有用来语法分析的输入了

INTEGER, PLUS, MINUS, EOF = "INTEGER", "PLUS", "MINUS", "EOF"


class Token(object):
    def __init__(self, type, value):
        # token类型：INTEGER, PLUS, EOF
        self.type = type
        # token值：0, 1, 2, 3, 4, 5, 6, 7, 8, 9, '+' 或者 None
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


class Interpreter(object):
    def __init__(self, text):
        # 字符串输入，比如"3+5"
        self.text = text
        # self.pos是self.text的下标索引
        self.pos = 0
        # 当前的token实例
        self.current_token = None

    def error(self):
        return Exception("Error parsing input")

    def get_next_token(self):
        """ 语义分析器(tokenizer)

        这个方法被用来将一条语句分解成tokens(一次一个token)
        """
        text = self.text

        # 是否self.pos超出了self.text的最大索引了？
        # 如果是的话，返回EOF(因为没有需要再转换成token的输入了)
        if self.pos > len(text) - 1:
            return Token(EOF, None)

        # 取self.text中self.pos位置上的字符
        # 并由这单个字符决定创建什么token
        current_char = text[self.pos]

        # 如果字符是一个数字，就将其转换成integer，并创建一个INTEGER token
        # 并递增self.pos，后返回INTEGER token
        # 这里的数字可以>9

        if current_char.isdigit():
            val = 0
            while self.pos < len(text) and text[self.pos].isdigit():
                current_char = text[self.pos]
                val = (val * 10 + int(current_char))
                self.pos += 1
            return Token(INTEGER, val)

        if current_char == '+':
            token = Token(PLUS, current_char)
            self.pos += 1
            return token

        # 如果是空格则跳过
        # 并且返回空格后面的token
        if current_char.isspace():
            self.skip_space()
            return self.get_next_token()


        self.error()

    def eat(self, token_type):
        # 将当前的token和传入的token类型相比较
        # 如果符合，则"eat"当前的token
        # 并且将下一个token赋给self.current_token
        # 否则引发一个错误
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def expr(self):
        """expr -> INTEGER PLUS INTEGER"""
        # 将当前的token设置为从输入得到的第一个token
        self.current_token = self.get_next_token()

        # 期望当前的token是一个单字符的数字
        left = self.current_token
        self.eat(INTEGER)

        # 期望当前的token是一个'+'
        op = self.current_token
        self.eat(PLUS)

        # 期望当前的token是一个单字符数字
        right = self.current_token
        self.eat(INTEGER)

        # 经过了上面的解析之后，current_token被设置为EOF

        # 此时 `INTEGER PLUS INTEGER`序列已经被成功解析
        # 所以只需要返回加法运算的结果就OK了
        result = left.value + right.value
        return result

    def skip_space(self):
        while self.pos < len(self.text) and self.text[self.pos].isspace():
            self.pos += 1


def main():
    while True:
        try:
            text = input("calc> ")
        except EOFError:
            break
        if not text:
            continue
        interpreter = Interpreter(text)
        result = interpreter.expr()
        print(result)

        
if __name__ == "__main__":
    main()
