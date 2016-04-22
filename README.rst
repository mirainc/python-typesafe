python-typesafe
===============

Runtime type-checking for Python 2.7. Add decorators to your functions
and properties to support runtime type safety of arguments and return
types.

Usage
-----

.. code-block:: python

    @types(x=str, returns=str)
    def greet(x):
      return 'Hello ' + x

    greet('user!')  # >>> Hello user!
    greet(42)  # >>> x (42) is not type <type 'str'>
