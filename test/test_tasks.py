from fixture import client, create_default_task
from app.database_reset import database_reset
from app.models import Task, Status
import json


def test_get():
    database_reset()
    task = create_default_task()
    status_id = task.status_id

    testapp = client()

    expected_response = [{
        "id": task.id,
        "type": "task",
        "content": "some fake content",
        "title": "test",
        "status_id": status_id,
        "meta": {
            "status": {
                "id": status_id,
                "title": "Not Started",
            },
        },
    }]

    response = testapp.get("/tasks")

    assert response.status_code == 200
    assert response.get_json() == expected_response


def test_post():
    database_reset()
    testapp = client()
    status_id = Status.query.first().id
    request_body = {
        "content": "some fake content",
        "title": "test",
        "type": "task",
        "status_id": status_id,
    }

    response = testapp.post('/tasks',
                            data=json.dumps(request_body),
                            content_type='application/json')

    """
    finding newly created task
    """
    task = Task.query.filter_by(id=status_id).first()

    expected_response = {
            "id": task.id,
            "type": "task",
            "content": "some fake content",
            "title": "test",
            "status_id": status_id,
            "meta": {
                "status": {
                    "id": status_id,
                    "title": "Not Started",
                },
            },
        }

    assert response.status_code == 200
    assert response.get_json() == expected_response


def test_delete():
    database_reset()
    task = create_default_task()
    task_id = task.id
    testapp = client()
    response = testapp.delete("/tasks/%s" % (task_id))
    assert response.status_code == 200
    assert response.get_json() == {"success": True}
    found_task = Task.query.filter_by(id=task_id).first()
    assert found_task.is_deleted


def test_put():
    database_reset()
    task = create_default_task()
    status_id = task.status_id
    testapp = client()

    request_body = {
        "content": "some new content",
        "title": "new title",
        "type": "task",
        # TODO: what if status doesn't exist?
        "status_id": status_id,
    }

    expected_response = {
            "id": task.id,
            "type": "task",
            "content": "some new content",
            "title": "new title",
            "status_id": status_id,
            "meta": {
                "status": {
                    "id": status_id,
                    "title": "Not Started",
                },
            },
        }

    response = testapp.put("/tasks/%s" % (task.id),
                           data=json.dumps(request_body),
                           content_type="application/json")

    """
    testing that the response is correct
    """
    assert response.status_code == 200
    assert expected_response == response.get_json()

    """
    testing that the record was updated correctly in the database
    """
    found_task = Task.query.filter_by(id=task.id).first()
    assert found_task.content == "some new content"
    assert found_task.title == "new title"
    assert found_task.status_id == status_id
