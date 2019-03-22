from flask import jsonify, request
from app import app
from app.services.custom_field_service import CustomFieldService
from app.presenters.custom_field_presenter import CustomFieldPresenter


# TODO require that there is a query string of a TaskId
# @app.route('/custom_fields', methods=['GET'])
# def get_statuses():
#     statuses = StatusService().get()
#     response = StatusPresenter().convert_list(statuses)
#     return jsonify(response)


@app.route('/custom_fields', methods=['POST'])
def create_custom_field():
    request_json = request.json
    custom_field = CustomFieldService().post(
        request_json["title"],
        request_json["type"]
    )
    response = CustomFieldPresenter().convert(custom_field)
    return jsonify(response)


@app.route('/custom_fields/<int:custom_field_id>', methods=['GET'])
def get_custom_field(custom_field_id):
    custom_field = CustomFieldService().get_by_id(custom_field_id)
    response = CustomFieldPresenter().convert(custom_field)
    return jsonify(response)


@app.route('/custom_fields/<int:custom_field_id>', methods=['DELETE'])
def delete_custom_field(custom_field_id):
    response = CustomFieldService().delete(custom_field_id)
    if response["success"]:
        return jsonify(response)
    else:
        return jsonify(response), 422


@app.route('/custom_fields/<int:custom_field_id>', methods=['PUT'])
def update_custom_field(custom_field_id):
    request_json = request.json
    custom_field = CustomFieldService().put(
        custom_field_id, request_json['title']
    )
    response = CustomFieldPresenter().convert(custom_field)
    return jsonify(response)
