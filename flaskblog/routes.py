from flask import jsonify, request
from flaskblog import app
from flaskblog.register_service import RegisterService
from flaskblog.create_task_service import CreateTaskService
from flaskblog.delete_task_service import DeleteTaskService


@app.route("/fake", methods=['GET'])
def fake():
    ret_val = {
        "foo": "bar"
    }
    return jsonify(ret_val)


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
        content=request_json['content'],
        status_id=request_json['status_id']
    )
    new_task = service.perform()
    status = new_task.status

    response = {
        'title': new_task.title,
        'content': new_task.content,
        'status_id': new_task.status_id,
        'meta': {
            'status': {
                'id': status.id,
                'title': status.title
            }
        }
    }
    return jsonify(response)


@app.route("/task/<int:task_id>", methods=['DELETE'])
def delete_task(task_id):
    service = DeleteTaskService(
        task_id=task_id
    )
    service.perform()
    return jsonify({'success': True})
