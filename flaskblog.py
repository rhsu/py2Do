from flask import Flask, jsonify, request
from register_service import RegisterService

app = Flask(__name__)


@app.route("/")
def dontmatter():
    return "hello world"


@app.route("/test")
def test():
    response = {
        "foo": "bar",
        "baz": "bill"
    }
    return jsonify(response)


@app.route("/something", methods=['POST'])
def something():
    return jsonify(request.json)


@app.route("/register", methods=['POST'])
def register():
    #
    # TBD import ipdb; ipdb.set_trace()
    #
    # import ipdb; ipdb.set_trace()

    request_json = request.json
    
    username = request_json['username']
    password = request_json['password']

    service = RegisterService(username, password)
    service.perform

    return jsonify(request.json)


if __name__ == '__main__':
    app.run(debug=True)
