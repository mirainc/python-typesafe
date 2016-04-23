#!/bin/bash

source .venv/bin/activate
pip install -r requirements.txt

coverage run --include=typesafe/* -m unittest tests.test_decorators.TestDecorators
coverage html

flake8 typesafe/