from fixture import client, create_default_task
from flaskblog.database_reset import DatabaseReset
from flaskblog.models import Task
import json


def test_get():
    DatabaseReset()
    create_default_task()

    testapp = client()

    expected_response = [{
        'content': 'some fake content',
        'title': 'test',
        'status_id': 1,
        'meta': {
            'status': {
                'id': 1,
                'title': 'Not Started'
            },
        },
    }]

    response = testapp.get('/tasks')

    assert response.status_code == 200
    assert response.get_json() == expected_response


def test_post():
    DatabaseReset()
    testapp = client()

    request_body = {
        "content": "some fake content",
        "title": "test",
        "status_id": 1
    }

    expected_response = {
            'content': 'some fake content',
            'title': 'test',
            'status_id': 1,
            'meta': {
                'status': {
                    'id': 1,
                    'title': 'Not Started'
                },
            },
        }

    response = testapp.post('/tasks',
                            data=json.dumps(request_body),
                            content_type='application/json')

    assert response.status_code == 200
    assert response.get_json() == expected_response


def test_delete():
    DatabaseReset()
    task = create_default_task()
    testapp = client()

    expected_response = {'success': True}
    response = testapp.delete('/tasks/%s' % (task.id))

    assert response.status_code == 200
    assert response.get_json() == expected_response

    found_task = Task.query.filter_by(id=task.id).first()
    assert found_task is None


def test_put():
    DatabaseReset()
    task = create_default_task()

    testapp = client()

    request_body = {
        "content": "some new content",
        "title": "new title",
        # TODO: should test setting a new status
        "status_id": 1
    }

    expected_response = {
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