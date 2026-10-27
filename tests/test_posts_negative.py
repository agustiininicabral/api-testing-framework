import pytest


pytestmark = pytest.mark.integration


def test_get_nonexistent_post(api_client):
    post_id = 99999
    response = api_client.get(f"/posts/{post_id}")

    assert response.status_code == 404, f"Expected GET /posts/{post_id} to return HTTP 404, got {response.status_code}."


@pytest.mark.parametrize(
    "post_id",
    ["0", "-1", "abc"],
    ids=["zero", "negative", "non-numeric"],
)
def test_get_post_with_invalid_id(
    api_client,
    post_id,
):
    response = api_client.get(f"/posts/{post_id}")

    assert response.status_code == 404, (
        f"Expected GET /posts/{post_id} to return HTTP 404 based on the "
        f"observed JSONPlaceholder response, got {response.status_code}."
    )
