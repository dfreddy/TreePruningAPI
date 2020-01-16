from flask import Flask
import json
from TreePruningAPI.pruner import configure_routes, pruneTree

# API TESTING #
def test_localhost():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    response = client.get('/')

    assert response.json == {'msg': 'localhost works'}
    assert response.status_code == 200

def test_get_tree():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    response = client.get('/tree/input')

    assert response.status_code in [200, 500]

def test_failed_get_tree():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    response = client.get('/tree/i')

    assert response.status_code in [404, 500]

# UNIT TESTING #
def test_pruning():
    input_tree = json.load(open('test_tree.txt'))
    expected_tree = json.load(open('test_pruned_tree.txt'))
    indicator_ids = ['1', '31', '32']

    pruned_tree = pruneTree(input_tree, indicator_ids)

    assert pruned_tree == expected_tree
