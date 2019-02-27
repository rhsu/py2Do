from flaskblog import app, db
from flaskblog.models import User
from flask import jsonify, request


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
    # TODO: make this work later. Need to learn more flask
    # username = request_json['username']
    # password = request_json['password']
    # email = request_json['email']
    # service = RegisterService(username, password, email)
    # service.perform()

    request_json = request.json

    new_user = User(
        username=request_json['username'],
        password=request_json['password'],
        email=request_json['email']
    )

    db.session.add(new_user)

    try:
        db.session.commit()
    except Exception as e:
        error = {
            "error": str(e)
        }
        return jsonify(error)

    return jsonify(request.json)
