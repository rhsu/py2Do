from app import app
from app.presenters.status_presenter import StatusPresenter
from app.services.status_service import StatusService
from flask import jsonify, request


@app.route('/statuses', methods=['GET'])
def get_statuses():
    statuses = StatusService().get_list()
    response = StatusPresenter().convert_list(statuses)
    return jsonify(response)


@app.route('/statuses/<int:status_id>', methods=['GET'])
def get_status(status_id):
    status = StatusService().get(status_id)
    if status is None:
        return jsonify({
            "errors": ["the status of id %s does not exist" % (status_id)]
        }), 422

    response = StatusPresenter().convert(status)
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
    if response["success"]:
        return jsonify(response)
    else:
        return jsonify(response), 422


@app.route('/statuses/<int:status_id>', methods=['PUT'])
def update_statuses(status_id):
    request_json = request.json
    status = StatusService().put(status_id, request_json['title'])
    response = StatusPresenter().convert(status)
    return jsonify(response)
