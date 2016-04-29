# imports
import unittest
from typesafe import add_property


class TestProperties(unittest.TestCase):
    # test add_property
    def test_add_property(self):
        class TypesafeClass(object):
            def __init__(self):
                self._x = 'Hello World'
                add_property(self, 'x', str)
        
        y = TypesafeClass()
        self.assertEqual(y.x, 'Hello World')
        
        y.x = 'Foo'
        self.assertEqual(y.x, 'Foo')
