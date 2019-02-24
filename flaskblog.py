from flask import Flask, jsonify


app = Flask(__name__)


@app.route("/")
def hello():
	return "hello world"


@app.route("/test")
def test():
	response = { "foo" : "bar", "baz": "bill" }
	return jsonify(response)


if __name__ == '__main__':
	app.run(debug=True)