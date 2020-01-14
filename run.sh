#!/bin/bash

pip install requests
pip install flask

source venv/bin/activate

python3 api.py

deactivate
