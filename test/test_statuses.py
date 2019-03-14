from app import db
from app.database_reset import database_reset
from app.models.status import Status
from fixture import client, create_default_task
import json


def test_get():
    database_reset()
    testapp = client()
    response = testapp.get('/statuses')
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


def test_get_by_id():
    database_reset()
    testapp = client()
    response = testapp.get("/statuses/1")
    assert response.status_code == 200
    assert response.get_json() == {
        "id": "1",
        "type": "status",
        "title": "Not Started",
    }


def test_get_by_id_when_deleted():
    database_reset()
    testapp = client()
    status = Status.query.first()
    status.is_deleted = True
    db.session.add(status)
    db.session.commit()
    response = testapp.get("/statuses/%s" % status.id)
    assert response.status_code == 422
    assert response.get_json() == {
        "errors": ["the status of id %s does not exist" % (status.id)]
    }


def test_get_by_id_when_bogus_id():
    database_reset()
    testapp = client()
    status_id = Status.query.first().id
    response = testapp.get("/statuses/%s" % (status_id+1000))
    assert response.status_code == 422
    assert response.get_json() == {
        "errors": ["the status of id %s does not exist" % (status_id+1000)]
    }


def test_post():
    database_reset()
    testapp = client()
    request_body = {"title": "some new status", "type": "status"}
    response = testapp.post('/statuses',
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


def test_delete():
    database_reset()
    testapp = client()
    some_status = Status.query.first()
    status_id = some_status.id
    response = testapp.delete('/statuses/%s' % (status_id))
    assert response.status_code == 200
    assert response.get_json() == {"success": True}
    found_status = Status.query.filter_by(id=status_id).first()
    assert found_status.is_deleted


def test_delete_but_referenced():
    database_reset()
    testapp = client()
    default_task = create_default_task()
    response = testapp.delete('/statuses/%s' % (default_task.status_id))
    assert response.status_code == 422
    assert response.get_json() == {
        "success": False,
        "errors": ["This status is being referenced"]
    }


def test_put():
    database_reset()
    status = Status.query.filter_by(id=1).first()
    request_body = {"title": "some updated status", "type": "status"}

    testapp = client()

    response = testapp.put('/statuses/%s' % (status.id),
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
