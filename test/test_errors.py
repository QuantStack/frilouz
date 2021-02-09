import unittest
import astunparse
import ast
import frilouz

class TestErrors(unittest.TestCase):

    def test_fine(self):
        code = 'def foo(): pass'
        tree, errors = frilouz.parse(ast.parse, code)
        self.assertFalse(errors);
        self.assertEqual(astunparse.unparse(tree).strip(),
                         'def foo():\n    pass')

    def test_faulty_top(self):
        code = 'return def'
        tree, errors = frilouz.parse(ast.parse, code)
        self.assertTrue(errors);
        self.assertEqual(astunparse.unparse(tree).strip(),
                         'pass')


    def test_faulty_func(self):
        code = 'def foo():pass\ndef oops(): return return\ndef bar():pass'
        tree, errors = frilouz.parse(ast.parse, code)
        self.assertTrue(errors);
        self.assertEqual(astunparse.unparse(tree).strip(),
                         'def foo():\n    pass\n'
                         'pass\n\n'
                         'def bar():\n    pass')

    def test_faulty_nested_func(self):
        code = 'def foo():\n\tdef oops(): return return\ndef bar():pass'
        tree, errors = frilouz.parse(ast.parse, code)
        self.assertTrue(errors);
        self.assertEqual(astunparse.unparse(tree).strip(),
                         'pass\n'
                         'pass\n\n'
                         'def bar():\n    pass')

    def test_faulty_nested_func_multiline(self):
        code = 'def foo():\n\tx = 1\n\tdef oops(): return return'
        tree, errors = frilouz.parse(ast.parse, code)
        self.assertTrue(errors);
        self.assertEqual(astunparse.unparse(tree).strip(),
                         'def foo():\n'
                         '    x = 1\n'
                         '    pass')

    def test_faulty_func_multiline(self):
        code = 'def foo():pass\ndef oops():\n return return\ndef bar():pass'
        tree, errors = frilouz.parse(ast.parse, code)
        self.assertTrue(errors);
        self.assertEqual(astunparse.unparse(tree).strip(),
                         'def foo():\n    pass\n'
                         'pass\n'
                         'pass\n\n'
                         'def bar():\n    pass')

    def test_faulty_class(self):
        code = 'def foo():pass\nclass oops(): def\ndef bar():pass'
        tree, errors = frilouz.parse(ast.parse, code)
        self.assertTrue(errors);
        self.assertEqual(astunparse.unparse(tree).strip(),
                         'def foo():\n    pass\n'
                         'pass\n\n'
                         'def bar():\n    pass')

    def test_faulty_class_multiline(self):
        code = 'def foo():pass\nclass oops(): \ndef\ndef bar():pass'
        tree, errors = frilouz.parse(ast.parse, code)
        self.assertTrue(errors);
        self.assertEqual(astunparse.unparse(tree).strip(),
                         'def foo():\n    pass\n'
                         'pass\n'
                         'pass\n\n'
                         'def bar():\n    pass')
