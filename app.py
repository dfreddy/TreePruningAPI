import json
from flask import Flask, jsonify, request, abort
import requests
from pruner import configure_routes

app = Flask(__name__)

configure_routes(app)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
