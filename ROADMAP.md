# Repository Completion Plan

This roadmap defines the completion criteria for the API Testing Framework. Work should be delivered in small, reviewable changes, with CI evidence for each milestone. A milestone is not complete merely because code was written.

## Milestone 1 — Validation helpers and edge cases
- [x] Add unit tests for accepted and rejected JSON Content-Type values.
- [x] Test response schema validation for non-object values, missing fields, and invalid primitive types.
- [x] Run the unit suite in GitHub Actions and record the result. The two latest runs for this branch completed successfully: [test changes](https://github.com/agustiininicabral/api-testing-framework/actions/runs/40443741251) and [roadmap commit](https://github.com/agustiininicabral/api-testing-framework/actions/runs/40443744292).

## Milestone 2 — API client behavior
- [x] Review URL/path normalization and timeout validation edge cases.
- [x] Verify timeout and connection exceptions preserve their original causes.
- [x] Decide and document whether HTTP error responses should be returned unchanged or raised as exceptions; test the chosen contract. The client returns HTTP error responses unchanged; endpoint tests own status-code assertions.
- [x] Test request forwarding and supported methods without external network access.

## Milestone 3 — Integration coverage
- [x] Add deterministic tests for malformed JSON and empty response bodies using mocked responses; endpoint tests now use the shared parser helper.
- [x] Keep real API integration tests clearly separated from offline unit tests.
- [x] Validate positive, negative, response-shape, and create-response scenarios against the configured API. The post-merge integration workflow passed on commit `b616ec8`.
- [x] Document external-service limitations and avoid claiming persistence for simulated writes.

## Milestone 4 — CI and maintainability
- [x] Ensure CI installs pinned dependencies and runs all offline tests on pushes and pull requests; add pip caching and a downloadable JUnit report.
- [x] Add a separate manually triggered and weekly integration workflow against the public demo API, accounting for external outages and rate limits.
- [x] Publish JUnit test reports as short-lived workflow artifacts and keep secrets out of logs.
- [ ] Finish validating Ruff formatting/lint checks and `pip check`; no separate type checker or security scanner is planned for this small test-only client unless future complexity justifies it.

## Milestone 5 — Documentation and release readiness
- [x] Align README instructions with actual test markers and CI behavior.
- [x] Document configuration, expected behavior, limitations, and reproducible commands.
- [x] Review `.gitignore`, dependency pins, MIT license, and repository metadata.
- [ ] Run the complete feasible validation matrix and review the final Git diff.
- [ ] Publish a final status report listing verified checks, known limitations, and follow-up work.

## Completion rules
- Do not claim tests passed unless a test runner or CI result confirms it.
- Prefer small branches and pull requests over unreviewed changes directly on the default branch.
- Do not add secrets, credentials, personal data, or generated environment files to the repository.
- Do not change the API client's public behavior without tests and documentation.
- Reassess the roadmap when repository evidence shows that an item is unnecessary or a higher-priority defect exists.
