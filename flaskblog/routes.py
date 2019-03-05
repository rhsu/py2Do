from flask import jsonify, request
from flaskblog import app
from flaskblog.register_service import RegisterService
from flaskblog.services.tasks.task_service import TaskService


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


@app.route('/tasks', methods=['GET'])
def get_tasks():
    service = TaskService()
    tasks = service.get()
    response = []

    for task in tasks:
        status = task.status
        response.append({
            'title': task.title,
            'content': task.content,
            'status_id': task.status_id,
            'meta': {
                'status': {
                    'id': status.id,
                    'title': status.title
                }
            }
        })
    return jsonify(response)


@app.route('/tasks', methods=['POST'])
def create_task():
    request_json = request.json
    service = TaskService()

    task = service.post(
        request_json['title'],
        request_json['content'],
        request_json['status_id']
    )

    status = task.status

    response = {
        'title': task.title,
        'content': task.content,
        'status_id': task.status_id,
        'meta': {
            'status': {
                'id': status.id,
                'title': status.title
            }
        }
    }
    return jsonify(response)


@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    service = TaskService()
    service.delete(task_id)
    return jsonify({'success': True})


@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    request_json = request.json
    service = TaskService()
    task = service.put(
        task_id,
        request_json['title'],
        request_json['content'],
        request_json['status_id']
    )
    status = task.status

    response = {
        'title': task.title,
        'content': task.content,
        'status_id': task.status_id,
        'meta': {
            'status': {
                'id': status.id,
                'title': status.title
            }
        }
    }
    return jsonify(response)
