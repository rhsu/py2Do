from flask import jsonify, request
from app import app
from app.register_service import RegisterService
from app.services.tasks.task_service import TaskService
from app.services.statuses.status_service import StatusService
from app.presenters.tasks.task_presenter import TaskPresenter
from app.presenters.statuses.status_presenter import StatusPresenter


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
    tasks = TaskService().get()
    response = TaskPresenter().convert_list(tasks)
    return jsonify(response)


@app.route('/tasks', methods=['POST'])
def create_task():
    request_json = request.json
    task = TaskService().post(
        request_json['title'],
        request_json['content'],
        request_json['status_id']
    )

    response = TaskPresenter().convert(task)
    return jsonify(response)


@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    TaskService().delete(task_id)
    return jsonify({'success': True})


@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    request_json = request.json
    task = TaskService().put(
        task_id,
        request_json['title'],
        request_json['content'],
        request_json['status_id']
    )
    response = TaskPresenter().convert(task)
    return jsonify(response)


@app.route('/statuses', methods=['GET'])
def get_statuses():
    statuses = StatusService().get()
    response = StatusPresenter().convert_list(statuses)
    return jsonify(response)


@app.route('/statuses', methods=['POST'])
def create_statuses():
    request_json = request.json
    status = StatusService().post(request_json['title'])
    response = StatusPresenter().convert(status)
    return jsonify(response)


@app.route('/statuses/<int:status_id>', methods=['DELETE'])
def delete_statuses(status_id):
    service = StatusService()
    service.delete(status_id)
    return jsonify({'success': True})


@app.route('/statuses/<int:status_id>', methods=['PUT'])
def update_statuses(status_id):
    request_json = request.json
    status = StatusService().put(status_id, request_json['title'])
    response = StatusPresenter().convert(status)
    return jsonify(response)
