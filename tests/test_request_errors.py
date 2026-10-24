import math

import pytest
import requests

from src.api_client import APIClientConnectionError, APIClientTimeoutError


pytestmark = pytest.mark.unit


@pytest.mark.parametrize(
    "timeout_error",
    [requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout],
    ids=["connect-timeout", "read-timeout"],
)
def test_request_timeout_errors_propagate(
    api_client,
    api_session,
    monkeypatch,
    timeout_error,
):
    sent_kwargs = {}

    def raise_timeout(_request, **kwargs):
        sent_kwargs.update(kwargs)
        raise timeout_error("Simulated request timeout.")

    monkeypatch.setattr(api_session, "send", raise_timeout)

    with pytest.raises(APIClientTimeoutError) as error:
        api_client.get("/posts/1")

    assert isinstance(error.value.__cause__, timeout_error)
    assert sent_kwargs["timeout"] == api_client.timeout
    assert all(
        math.isfinite(timeout) and timeout > 0
        for timeout in sent_kwargs["timeout"]
    ), "Expected connection and read timeouts to be finite and positive."


def test_connection_error_propagates(
    api_client,
    api_session,
    monkeypatch,
):
    def raise_connection_error(_request, **_kwargs):
        raise requests.exceptions.ConnectionError("Simulated connection error.")

    monkeypatch.setattr(api_session, "send", raise_connection_error)

    with pytest.raises(
        APIClientConnectionError,
        match="Unable to connect",
    ):
        api_client.get("/posts/1")
