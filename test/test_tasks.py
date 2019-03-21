from app import db
from app.models.status import Status
from app.models.task import Task
import json


def test_get_by_id(client, default_task):
    status_id = default_task.status_id
    response = client.get("/tasks/%s" % (default_task.id))

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
        "id": str(default_task.id),
    }


def test_get_by_id_item_deleted(client, default_task):
    default_task.is_deleted = True
    db.session.add(default_task)
    db.session.commit()
    response = client.get("/tasks/%s" % default_task.id)
    assert response.status_code == 422
    assert response.get_json() == {
        "errors": ["the task of id %s does not exist" % (default_task.id)]
    }


def test_get_by_id_when_bogus_id(client, default_task):
    task_id = default_task.id
    response = client.get("/tasks/%s" % (task_id+1000))
    assert response.status_code == 422
    assert response.get_json() == {
        "errors": ["the task of id %s does not exist" % (task_id+1000)]
    }


def test_get(client, default_task):
    status_id = default_task.status_id
    response = client.get("/tasks")

    assert response.status_code == 200
    assert response.get_json() == [
        {
            "id": str(default_task.id),
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


def test_post(client):
    status_id = Status.query.first().id
    request_body = {
        "content": "some fake content",
        "title": "test",
        "type": "task",
        "status_id": str(status_id),
    }

    response = client.post('/tasks',
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


def test_post_bad_status_id(client):
    status_id = Status.query.first().id + 1000
    request_body = {
        "content": "some fake content",
        "title": "test",
        "type": "task",
        "status_id": str(status_id),
    }

    response = client.post('/tasks',
                           data=json.dumps(request_body),
                           content_type='application/json')

    assert response.status_code == 422
    assert response.get_json() == {
        "errors": ["status_id of %s is not valid" % status_id]
    }


def test_delete(client, default_task):
    task_id = default_task.id
    response = client.delete("/tasks/%s" % (task_id))
    assert response.status_code == 200
    assert response.get_json() == {"success": True}
    found_task = Task.query.filter_by(id=task_id).first()
    assert found_task.is_deleted


def test_put(client, default_task):
    status_id = default_task.status_id

    request_body = {
        "content": "some new content",
        "title": "new title",
        "type": "task",
        "status_id": str(status_id),
    }

    response = client.put("/tasks/%s" % (default_task.id),
                          data=json.dumps(request_body),
                          content_type="application/json")

    """
    testing that the response is correct
    """
    assert response.status_code == 200
    assert response.get_json() == {
        "id": str(default_task.id),
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
    found_task = Task.query.filter_by(id=default_task.id).first()
    assert found_task.content == "some new content"
    assert found_task.title == "new title"
    assert found_task.status_id == int(status_id)


def test_put_bad_status_id(client, default_task):
    status_id = default_task.status_id + 1000

    request_body = {
        "content": "some new content",
        "title": "new title",
        "type": "task",
        "status_id": str(status_id),
    }

    response = client.put("/tasks/%s" % (default_task.id),
                          data=json.dumps(request_body),
                          content_type="application/json")

    assert response.status_code == 422
    assert response.get_json() == {
        "errors": ["status_id of %s is not valid" % status_id]
    }
