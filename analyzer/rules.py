"""Detection rules. Each rule takes a parsed AST and yields Findings.
To add a rule: write a function and decorate it with @rule."""
import ast
from dataclasses import dataclass

FUNCS = (ast.FunctionDef, ast.AsyncFunctionDef)
BLOCKS = (ast.If, ast.For, ast.While, ast.Try, ast.With)
RULES = []


@dataclass
class Finding:
    rule: str
    line: int
    severity: int  # 1 minor, 2 major, 3 deadly
    detail: str = ""


def rule(fn):
    RULES.append(fn)
    return fn


def functions(tree):
    return [n for n in ast.walk(tree) if isinstance(n, FUNCS)]


def handlers(tree):
    return [n for n in ast.walk(tree) if isinstance(n, ast.ExceptHandler)]


@rule
def long_function(tree, limit=30):
    for fn in functions(tree):
        n = fn.end_lineno - fn.lineno + 1
        if n > limit:
            yield Finding("long_function", fn.lineno, 2, f"{fn.name} ({n} lines)")


@rule
def deep_nesting(tree, limit=3):
    def walk(node, depth):
        for child in ast.iter_child_nodes(node):
            if isinstance(child, FUNCS + (ast.Lambda,)):
                continue  # nested functions are checked on their own
            d = depth + isinstance(child, BLOCKS)
            if d == limit + 1 and isinstance(child, BLOCKS):
                yield Finding("deep_nesting", child.lineno, 2, f"{d} levels")
            yield from walk(child, d)

    for fn in functions(tree):
        yield from walk(fn, 0)


@rule
def too_many_params(tree, limit=5):
    for fn in functions(tree):
        a = fn.args
        names = [x.arg for x in a.posonlyargs + a.args + a.kwonlyargs
                 if x.arg not in ("self", "cls")]
        if len(names) > limit:
            yield Finding("too_many_params", fn.lineno, 1, f"{fn.name} takes {len(names)}")


@rule
def mutable_default(tree):
    for fn in functions(tree):
        for d in fn.args.defaults + [k for k in fn.args.kw_defaults if k]:
            if isinstance(d, (ast.List, ast.Dict, ast.Set)):
                yield Finding("mutable_default", d.lineno, 3, fn.name)


@rule
def bare_except(tree):
    for h in handlers(tree):
        if h.type is None:
            yield Finding("bare_except", h.lineno, 3)


@rule
def swallowed_error(tree):
    for h in handlers(tree):
        if len(h.body) == 1 and isinstance(h.body[0], ast.Pass):
            yield Finding("swallowed_error", h.lineno, 2)


@rule
def unused_variable(tree):
    for fn in functions(tree):
        loaded = {n.id for n in ast.walk(fn)
                  if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load)}
        seen = set()
        for n in ast.walk(fn):
            if isinstance(n, ast.Assign):
                for t in n.targets:
                    if (isinstance(t, ast.Name) and t.id not in loaded
                            and not t.id.startswith("_") and t.id not in seen):
                        seen.add(t.id)
                        yield Finding("unused_variable", n.lineno, 1, t.id)
