import unittest
from analyzer.engine import analyze, score


def rules(src):
    return {f.rule for f in analyze(src)}


class RuleTests(unittest.TestCase):
    def test_clean(self):
        self.assertEqual(rules("def add(a, b):\n    return a + b\n"), set())

    def test_mutable_default(self):
        self.assertIn("mutable_default", rules("def f(a=[]):\n    return a\n"))

    def test_bare_except(self):
        self.assertIn("bare_except", rules("try:\n    1\nexcept:\n    raise\n"))

    def test_swallowed(self):
        self.assertIn("swallowed_error", rules("try:\n    1\nexcept ValueError:\n    pass\n"))

    def test_unused(self):
        self.assertIn("unused_variable", rules("def f():\n    x = 1\n    return 2\n"))

    def test_params(self):
        self.assertIn("too_many_params", rules("def f(a, b, c, d, e, g):\n    return a\n"))

    def test_long(self):
        self.assertIn("long_function", rules("def f():\n" + "    pass\n" * 31))

    def test_nesting(self):
        src = "def f(x):\n if x:\n  for i in x:\n   while i:\n    if i:\n     return 1\n"
        self.assertIn("deep_nesting", rules(src))

    def test_syntax_error(self):
        self.assertEqual(rules("def (:"), {"syntax_error"})

    def test_score_capped(self):
        self.assertEqual(score(analyze("def f(a=[]):\n    pass\n" * 10)), 100)


if __name__ == "__main__":
    unittest.main()
