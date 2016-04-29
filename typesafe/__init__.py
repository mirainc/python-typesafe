# global types
class Any():
    pass
    
class Class():
    pass
    
class Optional():
    def __init__(self, wrapped_type):
        self._wrapped_type = wrapped_type
opt = Optional

from types import NoneType


# decorators
from decorators import args, returns, types   # flake8: noqa
from properties import add_property  # flake8: noqa


# flake8 type checkers
class TypeChecker(object):
    name = 'typesafety'
    version = 0.1
    _code = 'T0'
    _error_tmpl = "T000 function %r does not have a type declaration"

    def __init__(self, tree, filename):
        self.tree = tree

    def run(self):
        import ast
        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef):
                text = self._error_tmpl % (node.name)

                if not node.decorator_list:
                    yield node.lineno, 0, text, type(self)
                    continue
                
                decorator_ids = [d.func.id for d in node.decorator_list if hasattr(d, 'func')]
                if 'types' in decorator_ids:
                    continue

                if 'returns' not in decorator_ids:
                    yield node.lineno, 0, text, type(self)
                    continue

                has_args = (
                    bool(node.args.args) or
                    bool(node.args.vararg) or
                    bool(node.args.kwarg)
                )

                if has_args and 'args' not in decorator_ids:
                    yield node.lineno, 0, text, type(self)
                    continue
