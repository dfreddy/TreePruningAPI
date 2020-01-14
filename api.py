from flask import Flask, jsonify, request, abort
import requests
import json

app = Flask(__name__)

# requests tree from server
def getTree(name):
    server_url = 'https://kf6xwyykee.execute-api.us-east-1.amazonaws.com/production/tree/' + name
    response = requests.get(server_url)
    count = 0

    while response.status_code != 200:
        if response.status_code == 404:
            abort(404)

        count += 1
        if count >= 10:
            abort(500)

    data = response.json()

    # testing json response
    output_file = open("output.txt","w+")
    json.dump(data, output_file, indent=4)
    output_file.close()

    return data

# iterates over the original tree
# removes indicators that werent selected
# cleans out categories that have no indicators
# same for sub_themes and themes
def pruneTree(tree, indicator_ids):
    themes_list = []

    for a in tree:
        sub_themes_list = []

        for b in a['sub_themes']:
            categories_list = []

            for c in b['categories']:
                indicators_list = []

                for d in c['indicators']:
                    if str(d['id']) in indicator_ids:
                        indicators_list.append(d)

                # if category c has no indicators, removes it
                c['indicators'] = indicators_list
                if c['indicators'] != []:
                    categories_list.append(c)

            # if sub theme b has no categories, removes it
            b['categories'] = categories_list
            if b['categories'] != []:
                sub_themes_list.append(b)

        # if theme a has no sub themes, removes it
        a['sub_themes'] = sub_themes_list
        if a['sub_themes'] != []:
            themes_list.append(a)

    tree = themes_list

    # testing pruned output
    output_file = open("pruned_output.txt","w+")
    json.dump(tree, output_file, indent=4)
    output_file.close()

    return tree

@app.route('/tree/<string:name>', methods=['GET'])
def pruner(name):
    indicator_ids = request.args.getlist('indicator_ids[]')

    tree = getTree(name)

    if indicator_ids != []:
        pruned_tree = pruneTree(tree, indicator_ids)
        return jsonify(pruned_tree)

    return jsonify(tree)

''' testing for endpoint args
@app.route('/tree/<string:name>', methods=['GET'])
def testUrlArgs(name):
    indicator_ids = request.args.getlist('indicator_ids[]')
    return jsonify({'Tree name': name, 'Indicators': '{}'.format(indicator_ids)})
'''

@app.route('/', methods=['GET'])
def test():
    return jsonify({'msg': 'localhost works'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
