#!/usr/bin/env python3
"""Validate an Architecture Council decision record JSON file."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Iterable

ALLOWED_MODES = {"quick", "duo", "full"}
ALLOWED_EXECUTION_MODELS = {
    "single-model structured deliberation",
    "verified isolated agents",
    "verified multi-provider",
}
ALLOWED_STATUSES = {
    "proposed",
    "approved",
    "implemented",
    "confirmed",
    "revised",
    "reversed",
    "inconclusive",
}
ALLOWED_CONFIDENCE = {"high", "medium", "low"}
SECRET_PATTERNS = [
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    re.compile(r"(?i)\b(?:password|passwd|api[_-]?key|access[_-]?token|secret)\s*[:=]\s*[^\s,;]{8,}"),
]


def walk_strings(value: Any) -> Iterable[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for key, child in value.items():
            yield str(key)
            yield from walk_strings(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk_strings(child)


def validate(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return [f"file not found: {path}"]
    except json.JSONDecodeError as exc:
        return [f"invalid JSON: {exc}"]

    if not isinstance(data, dict):
        return ["top-level JSON value must be an object"]

    required = (
        "decision_id",
        "mode",
        "execution_model",
        "panel",
        "evidence_summary",
        "recommendation",
        "vote_tally",
        "minority_position",
        "unresolved_questions",
        "kill_criteria",
        "concrete_next_action",
        "owner",
        "reversal_evidence",
        "status",
        "confidence",
        "limitations",
    )
    for key in required:
        value = data.get(key)
        if value is None or value == "" or value == []:
            errors.append(f"missing or empty required field: {key}")

    decision_id = data.get("decision_id")
    if isinstance(decision_id, str) and not re.fullmatch(r"DEC-\d{4}-\d{3,}", decision_id):
        errors.append("decision_id must match DEC-YYYY-NNN")

    if data.get("mode") not in ALLOWED_MODES:
        errors.append(f"mode must be one of {sorted(ALLOWED_MODES)}")
    if data.get("execution_model") not in ALLOWED_EXECUTION_MODELS:
        errors.append(f"execution_model must be one of {sorted(ALLOWED_EXECUTION_MODELS)}")
    if data.get("status") not in ALLOWED_STATUSES:
        errors.append(f"status must be one of {sorted(ALLOWED_STATUSES)}")
    if data.get("confidence") not in ALLOWED_CONFIDENCE:
        errors.append(f"confidence must be one of {sorted(ALLOWED_CONFIDENCE)}")

    panel = data.get("panel")
    if isinstance(panel, list):
        expected_minimum = {"quick": 3, "duo": 2, "full": 6}.get(data.get("mode"), 1)
        if len(panel) < expected_minimum:
            errors.append(f"panel must contain at least {expected_minimum} reviewers for {data.get('mode')} mode")
        if len(panel) != len({str(x).strip() for x in panel}):
            errors.append("panel contains duplicate reviewers")
    elif panel is not None:
        errors.append("panel must be an array")

    evidence_summary = data.get("evidence_summary")
    if isinstance(evidence_summary, dict):
        for key in ("facts", "inferences", "assumptions", "unknowns"):
            value = evidence_summary.get(key)
            if not isinstance(value, list):
                errors.append(f"evidence_summary.{key} must be an array")
    elif evidence_summary is not None:
        errors.append("evidence_summary must be an object")

    vote_tally = data.get("vote_tally")
    if vote_tally is not None and not isinstance(vote_tally, dict):
        errors.append("vote_tally must be an object")

    kill_criteria = data.get("kill_criteria")
    if isinstance(kill_criteria, list):
        for index, criterion in enumerate(kill_criteria):
            if not isinstance(criterion, dict):
                errors.append(f"kill_criteria[{index}] must be an object")
                continue
            for key in ("condition", "measure", "trigger", "response"):
                if not criterion.get(key):
                    errors.append(f"kill_criteria[{index}].{key} is required")
    elif kill_criteria is not None:
        errors.append("kill_criteria must be an array")

    next_action = data.get("concrete_next_action")
    if isinstance(next_action, str) and ("\n" in next_action.strip() or len(next_action.strip()) < 5):
        errors.append("concrete_next_action must contain exactly one clear action on one line")

    for key in ("unresolved_questions", "reversal_evidence", "limitations"):
        value = data.get(key)
        if value is not None and not isinstance(value, list):
            errors.append(f"{key} must be an array")

    for text in walk_strings(data):
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                errors.append("possible secret or credential detected")
                break

    return sorted(set(errors))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path, help="Path to decision record JSON")
    args = parser.parse_args()
    errors = validate(args.path)
    if errors:
        print("Decision record validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(f"Decision record is valid: {args.path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
