import pytest
import requests

from tests.helpers import (
    assert_json_content_type,
    assert_post_schema,
    parse_json_response,
)


pytestmark = pytest.mark.unit


def _response(body: bytes, *, status_code: int = 200) -> requests.Response:
    response = requests.Response()
    response.status_code = status_code
    response._content = body
    response.headers["Content-Type"] = "application/json; charset=utf-8"
    return response


@pytest.mark.parametrize(
    "content_type",
    [
        "application/json",
        "application/json; charset=utf-8",
        "Application/JSON",
        " application/json ; charset=UTF-8 ",
    ],
)
def test_json_content_type_accepts_json_media_type(content_type: str) -> None:
    assert_json_content_type(content_type)


@pytest.mark.parametrize(
    "content_type",
    [None, "", "text/plain", "application/problem+json", "application/jsonp"],
    ids=["missing", "empty", "plain-text", "problem-json", "json-prefix"],
)
def test_json_content_type_rejects_non_json_media_type(
    content_type: str | None,
) -> None:
    with pytest.raises(AssertionError, match="Content-Type"):
        assert_json_content_type(content_type)


@pytest.mark.parametrize(
    ("body", "status_code"),
    [
        (b"", 200),
        (b"   ", 200),
        (b"{not-json}", 200),
        (b"<html>upstream error</html>", 502),
    ],
    ids=["empty-body", "whitespace-body", "malformed-json", "html-error-page"],
)
def test_parse_json_response_reports_invalid_body_with_status(
    body: bytes,
    status_code: int,
) -> None:
    response = _response(body, status_code=status_code)

    with pytest.raises(
        AssertionError,
        match=rf"valid JSON, got HTTP {status_code}",
    ) as error:
        parse_json_response(response)

    assert isinstance(error.value.__cause__, requests.exceptions.JSONDecodeError)


def test_parse_json_response_returns_valid_json() -> None:
    response = _response(b'{"id": 7, "title": "example"}')

    assert parse_json_response(response) == {"id": 7, "title": "example"}


def test_post_schema_rejects_missing_required_field() -> None:
    with pytest.raises(AssertionError, match="missing required field 'body'"):
        assert_post_schema({"userId": 1, "id": 2, "title": "example"})


@pytest.mark.parametrize(
    ("field", "value", "expected_message"),
    [
        ("userId", True, "userId"),
        ("id", "2", "id"),
        ("title", None, "title"),
        ("body", 123, "body"),
    ],
)
def test_post_schema_rejects_wrong_primitive_types(
    field: str,
    value: object,
    expected_message: str,
) -> None:
    post: dict[str, object] = {
        "userId": 1,
        "id": 2,
        "title": "example",
        "body": "example body",
    }
    post[field] = value

    with pytest.raises(AssertionError, match=expected_message):
        assert_post_schema(post)
