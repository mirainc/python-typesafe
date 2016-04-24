# imports
import unittest
from typesafe import args, types, returns, Any
from typesafe.errors import NotATypeError, InvalidTypeError, UnlabeledArgError


class TestDecorators(unittest.TestCase):
    # test @returns
    def test_returns_type(self):
        @returns(str)
        def test_str_return():
            return 'Hello World'
        
        self.assertEqual(test_str_return(), 'Hello World')
        
    def test_returns_any(self):
        @returns(Any)
        def test_any_return():
            return 'Hello World'
        
        self.assertEqual(test_any_return(), 'Hello World')

    def test_returns_invalid_type(self):
        @returns(str)
        def test_int_return():
            return 5
            
        with self.assertRaises(InvalidTypeError):
            _ = test_int_return()
        
    def test_return_non_type(self):
        with self.assertRaises(NotATypeError):
            @returns('str')
            def test_str_return():
                return 'Hello World'
                
    # test @args
    def test_types(self):
        @args(x=str)
        def test_str_arg(x):
            return x
            
        str_arg = 'Hello World'
        self.assertEqual(test_str_arg(str_arg), str_arg)
        
    def test_keyword_types(self):
        @args(x=str, y=int)
        def test_args(x, y=0):
            return [x for _ in range(y)]
                
        str_arg = 'A'
        int_arg = 2
        
        self.assertEqual(test_args(str_arg, y=int_arg), ['A', 'A'])
    
    def test_any_types(self):
        @args(x=str, y=Any)
        def test_args(x, y):
            return x + ' %s' % (y)
        
        self.assertEqual(test_args('Hello', 'World'), 'Hello World')
        
    def test_invalid_types(self):
        @args(x=str)
        def test_int_arg(x):
            return x
        
        int_arg = 5
        with self.assertRaises(InvalidTypeError):
            _ = test_int_arg(int_arg)
            
    def test_unlabled_types(self):
        with self.assertRaises(UnlabeledArgError) as context:
            @args(x=str)
            def test_args(x, y):
                return x + y
        
        self.assertTrue(str(context.exception).startswith('y'))
    
    def test_non_type(self):
        with self.assertRaises(NotATypeError):
            @args(x='str')
            def test_str_arg(x):
                return x
                
    # test @args and @returns
    def test_combination(self):
        @types(x=str, returns=str)
        def test_str_arg(x):
            return x
            
        str_arg = 'Hello World'
        self.assertEqual(test_str_arg(str_arg), str_arg)
    
    def test_types_and_returns(self):
        # @args decorator must be closest to function call
        @returns(str)
        @args(x=str)
        def test_str_arg(x):
            return x
            
        str_arg = 'Hello World'
        self.assertEqual(test_str_arg(str_arg), str_arg)
        
    # test as properties
    def test_as_property(self):
        class TypesafeClass(object):
            def __init__(self):
                self.__x = 'Hello World'
        
            @property
            @returns(str)
            def x(self):
                return self.__x
                
            @x.setter
            @args(new_val=str)
            def x(self, new_val):
                self.__x = new_val
    
        y = TypesafeClass()
        self.assertEqual(y.x, 'Hello World')
        
        y.x = 'Foo'
        self.assertEqual(y.x, 'Foo')
        
    # test as lambda
    def test_ignore_lambda(self):
        test_func = lambda x: x
        self.assertEqual(test_func('Hello World'), 'Hello World')
        