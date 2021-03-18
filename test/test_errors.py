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

    def test_multiple_errors(self):
        code = 'return def\ndef (x):pass\nreturn def'
        tree, errors = frilouz.parse(ast.parse, code)
        self.assertEqual(len(errors), 3);
        self.assertEqual(astunparse.unparse(tree).strip(),
                         'pass\n'
                         'pass\n'
                         'pass')

    def test_faulty_func(self):
        code = 'def foo():pass\ndef oops(): return return\ndef bar():pass'
        tree, errors = frilouz.parse(ast.parse, code)
        self.assertEqual(len(errors), 1);
        self.assertEqual(astunparse.unparse(tree).strip(),
                         'def foo():\n    pass\n'
                         'pass\n\n'
                         'def bar():\n    pass')

    def test_faulty_nested_func(self):
        code = 'def foo():\n\tdef oops(): return return\ndef bar():pass'
        tree, errors = frilouz.parse(ast.parse, code)
        self.assertEqual(len(errors), 1);
        self.assertEqual(astunparse.unparse(tree).strip(),
                         'def foo():\n'
                         '    pass\n\n'
                         'def bar():\n    pass')

    def test_faulty_nested_func_multiline(self):
        code = 'def foo():\n\tx = 1\n\tdef oops(): return return'
        tree, errors = frilouz.parse(ast.parse, code)
        self.assertEqual(len(errors), 1);
        self.assertEqual(astunparse.unparse(tree).strip(),
                         'def foo():\n'
                         '    x = 1\n'
                         '    pass')

    def test_faulty_func_multiline(self):
        code = 'def foo():pass\ndef oops():\n return return\ndef bar():pass'
        tree, errors = frilouz.parse(ast.parse, code)
        self.assertEqual(len(errors), 1);
        self.assertEqual(astunparse.unparse(tree).strip(),
                         'def foo():\n    pass\n\n'
                         'def oops():\n    pass\n\n'
                         'def bar():\n    pass')

    def test_faulty_class(self):
        code = 'def foo():pass\nclass oops(): def\ndef bar():pass'
        tree, errors = frilouz.parse(ast.parse, code)
        self.assertEqual(len(errors), 1);
        self.assertEqual(astunparse.unparse(tree).strip(),
                         'def foo():\n    pass\n'
                         'pass\n\n'
                         'def bar():\n    pass')

    def test_faulty_nested_class(self):
        code = 'class oops(object):\n    class return: pass'
        tree, errors = frilouz.parse(ast.parse, code)
        self.assertTrue(errors);
        self.assertEqual(astunparse.unparse(tree).strip(),
                         'class oops(object):\n'
                         '    pass'
                        )

    def test_faulty_class_multiline(self):
        code = 'def foo():pass\nclass oops():\n def\ndef bar():pass'
        tree, errors = frilouz.parse(ast.parse, code)
        self.assertEqual(len(errors), 1);
        self.assertEqual(astunparse.unparse(tree).strip(),
                         'def foo():\n    pass\n\n'
                         'class oops():\n'
                         '    pass\n\n'
                         'def bar():\n    pass')

    def test_mutliple_top_level_stmt(self):
        code = 'def ok():pass\ndef ko(): &^$\n ok()\nok()\nko()'
        tree, errors = frilouz.parse(ast.parse, code)
        self.assertEqual(len(errors), 2);
        self.assertEqual(astunparse.unparse(tree).strip(),
                         'def ok():\n    pass\n'
                         'pass\npass\n'
                         'ok()\n'
                         'ko()')

    def test_faulty_after_dedent(self):
        code = 'if 1:\n if 2:\n  pass\n pass\n ! return'
        tree, errors = frilouz.parse(ast.parse, code)
        self.assertEqual(len(errors), 1);
        self.assertEqual(astunparse.unparse(tree).strip(),
                         'if 1:\n'
                         '    if 2:\n'
                         '        pass\n'
                         '    pass\n'
                         '    pass')


class TestMissingColumns(unittest.TestCase):

    def test_def(self):
        code = 'def foo():pass\ndef oops()\n pass\ndef bar(): pass'
        tree, errors = frilouz.parse(ast.parse, code)
        self.assertEqual(len(errors), 2);
        self.assertEqual(astunparse.unparse(tree).strip(),
                         'def foo():\n    pass\n'
                         'pass\n'
                         'pass\n\n'
                         'def bar():\n    pass'
                        )

    def test_class(self):
        code = 'def foo():pass\nclass oops\n pass\ndef bar(): pass'
        tree, errors = frilouz.parse(ast.parse, code)
        self.assertEqual(len(errors), 2);
        self.assertEqual(astunparse.unparse(tree).strip(),
                         'def foo():\n    pass\n'
                         'pass\n'
                         'pass\n\n'
                         'def bar():\n    pass'
                        )

    def test_stmt(self):
        code = 'def foo():\n if 1\n  pass\n'
        tree, errors = frilouz.parse(ast.parse, code)
        self.assertEqual(len(errors), 1);
        self.assertEqual(astunparse.unparse(tree).strip(),
                         'def foo():\n'
                         '    pass\n'
                         '    pass'
                        )

