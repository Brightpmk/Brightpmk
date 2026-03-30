# v2 Milestone: Repository Readiness Guardrail

## Why this milestone
During the initial audit, the checked-out repository did not contain application
source modules for the AI Analytics Assistant. This milestone adds a lightweight,
dependency-free readiness check so the repository can detect missing critical
structure early in local development and CI.

## What was added
- `tools_repo_readiness_check.py`
  - Checks required paths (`README.md`, `src`, `tests`)
  - Checks recommended paths (`requirements.txt`, `pyproject.toml`, `.github/workflows`, `docs`)
  - Supports both text and JSON output
  - Returns non-zero exit code when required paths are missing
- `tests/test_repo_readiness_check.py`
  - Unit tests for failing and passing scenarios
  - Unit test for report formatting

## Usage
```bash
python tools_repo_readiness_check.py
python tools_repo_readiness_check.py --json
```

## Notes
This does not replace application tests; it is a bootstrap quality gate that
keeps project structure explicit and reviewable while v2 implementation is
incrementally developed.
