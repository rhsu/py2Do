# TODO: should learn how to use real fixtures in pytest
# for reference see https://github.com/rhsu/py2Do/issues/19
from flaskblog import app


def client():
    client = app.test_client()
    return client
