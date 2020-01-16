#!/bin/bash

source venv/bin/activate

pipenv install

python3 app.py

deactivate
