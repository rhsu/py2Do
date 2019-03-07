from fixture import client
from app.database_reset import database_reset
from app.models import Status
import json


def test_get():
    database_reset()
    testapp = client()
    expected_response = [
        {
            "id": 1,
            "type": "status",
            "title": "Not Started",
        },
        {
            "id": 2,
            "type": "status",
            "title": "In Progress",
        },
        {
            "id": 3,
            "type": "status",
            "title": "Done",
        },
    ]
    response = testapp.get('/statuses')
    assert response.status_code == 200
    assert response.get_json() == expected_response


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
        "id": new_id,
        "type": "status",
        "title": "some new status"
    }


def test_delete():
    database_reset()
    testapp = client()
    expected_response = {'success': True}
    response = testapp.delete('/statuses/%s' % (1))

    assert response.status_code == 200
    assert response.get_json() == expected_response

    found_status = Status.query.filter_by(id=1).first()
    assert found_status is None


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
        "id": 1,
        "type": "status",
        "title": "some updated status",
    }
