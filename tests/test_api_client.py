from unittest.mock import Mock

import pytest


pytestmark = pytest.mark.unit


def test_get_forwards_url_parameters_and_finite_timeout(api_client, monkeypatch):
    response = Mock()
    captured = {}

    def fake_request(method, url, **kwargs):
        captured.update(method=method, url=url, **kwargs)
        return response

    monkeypatch.setattr(api_client.session, "request", fake_request)

    result = api_client.get("/posts", params={"userId": 1})

    assert result is response
    assert captured == {
        "method": "GET",
        "url": "https://jsonplaceholder.typicode.com/posts",
        "params": {"userId": 1},
        "timeout": api_client.timeout,
    }
