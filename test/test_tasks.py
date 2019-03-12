from fixture import client, create_default_task
from app.database_reset import database_reset
from app.models import Task
import json


def test_get():
    database_reset()
    task = create_default_task()

    testapp = client()

    expected_response = [{
        "id": task.id,
        "type": "task",
        "content": "some fake content",
        "title": "test",
        "status_id": 1,
        "meta": {
            "status": {
                "id": 1,
                "title": "Not Started"
            },
        },
    }]

    response = testapp.get('/tasks')

    assert response.status_code == 200
    assert response.get_json() == expected_response


def test_post():
    database_reset()
    testapp = client()

    request_body = {
        "content": "some fake content",
        "title": "test",
        "type": "task",
        "status_id": 1
    }

    response = testapp.post('/tasks',
                            data=json.dumps(request_body),
                            content_type='application/json')

    """
    finding newly created task
    """
    task = Task.query.filter_by(id=1).first()

    expected_response = {
            "id": task.id,
            "type": "task",
            "content": "some fake content",
            "title": "test",
            # TODO refactor this. shouldn't assert off of 1. should find that
            # something was created in the database first.
            # then assert this.
            "status_id": 1,
            "meta": {
                "status": {
                    "id": 1,
                    "title": "Not Started"
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
    response = testapp.delete('/tasks/%s' % (task_id))
    assert response.status_code == 200
    assert response.get_json() == {"success": True}
    found_task = Task.query.filter_by(id=task_id).first()
    assert found_task.is_deleted


def test_put():
    database_reset()
    task = create_default_task()

    testapp = client()

    request_body = {
        "content": "some new content",
        "title": "new title",
        "type": "task",
        # TODO: should test setting a new status
        "status_id": 1
    }

    expected_response = {
            'id': task.id,
            'type': 'task',
            'content': 'some new content',
            'title': 'new title',
            'status_id': 1,
            'meta': {
                'status': {
                    'id': 1,
                    'title': 'Not Started'
                },
            },
        }

    response = testapp.put('/tasks/%s' % (task.id),
                           data=json.dumps(request_body),
                           content_type='application/json')

    """
    testing that the response is correct
    """
    assert response.status_code == 200
    assert expected_response == response.get_json()

    """
    testing that the record was updated correctly in the database
    """
    found_task = Task.query.filter_by(id=task.id).first()
    assert found_task.content == 'some new content'
    assert found_task.title == 'new title'
    assert found_task.status_id == 1
