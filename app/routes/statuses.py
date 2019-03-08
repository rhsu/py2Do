from flask import jsonify, request
from app import app
from app.services.statuses.status_service import StatusService
from app.presenters.statuses.status_presenter import StatusPresenter


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
    response = StatusService().delete(status_id)
    return jsonify(response)


@app.route('/statuses/<int:status_id>', methods=['PUT'])
def update_statuses(status_id):
    request_json = request.json
    status = StatusService().put(status_id, request_json['title'])
    response = StatusPresenter().convert(status)
    return jsonify(response)