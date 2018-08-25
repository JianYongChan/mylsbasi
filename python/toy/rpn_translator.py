import unittest
from calculator import Lexer, Parser, NodeVisitor


class RPNNnodeVisitor(object):
    def __init__(self, root):
        self.tree = root

    def rpn_visit_BinOp(self, node):
        left_val = self.visit(node.left)
        right_val = self.visit(node.right)
        return "{left} {right} {op}".format(
            left = left_val,
            right = right_val,
            op = node.op.value,
        )

    def rpn_visit_Num(self, node):
        return node.value

    def visit(self, node):
        method_name = "rpn_visit_" + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception("No visit_{} method".format(type(node).__name__))

    def translate(self):
        return self.visit(self.tree)


def get_rpn(text):
    lexer = Lexer(text)
    parser = Parser(lexer)
    root = parser.parse()
    rpn_visitor = RPNNnodeVisitor(root)
    return rpn_visitor.translate()


class RPNTest(unittest.TestCase):
    def test_1(self):
        self.assertEqual(get_rpn("3 + 4"), "3 4 +")

    def test_2(self):
        self.assertEqual(get_rpn("37 * (7 + 13)"), "37 7 13 + *")

    def test_3(self):
        self.assertEqual(get_rpn("5 + ((1 + 2) * 4) - 3"), "5 1 2 + 4 * + 3 -")

    def test_4(self):
        self.assertEqual(get_rpn("(5 + 3) * 12 / 3"), "5 3 + 12 * 3 /")

if __name__ == "__main__":
    unittest.main()
