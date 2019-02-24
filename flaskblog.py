from flask import Flask, jsonify


app = Flask(__name__)


@app.route("/")
def hello():
	return "hello world"


@app.route("/test")
def test():
	response = { "foo" : "bar" }
	return jsonify(response)