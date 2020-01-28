import json
from flask import Flask, jsonify, request, abort
import requests
import os

# requests tree from server
def getTree(name):
    server_url = (
        "https://kf6xwyykee.execute-api.us-east-1.amazonaws.com/production/tree/" + name
    )
    response = requests.get(server_url)
    count = 0

    while response.status_code != 200:
        if response.status_code == 404:
            abort(404)

        count += 1
        if count >= 4:
            abort(500)
        # print("500, new request")
        response = requests.get(server_url)

    data = response.json()

    """
    # testing json response
    if not os.path.isdir('output'):
        os.mkdir('output')
    output_file = open('output/output.txt', 'w+')
    json.dump(data, output_file, indent=4)
    output_file.close()
    """

    return data


# iterates over the original tree
# removes indicators that werent selected
# cleans out categories that have no indicators
# same for sub_themes and themes


def aux_pruner(tree, ids, st_list, cat_list, ind_list):
    new_tree = []

    for item in tree:
        if "sub_themes" in item:
            aux_pruner(item["sub_themes"], ids, st_list, [], [])
            item["sub_themes"] = st_list
            if item["sub_themes"] != []:
                new_tree.append(item)
            st_list = []

        elif "categories" in item:
            aux_pruner(item["categories"], ids, st_list, cat_list, [])
            item["categories"] = cat_list
            if item["categories"] != []:
                st_list.append(item)
            cat_list = []

        elif "indicators" in item:
            aux_pruner(item["indicators"], ids, st_list, cat_list, ind_list)
            item["indicators"] = ind_list
            if item["indicators"] != []:
                cat_list.append(item)
            ind_list = []

        elif str(item["id"]) in ids:
            ind_list.append(item)

    return new_tree


def pruneTree(tree, indicator_ids):
    return aux_pruner(tree, indicator_ids, [], [], [])


def configure_routes(app):
    @app.route("/tree/<string:name>", methods=["GET"])
    def pruner(name):
        indicator_ids = request.args.getlist("indicator_ids[]")

        tree = getTree(name)

        if indicator_ids != []:
            pruned_tree = pruneTree(tree, indicator_ids)
            return jsonify(pruned_tree)

        return jsonify(tree)

    # testing for localhost
    @app.route("/", methods=["GET"])
    def localhost():
        return jsonify({"msg": "localhost works"})
