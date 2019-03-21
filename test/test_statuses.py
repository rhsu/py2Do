from app import db
from app.models.status import Status
import json


def test_get(client):
    response = client.get("/statuses")
    assert response.status_code == 200
    assert response.get_json() == [
        {
            "id": "1",
            "type": "status",
            "title": "Not Started",
        },
        {
            "id": "2",
            "type": "status",
            "title": "In Progress",
        },
        {
            "id": "3",
            "type": "status",
            "title": "Done",
        },
    ]


def test_get_by_id(client):
    response = client.get("/statuses/1")
    assert response.status_code == 200
    assert response.get_json() == {
        "id": "1",
        "type": "status",
        "title": "Not Started",
    }


def test_get_by_id_when_deleted(client, default_status):
    default_status.is_deleted = True
    db.session.add(default_status)
    db.session.commit()
    response = client.get("/statuses/%s" % default_status.id)
    assert response.status_code == 422
    assert response.get_json() == {
        "errors": ["the status of id %s does not exist" % (default_status.id)]
    }


def test_get_by_id_when_bogus_id(client, default_status):
    status_id = default_status.id
    response = client.get("/statuses/%s" % (status_id+1000))
    assert response.status_code == 422
    assert response.get_json() == {
        "errors": ["the status of id %s does not exist" % (status_id+1000)]
    }


def test_post(client):
    request_body = {"title": "some new status", "type": "status"}
    response = client.post('/statuses',
                           data=json.dumps(request_body),
                           content_type='application/json')
    """
    find the status that was just created
    """
    json_response = response.get_json()
    new_id = json_response["id"]
    new_status = Status.query.filter_by(id=new_id).first()
    assert new_status.title == "some new status"
    assert response.status_code == 200
    assert response.get_json() == {
        "id": str(new_id),
        "type": "status",
        "title": "some new status"
    }


def test_delete(client, default_status):
    status_id = default_status.id
    response = client.delete('/statuses/%s' % (status_id))
    assert response.status_code == 200
    assert response.get_json() == {"success": True}
    found_status = Status.query.filter_by(id=status_id).first()
    assert found_status.is_deleted


def test_delete_but_referenced(client, default_task):
    response = client.delete('/statuses/%s' % (default_task.status_id))
    assert response.status_code == 422
    assert response.get_json() == {
        "success": False,
        "errors": ["This status is being referenced"]
    }


def test_put(client, default_status):
    request_body = {"title": "some updated status", "type": "status"}

    response = client.put('/statuses/%s' % (default_status.id),
                          data=json.dumps(request_body),
                          content_type='application/json')

    """
    testing that the response is correct
    """
    assert response.status_code == 200
    assert response.get_json() == {
        "id": "1",
        "type": "status",
        "title": "some updated status",
    }
