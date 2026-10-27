from typing import Any

import requests


def assert_json_content_type(content_type: str | None) -> None:
    assert content_type is not None, (
        "Expected response to include a Content-Type header."
    )

    media_type = content_type.partition(";")[0].strip().lower()
    assert media_type == "application/json", (
        f"Expected Content-Type to be application/json, got {content_type!r}."
    )


def parse_json_response(response: requests.Response) -> Any:
    try:
        return response.json()
    except requests.exceptions.JSONDecodeError as error:
        raise AssertionError(
            "Expected response body to contain valid JSON, "
            f"got HTTP {response.status_code}."
        ) from error


def assert_post_schema(post: object) -> None:
    assert isinstance(post, dict), "Expected a post to be a JSON object."

    required_fields = ("userId", "id", "title", "body")
    for field in required_fields:
        assert field in post, f"Post is missing required field {field!r}."

    assert type(post["userId"]) is int, "Post field 'userId' must be an integer."
    assert type(post["id"]) is int, "Post field 'id' must be an integer."
    assert type(post["title"]) is str, "Post field 'title' must be a string."
    assert type(post["body"]) is str, "Post field 'body' must be a string."
