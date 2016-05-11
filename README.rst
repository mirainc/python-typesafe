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

.. code-block:: python

    # Types
    Any  # represents any type; ignored by checker
    Class  # represents any type; analogous to types.TypeType

    Optional  # optional type; allows for given type or None value
    opt(str)  # optional type alias with a type value of str

.. code-block:: python

    # Properties
    class TypesafeClass(object):
      def __init__(self):
        self._x = ''
        add_property(self, 'x', str)

    instance = TypesafeClass()
    instance.x  # >>> ''


flake8 Integration
------------------

.. code-block:: python

    def greet(x):
      return 'Hello ' + x

.. code-block:: bash

    $ flake8 greet.py
    greet.py:1:1: T000 function 'greet' does not have a type declaration

Installation
------------

.. code-block:: bash

    $ pip install git+git://github.com/mirainc/python-typesafe.git@v0.3

.. code-block:: bash

    # in requirements.txt
    -e git://github.com/mirainc/python-typesafe.git@v0.3#egg=typesafe
