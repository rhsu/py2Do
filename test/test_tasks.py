from app import db
from app.database_reset import database_reset
from app.models.status import Status
from app.models.task import Task
from fixture import client, create_default_task
import json


def test_get_by_id():
    database_reset()
    task = create_default_task()
    status_id = task.status_id
    testapp = client()

    response = testapp.get("/tasks/%s" % (task.id))

    assert response.status_code == 200
    assert response.get_json() == {
        "title": "test",
        "status_id": str(status_id),
        "content": "some fake content",
        "meta": {
            "status": {
                "id": str(status_id),
                "title": "Not Started",
            }
        },
        "type": "task",
        "id": str(task.id),
    }


def test_get_by_id_item_deleted():
    database_reset()
    testapp = client()
    task = create_default_task()
    task.is_deleted = True
    db.session.add(task)
    db.session.commit()
    response = testapp.get("/tasks/%s" % task.id)
    assert response.status_code == 422
    assert response.get_json() == {
        "errors": ["the task of id %s does not exist" % (task.id)]
    }


def test_get_by_id_when_bogus_id():
    database_reset()
    testapp = client()
    task = create_default_task()
    task_id = task.id
    response = testapp.get("/tasks/%s" % (task_id+1000))
    assert response.status_code == 422
    assert response.get_json() == {
        "errors": ["the task of id %s does not exist" % (task_id+1000)]
    }


def test_get():
    database_reset()
    task = create_default_task()
    status_id = task.status_id
    testapp = client()

    response = testapp.get("/tasks")

    assert response.status_code == 200
    assert response.get_json() == [
        {
            "id": str(task.id),
            "type": "task",
            "content": "some fake content",
            "title": "test",
            "status_id": str(status_id),
            "meta": {
                "status": {
                    "id": str(status_id),
                    "title": "Not Started",
                },
            },
        }
    ]


def test_post():
    database_reset()
    testapp = client()
    status_id = Status.query.first().id
    request_body = {
        "content": "some fake content",
        "title": "test",
        "type": "task",
        "status_id": str(status_id),
    }

    response = testapp.post('/tasks',
                            data=json.dumps(request_body),
                            content_type='application/json')

    """
    finding newly created task
    """
    task = Task.query.filter_by(id=status_id).first()

    assert response.status_code == 200
    assert response.get_json() == {
        "id": str(task.id),
        "type": "task",
        "content": "some fake content",
        "title": "test",
        "status_id": str(status_id),
        "meta": {
            "status": {
                "id": str(status_id),
                "title": "Not Started",
            },
        },
    }


def test_post_bad_status_id():
    database_reset()
    testapp = client()
    status_id = Status.query.first().id + 1000
    request_body = {
        "content": "some fake content",
        "title": "test",
        "type": "task",
        "status_id": str(status_id),
    }

    response = testapp.post('/tasks',
                            data=json.dumps(request_body),
                            content_type='application/json')

    assert response.status_code == 422
    assert response.get_json() == {
        "errors": ["status_id of %s is not valid" % status_id]
    }


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
        "status_id": str(status_id),
    }

    response = testapp.put("/tasks/%s" % (task.id),
                           data=json.dumps(request_body),
                           content_type="application/json")

    """
    testing that the response is correct
    """
    assert response.status_code == 200
    assert response.get_json() == {
        "id": str(task.id),
        "type": "task",
        "content": "some new content",
        "title": "new title",
        "status_id": str(status_id),
        "meta": {
            "status": {
                "id": str(status_id),
                "title": "Not Started",
            },
        },
    }

    """
    testing that the record was updated correctly in the database
    """
    found_task = Task.query.filter_by(id=task.id).first()
    assert found_task.content == "some new content"
    assert found_task.title == "new title"
    assert found_task.status_id == int(status_id)


def test_put_bad_status_id():
    database_reset()
    task = create_default_task()
    status_id = task.status_id + 1000
    testapp = client()

    request_body = {
        "content": "some new content",
        "title": "new title",
        "type": "task",
        "status_id": str(status_id),
    }

    response = testapp.put("/tasks/%s" % (task.id),
                           data=json.dumps(request_body),
                           content_type="application/json")

    assert response.status_code == 422
    assert response.get_json() == {
        "errors": ["status_id of %s is not valid" % status_id]
    }
