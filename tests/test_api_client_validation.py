
import pytest

from src.api_client import APIClient


pytestmark = pytest.mark.unit


@pytest.mark.parametrize(
    "timeout",
    [
        0,
        -1,
        float("inf"),
        float("nan"),
        True,
        (1, 2, 3),
        (1, 0),
    ],
    ids=[
        "zero",
        "negative",
        "infinite",
        "nan",
        "boolean",
        "too-many-values",
        "invalid-read-timeout",
    ],
)
def test_client_rejects_invalid_timeout(api_session, timeout):
    with pytest.raises(ValueError):
        APIClient(
            base_url="https://example.com",
            session=api_session,
            timeout=timeout,
        )


def test_client_normalizes_base_url(api_session):
    client = APIClient(
        base_url="https://example.com/",
        session=api_session,
    )

    assert client.base_url == "https://example.com"


def test_client_rejects_empty_base_url(api_session):
    with pytest.raises(ValueError, match="must not be empty"):
        APIClient(
            base_url="",
            session=api_session,
        )
