from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/', methods=['GET'])
def test():
    return jsonify({'msg': 'localhost works'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
