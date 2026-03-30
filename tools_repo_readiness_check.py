#!/usr/bin/env python3
"""Repository readiness checker for the AI Analytics Assistant v2 milestone.

This script validates whether the local repository contains a minimum set of
files and directories required for a production-minded AI analytics assistant
project. It is intentionally dependency-free and can be run in CI.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence


DEFAULT_REQUIRED_PATHS: tuple[str, ...] = (
    "README.md",
    "src",
    "tests",
)

DEFAULT_RECOMMENDED_PATHS: tuple[str, ...] = (
    "requirements.txt",
    "pyproject.toml",
    ".github/workflows",
    "docs",
)


@dataclass(frozen=True)
class CheckResult:
    required_present: list[str]
    required_missing: list[str]
    recommended_present: list[str]
    recommended_missing: list[str]

    @property
    def ok(self) -> bool:
        return len(self.required_missing) == 0


def _partition_paths(root: Path, paths: Iterable[str]) -> tuple[list[str], list[str]]:
    present: list[str] = []
    missing: list[str] = []

    for rel_path in paths:
        if (root / rel_path).exists():
            present.append(rel_path)
        else:
            missing.append(rel_path)

    return present, missing


def run_check(
    root: Path,
    required_paths: Sequence[str] = DEFAULT_REQUIRED_PATHS,
    recommended_paths: Sequence[str] = DEFAULT_RECOMMENDED_PATHS,
) -> CheckResult:
    required_present, required_missing = _partition_paths(root, required_paths)
    recommended_present, recommended_missing = _partition_paths(root, recommended_paths)

    return CheckResult(
        required_present=required_present,
        required_missing=required_missing,
        recommended_present=recommended_present,
        recommended_missing=recommended_missing,
    )


def format_text_report(result: CheckResult) -> str:
    status = "PASS" if result.ok else "FAIL"

    lines = [
        "AI Analytics Assistant v2 - Repository Readiness Report",
        f"Status: {status}",
        "",
        f"Required present ({len(result.required_present)}): {', '.join(result.required_present) or '-'}",
        f"Required missing ({len(result.required_missing)}): {', '.join(result.required_missing) or '-'}",
        f"Recommended present ({len(result.recommended_present)}): {', '.join(result.recommended_present) or '-'}",
        f"Recommended missing ({len(result.recommended_missing)}): {', '.join(result.recommended_missing) or '-'}",
    ]

    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate repository readiness for v2 milestones.")
    parser.add_argument("--root", default=".", help="Path to repository root (default: current directory).")
    parser.add_argument("--json", action="store_true", help="Output machine-readable JSON.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()

    result = run_check(root=root)

    if args.json:
        print(
            json.dumps(
                {
                    "ok": result.ok,
                    "required_present": result.required_present,
                    "required_missing": result.required_missing,
                    "recommended_present": result.recommended_present,
                    "recommended_missing": result.recommended_missing,
                },
                indent=2,
            )
        )
    else:
        print(format_text_report(result))

    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
