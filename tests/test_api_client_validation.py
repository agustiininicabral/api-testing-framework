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


@pytest.mark.parametrize(
    "timeout",
    [0, -1, float("inf"), float("nan"), True, (1, 2, 3), (1, 0)],
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
def test_request_rejects_invalid_timeout_override(api_client, monkeypatch, timeout):
    request_called = False

    def fake_request(*_args, **_kwargs):
        nonlocal request_called
        request_called = True

    monkeypatch.setattr(api_client.session, "request", fake_request)

    with pytest.raises(ValueError):
        api_client.get("/posts/1", timeout=timeout)

    assert not request_called, (
        "Invalid timeout must be rejected before sending a request."
    )


@pytest.mark.parametrize(
    "base_url",
    [
        "example.com",
        "ftp://example.com",
        "https://",
        "https://example.com?query=1",
        "https://example.com#fragment",
    ],
    ids=[
        "missing-scheme",
        "unsupported-scheme",
        "missing-host",
        "contains-query",
        "contains-fragment",
    ],
)
def test_client_rejects_invalid_base_url(api_session, base_url):
    with pytest.raises(ValueError, match="absolute HTTP or HTTPS URL"):
        APIClient(base_url=base_url, session=api_session)


def test_client_rejects_whitespace_base_url(api_session):
    with pytest.raises(ValueError, match="must not be empty"):
        APIClient(base_url="   ", session=api_session)


def test_client_accepts_base_url_path_prefix(api_session):
    client = APIClient(
        base_url="https://example.com/api/",
        session=api_session,
    )

    assert client.base_url == "https://example.com/api"
