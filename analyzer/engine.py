"""Runs every rule over the source and computes the haunting score."""
import ast
from .rules import RULES, Finding

WEIGHT = {1: 5, 2: 10, 3: 20}  # points added to the score per severity


def analyze(source):
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        return [Finding("syntax_error", e.lineno or 1, 3, e.msg)]
    findings = [f for r in RULES for f in r(tree)]
    return sorted(findings, key=lambda f: f.line)


def score(findings):
    return min(100, sum(WEIGHT[f.severity] for f in findings))
