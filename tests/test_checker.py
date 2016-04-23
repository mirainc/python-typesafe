# imports
import ast
import unittest
import textwrap
from typesafe import TypeChecker


class TestCheck(unittest.TestCase):
    # test @types
    def test_types(self):
        code = textwrap.dedent("""
            @types(returns=str)
            def test():
                return 'Hello'
        """)
        
        tree = ast.parse(code)
        checker = TypeChecker(tree, __file__)
        
        results = [err for err in checker.run()]
        self.assertEquals(results, [])
        
    def test_property(self):
        code = textwrap.dedent("""
            class TestClass(object):
                @types()
                def __init__(self):
                    self.__test = 5
                
                @property
                @types(returns=int)
                def test(self):
                    return self.__test
                    
                @test.setter
                @types(new_val=int)
                def test(self, new_val):
                    self.__test = new_val
        """)
        
        tree = ast.parse(code)
        checker = TypeChecker(tree, __file__)
        
        results = [err for err in checker.run()]
        self.assertEquals(results, [])
        
    def test_failure(self):
        code = textwrap.dedent("""
            def test():
                return 'Hello'
        """)
        
        tree = ast.parse(code)
        checker = TypeChecker(tree, __file__)
        
        bad_lineno = 2
        results = [err for err in checker.run()]
        self.assertEquals(results[0][0], bad_lineno)
        
    # test @returns
    def test_returns(self):
        code = textwrap.dedent("""
            @returns(str)
            def test():
                return 'Hello'
        """)
        
        tree = ast.parse(code)
        checker = TypeChecker(tree, __file__)
        
        results = [err for err in checker.run()]
        self.assertEquals(results, [])
        
    def test_returns_failure(self):
        code = textwrap.dedent("""
            @other_decorator
            def test():
                return 'Hello'
        """)
        
        tree = ast.parse(code)
        checker = TypeChecker(tree, __file__)
        
        bad_lineno = 2
        results = [err for err in checker.run()]
        self.assertEquals(results[0][0], bad_lineno)
    
    # test @args
    def test_args(self):
        code = textwrap.dedent("""
            @returns(str)
            @args(x=str)
            def test(x):
                return 'Hello, ' + x
        """)
        
        tree = ast.parse(code)
        checker = TypeChecker(tree, __file__)
        
        results = [err for err in checker.run()]
        self.assertEquals(results, [])
        
    def test_args_failure(self):
        code = textwrap.dedent("""
            @returns(str)
            def test(x):
                return 'Hello, ' + x
        """)
        
        tree = ast.parse(code)
        checker = TypeChecker(tree, __file__)
        
        bad_lineno = 2
        results = [err for err in checker.run()]
        self.assertEquals(results[0][0], bad_lineno)
