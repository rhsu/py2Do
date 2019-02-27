from flask import jsonify, request
from flaskblog import app
from flaskblog.register_service import RegisterService


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
    request_json = request.json
    service = RegisterService(
        username=request_json['username'],
        password=request_json['password'],
        email=request_json['email']
    )

    try:
        service.perform()
    except Exception as e:
        error = {
            "error": str(e)
        }
        return jsonify(error)

    return jsonify(request.json)
