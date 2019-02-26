from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow
    )
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


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
    db.session.commit()
    return jsonify(request.json)


if __name__ == '__main__':
    app.run(debug=True)
