INTEGER, EOF = "INTEGER", "EOF"
PLUS, MINUS, MULTI, DIVID = "PLUS", "MINUS", "MULTI", "DIVID"
LPAREN, RPAREN = "LPAREN", "RPAREN"


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


###############################################################################
#                                                                             #
#      lexer                                                                  #
#                                                                             #
#                                                                             #
###############################################################################

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
        """
        词法分析器
        将语句分解为一个一个Token
        一次产生一个token
        """
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

            if self.current_char == '(':
                self.advance()
                return Token(LPAREN, '(')

            if self.current_char == ')':
                self.advance()
                return Token(RPAREN, ')')

            self.error()

        return Token(EOF, None)


###############################################################################
#                                                                             #
#      parser                                                                 #
#                                                                             #
#                                                                             #
###############################################################################

class AST(object):
    """
    抽象语法树(Abstract Syntax Tree)
    用来派生其他的子类，如Num，BinOp等
    """
    pass


class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right


class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value


class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception("Invalid Syntax")

    def eat(self, token_type):
        """
        将当前的token type和传入的token type相比较
        如果相符的话，就eat，并且产生下一个token(赋值给self.current_token)
        否则就产生一个异常
        """
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        """
        factor : INTEGER | LPAREN expr RPAREN
        """
        token = self.current_token
        if token.type == INTEGER:
            self.eat(INTEGER)
            return Num(token)
        elif token.type == LPAREN:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
            return node

    def term(self):
        """
        term : factor ((MULTI | DIVID) factor)*
        """
        node = self.factor()

        while self.current_token.type in (MULTI, DIVID):
            token = self.current_token
            if token.type == MULTI:
                self.eat(MULTI)
            elif token.type == DIVID:
                self.eat(DIVID)

            node = BinOp(left=node, op=token, right=self.factor())

        return node

    def expr(self):
        """
        factor : INTEGER | LPAREN expr RPAREN
        term   : factor ((MULTI | DIVID) factor)*
        expr   : term ((PLUS | MINUS) term)*
        """
        node = self.term()

        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
            elif token.type == MINUS:
                self.eat(MINUS)

            node = BinOp(left=node, op=token, right=self.term())

        return node

    def parse(self):
        node = self.expr()
        if self.current_token.type != EOF:
            self.error()
        return node


###############################################################################
#                                                                             #
#      interpreter                                                            #
#                                                                             #
#                                                                             #
###############################################################################

class NodeVisitor(object):
    def visit(self, node):
        method_name = "visit_" + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception("No visit_{} method".format(type(node).__name__))


class RPNNodeVisitor(object):
    def rpn_visit_BinOp(self, node):
        self.visit(node.left)
        self.visit(node.right)
        print(node.op.value, end=" ")

    def rpn_visit_Num(self, node):
        print(node.value, end=" ")

    def visit(self, node):
        method_name = "rpn_visit_" + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception("No visit_{} method".format(type(node).__name__))


class LispNodeVisitor(object):
    def lisp_visit_BinOp(self, node):
        print("(", end="")
        print(node.op.value, end=" ")
        self.visit(node.left)
        self.visit(node.right)
        print("\b)", end=" ")

    def lisp_visit_Num(self, node):
        print(node.value, end=" ")

    def visit(self, node):
        method_name = "lisp_visit_" + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception("No visit_{} method".format(type(node).__name__))


class Interpreter(NodeVisitor):
    def __init__(self, parser):
        self.parser = parser

    def visit_BinOp(self, node):
        if node.op.type == PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == MULTI:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type == DIVID:
            return self.visit(node.left) / self.visit(node.right)

    def visit_Num(self, node):
        return node.value

    def interpret(self):
        tree = self.parser.parse()
        return self.visit(tree)


def main():
    while True:
        try:
            text = input("calc> ")
        except EOFError:
            break
        if not text:
            continue
        lexer = Lexer(text)
        parser = Parser(lexer)
        root = parser.parse()
        rpn_visitor = RPNNodeVisitor()
        rpn_visitor.visit(root)
        print()
        lisp_visitor = LispNodeVisitor()
        lisp_visitor.visit(root)
        print()
        """
        interpreter = Interpreter(parser)
        result = interpreter.interpret()
        print(result)
        """


if __name__ == "__main__":
    main()
