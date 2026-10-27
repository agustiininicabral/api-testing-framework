# API Testing Framework

A small, maintainable API test suite for REST endpoints, built with Python,
`pytest`, and `requests`. The initial target is
[JSONPlaceholder](https://jsonplaceholder.typicode.com), a public demonstration
API.

## Requirements

- Python 3.10 or later
- Python 3.12 is tested in GitHub Actions
- `pip`
- Network access to the configured API base URL for integration tests and the
  complete suite

`requests` is the runtime dependency in `requirements.txt`. `pytest` is the
development and test dependency in `requirements-dev.txt`. Direct and
transitive dependencies are pinned to the versions currently used by the
project to keep package versions consistent across local installs and CI.

## Installation (Windows PowerShell)

Run these commands from the project directory:

```powershell
python -m venv .venv
```

Install the development dependencies into the virtual environment:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
```

## Configuration

The API base URL is read from the `API_BASE_URL` environment variable. If it is
not set, tests use `https://jsonplaceholder.typicode.com`.

Set it for the current PowerShell session with:

```powershell
$env:API_BASE_URL = "https://jsonplaceholder.typicode.com"
```

The value must be an absolute HTTP or HTTPS URL without a query or fragment.
A version prefix such as `/api/v1` is allowed; do not include a specific endpoint
such as `/posts`. Trailing slashes are removed by the client.

## Running tests

Run the offline unit tests from the project root:

```powershell
.\.venv\Scripts\python.exe -m pytest -v -m unit
```

Run the integration tests against JSONPlaceholder (requires network access):

```powershell
.\.venv\Scripts\python.exe -m pytest -v -m integration
```

Run the complete suite (unit and integration tests; requires network access):

```powershell
.\.venv\Scripts\python.exe -m pytest -v
```

Run one test module:

```powershell
.\.venv\Scripts\python.exe -m pytest -v tests/test_posts.py
```

Generate a JUnit XML report:

```powershell
.\.venv\Scripts\python.exe -m pytest -v --junitxml=report.xml
```

The generated `report.xml` is excluded from version control by `.gitignore`.
Pytest and Python cache files are also excluded.

## Covered scenarios

- **GET positive cases:** retrieve all posts and retrieve posts with IDs `1`,
  `2`, and `3`; check successful HTTP status, JSON content type and shape,
  required post fields, strict field types, a non-empty list, unique IDs in
  the collection, and the requested ID.
- **GET negative cases:** verify HTTP 404 for nonexistent ID `99999` and for
  IDs `0`, `-1`, and `abc`.
- **POST positive case:** submit `userId`, `title`, and `body`; check HTTP 201,
  JSON content type, the response post schema and strict types, and that the
  submitted fields are reflected in the response. The returned ID is checked
  as an integer, not against a fixed value.

Requests use finite connection and read timeouts. Tests locally simulate
`ConnectTimeout`, `ReadTimeout`, and `ConnectionError` to verify that Requests
propagates them and that finite timeout values are passed to the request. These
simulations do not rely on an external server failing. Connection and timeout
errors in integration tests are not suppressed or retried automatically.

GitHub Actions runs the offline unit tests on each push and when pull requests
are opened, synchronized, or reopened. The workflow is defined in
[`.github/workflows/tests.yml`](.github/workflows/tests.yml). A separate integration
workflow runs on pushes to `main`, can be run manually, and also runs weekly
against the configured public API. Because it depends on an external service,
its result is kept separate from the offline unit-test gate. See
[`.github/workflows/integration.yml`](.github/workflows/integration.yml).

## API client behavior

`APIClient` is a transport layer. It returns `requests.Response` objects unchanged, including HTTP 4xx and 5xx responses; callers and endpoint tests decide which status codes are expected. It validates absolute HTTP/HTTPS base URLs, accepts an optional path prefix, and rejects query strings and fragments in the base URL. Requests use finite positive timeouts by default. Timeout and connection failures are wrapped in project-specific exceptions while preserving the original exception as the cause. Endpoint tests use `parse_json_response` so empty or malformed JSON bodies fail with an explicit assertion message rather than an uncontextualized decoder error.

## What the framework validates

The current tests check selected endpoint responses: HTTP status codes,
expected JSON list/object shapes, required post fields, strict primitive types,
and selected values returned by the API. They do not verify an application's
business rules, authentication or authorization, performance, security,
compatibility across API implementations, or durable data storage.

## Limitations

JSONPlaceholder is an external demonstration service. Running the tests
requires network access, and outages, rate limits, or service behavior changes
can affect results independently of this project.

Its write endpoints simulate changes and do not provide durable persistence.
The POST test validates the create response only; it does not claim that the
post was permanently saved and does not try to retrieve it afterward.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).
