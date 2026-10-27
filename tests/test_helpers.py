import pytest

from tests.helpers import assert_json_content_type, assert_post_schema


pytestmark = pytest.mark.unit


@pytest.mark.parametrize(
    "content_type",
    [
        "application/json",
        "application/json; charset=utf-8",
        " Application/JSON ; charset=UTF-8 ",
    ],
)
def test_assert_json_content_type_accepts_json_media_type(content_type):
    assert_json_content_type(content_type)


@pytest.mark.parametrize(
    "content_type",
    [
        None,
        "",
        "text/plain",
        "application/problem+json",
        "application/jsonp",
    ],
    ids=["missing", "empty", "plain-text", "problem-json", "jsonp"],
)
def test_assert_json_content_type_rejects_non_json_media_type(content_type):
    with pytest.raises(AssertionError):
        assert_json_content_type(content_type)


def test_assert_post_schema_accepts_valid_post():
    assert_post_schema(
        {
            "userId": 1,
            "id": 10,
            "title": "Example title",
            "body": "Example body",
        }
    )


@pytest.mark.parametrize("post", [None, [], "not an object", 42])
def test_assert_post_schema_rejects_non_object(post):
    with pytest.raises(AssertionError, match="JSON object"):
        assert_post_schema(post)


@pytest.mark.parametrize("missing_field", ["userId", "id", "title", "body"])
def test_assert_post_schema_rejects_missing_required_field(missing_field):
    post = {
        "userId": 1,
        "id": 10,
        "title": "Example title",
        "body": "Example body",
    }
    del post[missing_field]

    with pytest.raises(AssertionError, match="missing required field"):
        assert_post_schema(post)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("userId", True),
        ("userId", "1"),
        ("id", False),
        ("id", "10"),
        ("title", 123),
        ("body", None),
    ],
)
def test_assert_post_schema_rejects_invalid_field_types(field, value):
    post = {
        "userId": 1,
        "id": 10,
        "title": "Example title",
        "body": "Example body",
    }
    post[field] = value

    with pytest.raises(AssertionError):
        assert_post_schema(post)
