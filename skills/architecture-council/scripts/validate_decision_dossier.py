#!/usr/bin/env python3
"""Validate an Architecture Council decision dossier JSON file."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Iterable

ALLOWED_LABELS = {"FACT", "INFERENCE", "ASSUMPTION", "UNKNOWN"}
ALLOWED_REVERSIBILITY = {
    "reversible",
    "partially-reversible",
    "difficult-to-reverse",
    "irreversible",
}
ALLOWED_SENSITIVITY = {"public", "internal", "confidential", "restricted"}
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


def require(data: dict[str, Any], key: str, errors: list[str]) -> Any:
    value = data.get(key)
    if value is None or value == "" or value == []:
        errors.append(f"missing or empty required field: {key}")
    return value


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

    for key in (
        "decision_id",
        "title",
        "question",
        "required_outcome",
        "options",
        "constraints",
        "evidence",
        "reversibility",
        "decision_authority",
        "risk_of_action",
        "risk_of_inaction",
        "sensitivity",
        "external_provider_allowed",
    ):
        require(data, key, errors)

    decision_id = data.get("decision_id")
    if isinstance(decision_id, str) and not re.fullmatch(r"DEC-\d{4}-\d{3,}", decision_id):
        errors.append("decision_id must match DEC-YYYY-NNN")

    options = data.get("options")
    if isinstance(options, list):
        if len(options) < 2:
            errors.append("options must contain at least two entries")
        seen_ids: set[str] = set()
        for index, option in enumerate(options):
            if not isinstance(option, dict):
                errors.append(f"options[{index}] must be an object")
                continue
            for key in ("id", "name", "description"):
                if not option.get(key):
                    errors.append(f"options[{index}].{key} is required")
            option_id = option.get("id")
            if isinstance(option_id, str):
                if option_id in seen_ids:
                    errors.append(f"duplicate option id: {option_id}")
                seen_ids.add(option_id)
    elif options is not None:
        errors.append("options must be an array")

    evidence = data.get("evidence")
    labels_seen: set[str] = set()
    if isinstance(evidence, list):
        for index, item in enumerate(evidence):
            if not isinstance(item, dict):
                errors.append(f"evidence[{index}] must be an object")
                continue
            label = item.get("label")
            statement = item.get("statement")
            if label not in ALLOWED_LABELS:
                errors.append(f"evidence[{index}].label must be one of {sorted(ALLOWED_LABELS)}")
            else:
                labels_seen.add(label)
            if not statement:
                errors.append(f"evidence[{index}].statement is required")
            if label == "FACT" and not item.get("source"):
                errors.append(f"evidence[{index}] FACT requires a source")
        if "UNKNOWN" not in labels_seen:
            errors.append("evidence must include at least one UNKNOWN or explicitly document that no material unknown remains")
    elif evidence is not None:
        errors.append("evidence must be an array")

    if data.get("reversibility") not in ALLOWED_REVERSIBILITY:
        errors.append(f"reversibility must be one of {sorted(ALLOWED_REVERSIBILITY)}")

    sensitivity = data.get("sensitivity")
    if sensitivity not in ALLOWED_SENSITIVITY:
        errors.append(f"sensitivity must be one of {sorted(ALLOWED_SENSITIVITY)}")

    external_allowed = data.get("external_provider_allowed")
    if not isinstance(external_allowed, bool):
        errors.append("external_provider_allowed must be a boolean")
    if sensitivity in {"confidential", "restricted"} and external_allowed is True:
        errors.append("confidential or restricted dossiers cannot enable external providers without a separately documented approval")

    for key in ("constraints", "risk_of_action", "risk_of_inaction"):
        value = data.get(key)
        if value is not None and (not isinstance(value, list) or not all(isinstance(x, str) and x.strip() for x in value)):
            errors.append(f"{key} must be a non-empty array of strings")

    for text in walk_strings(data):
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                errors.append("possible secret or credential detected")
                break

    return sorted(set(errors))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path, help="Path to decision dossier JSON")
    args = parser.parse_args()
    errors = validate(args.path)
    if errors:
        print("Decision dossier validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(f"Decision dossier is valid: {args.path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
