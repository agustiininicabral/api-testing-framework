# Repository Completion Plan

This roadmap defines the completion criteria for the API Testing Framework. Work should be delivered in small, reviewable changes, with CI evidence for each milestone. A milestone is not complete merely because code was written.

## Milestone 1 — Validation helpers and edge cases
- [x] Add unit tests for accepted and rejected JSON Content-Type values.
- [x] Test response schema validation for non-object values, missing fields, and invalid primitive types.
- [x] Run the unit suite in GitHub Actions and record the result. The two latest runs for this branch completed successfully: [test changes](https://github.com/agustiininicabral/api-testing-framework/actions/runs/40443741251) and [roadmap commit](https://github.com/agustiininicabral/api-testing-framework/actions/runs/40443744292).

## Milestone 2 — API client behavior
- [ ] Review URL/path normalization and timeout validation edge cases.
- [ ] Verify timeout and connection exceptions preserve their original causes.
- [ ] Decide and document whether HTTP error responses should be returned unchanged or raised as exceptions; test the chosen contract.
- [ ] Test request forwarding and supported methods without external network access.

## Milestone 3 — Integration coverage
- [ ] Add deterministic tests for malformed JSON and empty response bodies using mocked responses where appropriate.
- [ ] Keep real API integration tests clearly separated from offline unit tests.
- [ ] Validate positive, negative, response-shape, and create-response scenarios against the configured API.
- [ ] Document external-service limitations and avoid claiming persistence for simulated writes.

## Milestone 4 — CI and maintainability
- [ ] Ensure CI installs pinned dependencies and runs all offline tests on pushes and pull requests.
- [ ] Evaluate a separate integration job against the public demo API, accounting for external outages and rate limits.
- [ ] Add useful test reports and make failures diagnosable without exposing secrets.
- [ ] Check formatting, linting, type checks, and dependency/security checks; adopt only tools that provide value for this small project.

## Milestone 5 — Documentation and release readiness
- [ ] Align README instructions with actual test markers and CI behavior.
- [ ] Document configuration, expected behavior, limitations, and reproducible commands.
- [ ] Review .gitignore, dependency pins, license, repository metadata, and public-facing presentation.
- [ ] Run the complete feasible validation matrix and review the final Git diff.
- [ ] Publish a final status report listing verified checks, known limitations, and follow-up work.

## Completion rules
- Do not claim tests passed unless a test runner or CI result confirms it.
- Prefer small branches and pull requests over unreviewed changes directly on the default branch.
- Do not add secrets, credentials, personal data, or generated environment files to the repository.
- Do not change the API client's public behavior without tests and documentation.
- Reassess the roadmap when repository evidence shows that an item is unnecessary or a higher-priority defect exists.
