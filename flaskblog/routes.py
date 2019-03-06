from flask import jsonify, request
from flaskblog import app
from flaskblog.register_service import RegisterService
from flaskblog.services.tasks.task_service import TaskService
from flaskblog.services.statuses.status_service import StatusService


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
            'id': task.id,
            'type': 'task',
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
        'type': 'task',
        'id': task.id,
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
        'id': task.id,
        'type': 'task',
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


@app.route('/statuses', methods=['GET'])
def get_statuses():
    service = StatusService()
    statuses = service.get()
    response = map(
            lambda status: {
                'title': status.title,
                'id': status.id,
                'type': 'status',
            },
            statuses
        )
    return jsonify(response)


@app.route('/statuses', methods=['POST'])
def create_statuses():
    request_json = request.json
    service = StatusService()
    status = service.post(request_json['title'])
    response = {
        'id': status.id,
        'type': 'status',
        'title': status.title,
    }
    return jsonify(response)


@app.route('/statuses/<int:status_id>', methods=['DELETE'])
def delete_statuses(status_id):
    service = StatusService()
    service.delete(status_id)
    return jsonify({'success': True})


@app.route('/statuses/<int:status_id>', methods=['PUT'])
def update_statuses(status_id):
    request_json = request.json
    service = StatusService()
    status = service.put(status_id, request_json['title'])
    response = {
        'id': status.id,
        'type': 'status',
        'title': status.title,
    }
    return jsonify(response)
