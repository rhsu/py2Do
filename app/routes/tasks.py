from flask import jsonify, request
from app import app
from app.services.tasks.task_service import TaskService
from app.presenters.tasks.task_presenter import TaskPresenter


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
    response = TaskService().delete(task_id)
    return jsonify(response)


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
