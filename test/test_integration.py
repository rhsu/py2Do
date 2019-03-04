from fixture import client
import json


def test_fake():
    testapp = client()
    response = testapp.get('/fake')
    expected_data = {
        "foo": "bar"
    }
    assert response.status_code == 200
    assert json.loads(response.data) == expected_data
