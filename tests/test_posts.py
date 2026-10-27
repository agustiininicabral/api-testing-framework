import pytest

from tests.helpers import (
    assert_json_content_type,
    assert_post_schema,
    parse_json_response,
)


pytestmark = pytest.mark.integration


def test_get_all_posts(api_client):
    response = api_client.get("/posts")

    assert response.status_code == 200, (
        f"Expected GET /posts to return HTTP 200, got {response.status_code}."
    )

    assert_json_content_type(response.headers.get("Content-Type"))
    posts = parse_json_response(response)
    assert isinstance(posts, list), "Expected GET /posts to return a JSON list."
    assert posts, "Expected GET /posts to return a non-empty list."

    for post in posts:
        assert_post_schema(post)

    post_ids = [post["id"] for post in posts]
    assert len(post_ids) == len(set(post_ids)), "Expected post IDs to be unique."


@pytest.mark.parametrize("post_id", [1, 2, 3])
def test_get_post_by_id(api_client, post_id):
    response = api_client.get(f"/posts/{post_id}")

    assert response.status_code == 200, (
        f"Expected GET /posts/{post_id} to return HTTP 200, got {response.status_code}."
    )

    assert_json_content_type(response.headers.get("Content-Type"))
    post = parse_json_response(response)
    assert_post_schema(post)
    assert post["id"] == post_id, (
        f"Expected response post ID to be {post_id}, got {post['id']}."
    )
