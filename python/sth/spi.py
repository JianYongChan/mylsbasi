INTEGER, EOF = "INTEGER", "EOF"
PLUS, MINUS, MULTI, DIVID = "PLUS", "MINUS", "MULTI", "DIVID"
LPAREN, RPAREN = "LPAREN", "RPAREN"
BEGIN, END, ID, ASSIGN, SEMI, DOT = "BEGIN", "END", "ID", "ASSIGN", "SEMI", "DOT"


###############################################################################
#                                                                             #
#      lexer                                                                  #
#                                                                             #
#                                                                             #
###############################################################################

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


RESERVED_KEYWORDS = {
        "BEGIN": Token("BEGIN", "BEGIN"),
        "END": Token("END", "END"),
}


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

    def peek(self):
        # look forward
        peek_pos = self.pos + 1
        if peek_pos > len(self.text) - 1:
            return None
        else:
            return self.text[peek_pos]

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

    def _id(self):
        result = ""
        # isalnum表示为字母或者数字
        while self.current_char is not None and self.current_char.isalnum():
            result += self.current_char
            self.advance()

        token = RESERVED_KEYWORDS.get(result, Token(ID, result))
        return token

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

            if self.current_char.isalpha():
                return self._id()

            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())

            if self.current_char == ':' and self.peek() == '=':
                self.advance()
                self.advance()
                return Token(ASSIGN, '=')

            if self.current_char == ';':
                self.advance()
                return Token(SEMI, ';')

            if self.current_char == '.':
                self.advance()
                return Token(DOT, '.')

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


class UnaryOp(AST):
    """
    constructor接受两个参数
    op代表单目运算符
    expr表示一个AST节点
    """
    def __init__(self, op, expr):
        self.token = self.op = op
        self.expr = expr


class Compound(AST):
    """
    复合语句的class
    self.children表示该符合表达式所包含的所有子表达式
    是一个‘BEGIN ... END'语句块
    """
    def __init__(self):
        self.children = []


class Assign(AST):
    """
    left是一个Var节点
    right是由parser返回的一个节点
    """
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right


class Var(AST):
    """
    value是变量的名字
    """
    def __init__(self, token):
        self.token = token
        self.value = token.value


class NoOp(AST):
    """
    表示空表达式(empty expression)
    """
    pass


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

    def program(self):
        """
        program: compound_statement DOT
        """
        node = self.compound_statement()
        self.eat(DOT)
        return node

    def compound_statement(self):
        """
        compound_statement: BEGIN statement_list END
        """
        self.eat(BEGIN)
        nodes = self.statement_list()
        self.eat(END)

        root = Compound()
        for node in nodes:
            root.children.append(node)

        return root

    def statement_list(self):
        """
        statement_list: statement
                      | statement SEMI statement_list
        """
        node = self.statement()

        results = [node]

        while self.current_token.type == SEMI:
            self.eat(SEMI)
            results.append(self.statement())

        # 这一个判断不太懂
        if self.current_token.type == ID:
            self.error()

        return results

    def statement(self):
        """
        statement: compound_statement
                 | assign_statement
                 | empty
        """
        if self.current_token.type == BEGIN:
            node = self.compound_statement()
        elif self.current_token.type == ID:
            node = self.assign_statement()
        else:
            node = self.empty()

        return node

    def assign_statement(self):
        """
        assign_statement: variable ASSIGN expr
        """
        left = self.variable()
        token = self.current_token
        self.eat(ASSIGN)
        right = self.expr()
        node = Assign(left, token, right)
        return node

    def variable(self):
        """
        variable: ID
        """
        node = Var(self.current_token)
        self.eat(ID)
        return node

    def empty(self):
        return NoOp()

    def factor(self):
        """
        factor : (MULTI | PLUS)factor | INTEGER | LPAREN expr RPAREN
        """
        token = self.current_token
        if token.type == PLUS:
            self.eat(PLUS)
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == MINUS:
            self.eat(MINUS)
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == INTEGER:
            self.eat(INTEGER)
            return Num(token)
        elif token.type == LPAREN:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
        else:
            node = self.variable()
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
        """
        program: compound_statement DOT

        compound_statement: BEGIN statement_list END

        statement_list : statement
                       | statement SEMI statement_list

        statement : compound_statement
                  | assignment_statement
                  | empty

        assignment_statement : variable ASSIGN expr

        empty :

        expr : term ((PLUS | MINUS) term)*

        term : factor ((MULTI | DIVID) factor)*

        factor : PLUS factor
               | MINUS factor
               | INTEGER
               | LPAREN expr RPAREN
               | variable

        variable: ID
        """
        node = self.program()
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


class Interpreter(NodeVisitor):

    GLOBAL_SCOPE = {}

    def __init__(self, parser):
        self.parser = parser

    def visit_UnaryOp(self, node):
        op = node.op.type
        if op == PLUS:
            return +self.visit(node.expr)
        elif op == MINUS:
            return -self.visit(node.expr)

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

    def visit_Compound(self, node):
        for child in node.children:
            self.visit(child)

    def visit_NoOp(self, node):
        pass

    def visit_Assign(self, node):
        var_name = node.left.value
        self.GLOBAL_SCOPE[var_name] = self.visit(node.right)

    def visit_Var(self, node):
        var_name = node.value
        val = self.GLOBAL_SCOPE[var_name]
        if val is None:
            raise NameError(repr(var_name))
        else:
            return val

    def interpret(self):
        tree = self.parser.parse()
        if tree is None:
            return ''
        return self.visit(tree)


def main():
    import sys
    text = open(sys.argv[1], 'r').read()

    lexer = Lexer(text)
    parser = Parser(lexer)
    interpreter = Interpreter(parser)
    result = interpreter.interpret()
    print(interpreter.GLOBAL_SCOPE)


if __name__ == "__main__":
    main()