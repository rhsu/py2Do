from app.models.custom_field import CustomField
import json


def test_get_by_id(client, default_custom_field):
    response = client.get("/custom_fields/%s" % (default_custom_field.id))
    assert response.status_code == 200
    assert response.get_json() == {
        "field_type": "TEXT",
        "type": "custom-field",
        "id": 1,
        "title": "test custom field",
    }

# TODO test get_by_id_when_deleted
# TODO test_get_by_id_when_bogus_id


def test_post(client):
    request_body = {
        "title": "some new custom field",
        "type": "text",
    }

    response = client.post("/custom_fields",
                           data=json.dumps(request_body),
                           content_type='application/json')

    json_response = response.get_json()
    new_id = json_response["id"]
    new_custom_field = CustomField.query.filter_by(id=new_id).first()

    assert response.status_code == 200
    assert response.get_json() == {
        "field_type": "TEXT",
        "type": "custom-field",
        "id": new_custom_field.id,
        "title": "some new custom field",
    }


def test_delete(client, default_custom_field):
    custom_field_id = default_custom_field.id
    response = client.delete("/custom_fields/%s" % (custom_field_id))
    assert response.status_code == 200
    assert response.get_json() == {"success": True}
    found_custom_field = CustomField.query.filter_by(
        id=custom_field_id).first()
    assert found_custom_field.is_deleted


def test_put(client, default_custom_field):
    request_body = {"title": "some updated custom field"}

    response = client.put("/custom_fields/%s" % (default_custom_field.id),
                          data=json.dumps(request_body),
                          content_type='application/json')

    assert response.status_code == 200
    assert response.get_json() == {
        "field_type": "TEXT",
        "type": "custom-field",
        "id": default_custom_field.id,
        "title": "some updated custom field",
    }
