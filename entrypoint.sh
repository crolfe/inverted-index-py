#!/bin/bash

set -e

# This is needed for pytest
/venv/bin/pip install -e .

cd inverted_index

/venv/bin/python index.py corpus.txt stoplist.txt

/venv/bin/python ./api/app.py
