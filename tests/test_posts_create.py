import pytest

from tests.helpers import (
    assert_json_content_type,
    assert_post_schema,
    parse_json_response,
)


pytestmark = pytest.mark.integration


def test_create_post(api_client):
    post_data = {
        "userId": 1,
        "title": "QA Automation API test post",
        "body": "A test post created by the API Testing Framework.",
    }

    response = api_client.post("/posts", json=post_data)

    assert response.status_code == 201, (
        f"Expected POST /posts to return HTTP 201, got {response.status_code}."
    )

    assert_json_content_type(response.headers.get("Content-Type"))
    created_post = parse_json_response(response)
    assert_post_schema(created_post)
    assert created_post["userId"] == post_data["userId"], (
        "Expected the response userId to match the submitted userId."
    )
    assert created_post["title"] == post_data["title"], (
        "Expected the response title to match the submitted title."
    )
    assert created_post["body"] == post_data["body"], (
        "Expected the response body to match the submitted body."
    )
