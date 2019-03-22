from app import app, db
from app.database_reset import database_reset
from app.models.custom_field import CustomField
from app.models.status import Status
from app.models.task import Task
import pytest


@pytest.fixture(autouse=True)
def run_around_tests():
    database_reset()
    yield


@pytest.fixture
def client():
    client = app.test_client()
    return client


@pytest.fixture
def default_task():
    new_task = Task(
        title="test",
        content="some fake content",
        status_id=1
    )

    db.session.add(new_task)
    db.session.commit()
    return new_task


@pytest.fixture
def default_status():
    session = db.session()
    return session.query(Status).first()


@pytest.fixture
def default_custom_field():
    custom_field = CustomField(
        title="test custom field",
        field_type=1,
    )

    session = db.session()
    session.add(custom_field)
    session.commit()
    return custom_field
