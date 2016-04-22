python-typesafe
===============

.. figure:: https://codeship.com/projects/e1c62c40-eae3-0133-52bc-5e83b9717393/status?branch=master

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

Installation
------------

.. code-block:: bash

    $ pip install git+git://github.com/mirainc/python-typesafe.git@v0.1