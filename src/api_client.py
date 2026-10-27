import math
from typing import Any
from urllib.parse import urlsplit

import requests


DEFAULT_REQUEST_TIMEOUT = (3.05, 10.0)
Timeout = float | tuple[float, float]


class APIClientTimeoutError(requests.Timeout):
    """Raised when a request made by the API client times out."""


class APIClientConnectionError(requests.ConnectionError):
    """Raised when a request made by the API client cannot connect."""


def _validate_timeout(timeout: Timeout) -> None:
    values = timeout if isinstance(timeout, tuple) else (timeout,)
    if not values or any(
        not isinstance(value, (int, float))
        or isinstance(value, bool)
        or not math.isfinite(value)
        or value <= 0
        for value in values
    ):
        raise ValueError("Timeout values must be finite positive numbers.")

    if isinstance(timeout, tuple) and len(timeout) != 2:
        raise ValueError("A timeout tuple must contain connect and read values.")


class APIClient:
    def __init__(
        self,
        base_url: str,
        session: requests.Session,
        timeout: Timeout = DEFAULT_REQUEST_TIMEOUT,
    ) -> None:
        normalized_base_url = base_url.strip().rstrip("/")
        if not normalized_base_url:
            raise ValueError("The API base URL must not be empty.")

        try:
            parsed_base_url = urlsplit(normalized_base_url)
            _ = parsed_base_url.port
        except ValueError as error:
            raise ValueError(
                "The API base URL must be an absolute HTTP or HTTPS URL."
            ) from error

        if (
            parsed_base_url.scheme not in {"http", "https"}
            or not parsed_base_url.hostname
            or parsed_base_url.username is not None
            or parsed_base_url.password is not None
            or parsed_base_url.query
            or parsed_base_url.fragment
        ):
            raise ValueError(
                "The API base URL must be an absolute HTTP or HTTPS URL "
                "without credentials, a query, or a fragment."
            )

        _validate_timeout(timeout)

        self.base_url = normalized_base_url
        self.session = session
        self.timeout = timeout

    def request(
        self,
        method: str,
        path: str,
        *,
        timeout: Timeout | None = None,
        **kwargs: Any,
    ) -> requests.Response:
        request_timeout = self.timeout if timeout is None else timeout
        _validate_timeout(request_timeout)
        url = f"{self.base_url}/{path.lstrip('/')}"

        try:
            return self.session.request(
                method,
                url,
                timeout=request_timeout,
                **kwargs,
            )
        except requests.Timeout as error:
            raise APIClientTimeoutError(f"{method.upper()} {url} timed out.") from error
        except requests.ConnectionError as error:
            raise APIClientConnectionError(
                f"Unable to connect for {method.upper()} {url}."
            ) from error

    def get(
        self,
        path: str,
        *,
        timeout: Timeout | None = None,
        **kwargs: Any,
    ) -> requests.Response:
        return self.request("GET", path, timeout=timeout, **kwargs)

    def post(
        self,
        path: str,
        *,
        timeout: Timeout | None = None,
        **kwargs: Any,
    ) -> requests.Response:
        return self.request("POST", path, timeout=timeout, **kwargs)
