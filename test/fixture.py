# TODO: should learn how to use real fixtures in pytest
# for reference see https://github.com/rhsu/py2Do/issues/19
from flaskblog import app, db
from flaskblog.models import Task


def client():
    client = app.test_client()
    return client


def create_default_task():
    new_task = Task(
        title='test',
        content='some fake content',
        status_id=1
    )

    db.session.add(new_task)
    db.session.commit()
    return new_task
