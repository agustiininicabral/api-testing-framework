import os
from collections.abc import Iterator

import pytest
import requests

from src.api_client import APIClient

DEFAULT_API_BASE_URL = "https://jsonplaceholder.typicode.com"


@pytest.fixture
def api_session() -> Iterator[requests.Session]:
    with requests.Session() as session:
        yield session


@pytest.fixture(scope="session")
def api_base_url() -> str:
    return os.getenv("API_BASE_URL", DEFAULT_API_BASE_URL).rstrip("/")


@pytest.fixture
def api_client(api_session, api_base_url) -> APIClient:
    return APIClient(base_url=api_base_url, session=api_session)
