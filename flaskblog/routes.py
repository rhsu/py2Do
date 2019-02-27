from flask import jsonify, request
from flaskblog import app
from flaskblog.register_service import RegisterService
from flaskblog.create_task_service import CreateTaskService


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


@app.route("/task", methods=['POST'])
def create_task():
    request_json = request.json
    service = CreateTaskService(
        title=request_json['title'],
        content=request_json['content']
    )

    service.perform()

    return jsonify(request.json)
