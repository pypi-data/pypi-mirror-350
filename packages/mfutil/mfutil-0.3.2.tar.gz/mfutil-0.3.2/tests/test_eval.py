import sys

import unittest

import simpleeval

from mfutil import eval


class TestBasic(unittest.TestCase):
    # eval.py does not work with python2
    if sys.version_info.major >= 3:

        def setUp(self):
            self.s = eval

        def t(self, expr, variables, should_be):
            return self.assertEqual(self.s(expr, variables), should_be)

        def test_endswith(self):
            self.t("x.endswith('foo')", {"x": "/to/foo"}, True)

        def test_split(self):
            self.t("x.split('/')[-1] == 'foo'", {"x": "/to/foo"}, True)

        def test_instance(self):
            class Foo:
                def fullpath(self):
                    return "/to/foo"

            x = Foo()
            self.t("'foo' in x.fullpath()", {'x': x}, True)

        def test_re_match(self):
            self.t("bool(re_match('f[o]{2}', 'foo'))", None, True)
            self.t("bool(re_match('f[o]{2}', 'fox'))", None, False)

        def test_re_imatch(self):
            self.t("bool(re_imatch('f[o]{2}', 'Foo'))", None, True)
            self.t("bool(re_imatch('f[o]{2}', 'fox'))", None, False)

        def test_fnmatch(self):
            self.t("fnmatch_fnmatch('foo.txt', '*.txt')", None, True)

        def test_unsupported_function(self):
            with self.assertRaises(simpleeval.FunctionNotDefined):
                self.t("filter(None, (True, False))", None, (True,))

        def test_bytes_contains(self):
            self.t("b'1' in (1,2)", None, False)

        def test_bytes_endswith(self):
            self.t("b'toto.png'.endswith(b'png')", None, True)

        def test_dict(self):
            self.t("x['foo'] == b'png'", {'x': {'foo': b'png'}}, True)

        def test_bytes_in_variables(self):
            self.t("x['foo'].startswith(b'png')", {'x': {'foo': b'png'}}, True)
