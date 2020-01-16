from flask import Flask
import json
from TreePruningAPI.pruner import configure_routes

def test_localhost():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    response = client.get('/')
    print(response)

    assert response.json == {'msg': 'localhost works'}
    assert response.status_code == 200

def test_get_tree():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    response = client.get('/tree/input')

    # assert response.status_code == 200
