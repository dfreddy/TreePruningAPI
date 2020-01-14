from flask import Flask, jsonify, request, abort
import requests
import json

app = Flask(__name__)

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

    ''' testing json response
    output_file = open("output.txt","w+")
    json.dump(data, output_file)
    output_file.close()
    '''

    return data

def pruneTree(tree, indicator_ids):
    return 0

@app.route('/tree/<string:name>', methods=['GET'])
def pruner(name):
    indicator_ids = request.args.getlist('indicator_ids[]')

    tree = getTree(name)

    pruned_tree = pruneTree(tree, indicator_ids)

    return jsonify(tree)

'''
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
