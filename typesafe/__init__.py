# global types
class Any():
    pass


# decorators
from decorators import args, returns, types   # flake8: noqa


# flake8 type checkers
class TypeChecker(object):
    name = 'typesafety'
    version = 0.1
    _code = 'T0'
    _error_tmpl = 'T0 %r does not have a type declaration'
    
    def __init__(self, tree, filename):
        self.tree = tree
        
    def run(self):
        if False:
            text = self._error_tmpl % (None)
            yield 0, 0, text, type(self)