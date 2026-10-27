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


def test_post_forwards_json_headers_and_custom_timeout(api_client, monkeypatch):
    response = Mock()
    captured = {}
    payload = {"title": "Test", "body": "Example"}
    headers = {"Authorization": "Bearer test-token"}
    custom_timeout = (1.0, 2.0)

    def fake_request(method, url, **kwargs):
        captured.update(method=method, url=url, **kwargs)
        return response

    monkeypatch.setattr(api_client.session, "request", fake_request)

    result = api_client.post(
        "posts",
        json=payload,
        headers=headers,
        timeout=custom_timeout,
    )

    assert result is response
    assert captured == {
        "method": "POST",
        "url": "https://jsonplaceholder.typicode.com/posts",
        "json": payload,
        "headers": headers,
        "timeout": custom_timeout,
    }


@pytest.mark.parametrize(
    ("path", "expected_url"),
    [
        ("/posts", "https://jsonplaceholder.typicode.com/posts"),
        ("posts", "https://jsonplaceholder.typicode.com/posts"),
        ("///posts", "https://jsonplaceholder.typicode.com/posts"),
        ("", "https://jsonplaceholder.typicode.com/"),
    ],
)
def test_request_normalizes_path(api_client, monkeypatch, path, expected_url):
    captured = {}

    def fake_request(method, url, **kwargs):
        captured.update(method=method, url=url, **kwargs)
        return Mock()

    monkeypatch.setattr(api_client.session, "request", fake_request)

    api_client.request("GET", path)

    assert captured["url"] == expected_url


def test_request_uses_default_timeout_when_not_overridden(api_client, monkeypatch):
    captured = {}

    def fake_request(method, url, **kwargs):
        captured.update(kwargs)
        return Mock()

    monkeypatch.setattr(api_client.session, "request", fake_request)

    api_client.get("/posts")

    assert captured["timeout"] == api_client.timeout


def test_request_forwards_query_params_and_headers(api_client, monkeypatch):
    captured = {}
    params = {"userId": 2}
    headers = {"Accept": "application/json"}

    def fake_request(method, url, **kwargs):
        captured.update(method=method, url=url, **kwargs)
        return Mock()

    monkeypatch.setattr(api_client.session, "request", fake_request)

    api_client.get("/posts", params=params, headers=headers)

    assert captured["params"] == params
    assert captured["headers"] == headers
    assert captured["method"] == "GET"

@pytest.mark.parametrize("status_code", [400, 401, 404, 500])
def test_get_returns_http_error_responses(
    api_client,
    monkeypatch,
    status_code,
):
    response = Mock()
    response.status_code = status_code

    def fake_request(method, url, **kwargs):
        return response

    monkeypatch.setattr(api_client.session, "request", fake_request)

    result = api_client.get("/posts/1")

    assert result is response
    assert result.status_code == status_code
