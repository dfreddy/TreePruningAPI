from flask import Flask
import json
from TreePruningAPI.pruner import configure_routes, pruneTree, aux_pruner
import pytest


@pytest.fixture
def client():
    app = Flask(__name__)
    configure_routes(app)
    return app.test_client()


def setup_mocker(mocker):
    get_mock = mocker.patch("requests.get")
    response_mock = get_mock.return_value
    response_mock.json.return_value = {}

    return response_mock


# API TESTING #
def test_localhost(client):
    response = client.get("/")

    assert response.json == {"msg": "localhost works"}
    assert response.status_code == 200


def test_get_tree(client, mocker):
    setup_mocker(mocker).status_code = 200

    response = client.get("/tree/input")

    assert response.status_code == 200


def test_failed_get_tree(client, mocker):
    setup_mocker(mocker).status_code = 404

    response = client.get("/tree/input")

    assert response.status_code == 404


# UNIT TESTING #
def test_pruning():
    input_tree = json.load(open("test_tree.txt"))
    expected_tree = json.load(open("test_pruned_tree.txt"))
    indicator_ids = ["1", "31", "32"]

    pruned_tree = aux_pruner(input_tree, indicator_ids, [], [], [])

    assert pruned_tree == expected_tree
