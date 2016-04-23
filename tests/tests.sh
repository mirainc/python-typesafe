#!/bin/bash

source .venv/bin/activate
pip install -r requirements.txt

coverage run --include=typesafe/* -m unittest discover tests
coverage html

flake8 typesafe/