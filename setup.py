from setuptools import setup, find_packages

setup(
    name='typesafe',
    version='0.1',
    license='MIT',
    
    url='https://github.com/mirainc/python-typesafe',
    author='Patrick Perini',
    author_email='patrick@atomic.vc',
    
    packages=find_packages(exclude=['tests']),
    entry_points={
        'flake8.extension': ['T0 = typesafe.TypeChecker'],
    }
)