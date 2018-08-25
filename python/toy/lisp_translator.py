import unittest
from calculator import Lexer, Parser


class LispNodeVisitor(object):
    def __init__(self, root):
        self.tree = root

    def lisp_visit_BinOp(self, node):
        left_val = self.visit(node.left)
        right_val = self.visit(node.right)
        return "({op} {left} {right})".format(
                op = node.op.value,
                left = left_val,
                right = right_val,
        )

    def lisp_visit_Num(self, node):
        return node.value

    def visit(self, node):
        method_name = "lisp_visit_" + type(node).__name__
        visitor = getattr(self, method_name, self.genetic_visit)
        return visitor(node)

    def genetic_visit(self, node):
        raise Exception("No lisp_visit_{} method".format(type(node).__name__))

    def translate(self):
        return self.visit(self.tree)


def get_lisp(text):
    lexer = Lexer(text)
    parser = Parser(lexer)
    root = parser.parse()
    lisp_visitor = LispNodeVisitor(root)
    return lisp_visitor.translate()


class LispTest(unittest.TestCase):
    def test_1(self):
        self.assertEqual(get_lisp("3 * (4 + 5)"), "(* 3 (+ 4 5))")

    def test_2(self):
        self.assertEqual(get_lisp("(13 + 37) / (3 * (3 + (2 * 5)))"), "(/ (+ 13 37) (* 3 (+ 3 (* 2 5))))")

    def test_3(self):
        self.assertEqual(get_lisp("7 + 5 * 2 - 3"), "(- (+ 7 (* 5 2)) 3)")


if __name__ == "__main__":
    unittest.main()
