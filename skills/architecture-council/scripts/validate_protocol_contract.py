#!/usr/bin/env python3
"""Validate cross-source Architecture Council protocol invariants.

`SKILL.md` remains authoritative for trigger and execution behavior. This script does
not create a second product configuration. It encodes regression expectations and
verifies that human-facing references and executable validators still describe the
same published protocol.
"""
from __future__ import annotations

import argparse
import ast
import re
import sys
from pathlib import Path

REVIEWERS = (
    "Strategic and Business Reviewer",
    "Technical and Security Architect",
    "Delivery and PMO Reviewer",
    "Risk and Governance Reviewer",
    "Operational Simplicity Reviewer",
    "Customer and Stakeholder Reviewer",
)
EXPECTED_EXECUTION_MODELS = {
    "single-model structured deliberation",
    "verified isolated agents",
    "verified multi-provider",
}
EXPECTED_RESULTS = {"recommended", "split", "defer", "reject"}
EXPECTED_CONFIDENCE = {"high", "medium", "low"}


def read(skill_root: Path, relative: str) -> str:
    return (skill_root / relative).read_text(encoding="utf-8")


def literal_assignment(source: str, name: str):
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if not isinstance(node, ast.Assign):
            continue
        if not any(isinstance(target, ast.Name) and target.id == name for target in node.targets):
            continue
        try:
            return ast.literal_eval(node.value)
        except (ValueError, TypeError):
            return None
    return None


def require(errors: list[str], condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def validate_contract(skill_root: Path) -> list[str]:
    errors: list[str] = []
    try:
        skill = read(skill_root, "SKILL.md")
        routing = read(skill_root, "references/routing-and-modes.md")
        roles = read(skill_root, "references/reviewer-roles.md")
        protocol = read(skill_root, "references/council-protocol.md")
        output = read(skill_root, "references/output-contract.md")
        security = read(skill_root, "references/security-and-provider-policy.md")
        record = read(skill_root, "scripts/validate_decision_record.py")
    except FileNotFoundError as exc:
        return [f"missing protocol source: {exc.filename}"]

    for reviewer in REVIEWERS:
        require(errors, reviewer in skill, f"SKILL.md missing professional reviewer: {reviewer}")
        require(errors, f"## {reviewer}" in roles, f"reviewer-roles.md missing reviewer heading: {reviewer}")

    require(errors, "7. Independent Chairman" in skill, "SKILL.md must list Independent Chairman separately")
    require(errors, "The Chairman synthesizes only and does not vote." in skill, "SKILL.md must keep Chairman synthesis-only and non-voting")
    require(errors, "Synthesize only. Do not vote." in roles, "reviewer-roles.md must keep Chairman non-voting")
    require(errors, "Independent Chairman synthesize without voting" in protocol, "council-protocol.md must keep Chairman non-voting")

    mode_patterns = {
        "quick": r"## Quick Council\s+Use three relevant professional reviewers",
        "duo": r"## Duo Review\s+Use two opposing professional lenses",
        "full": r"## Full Council\s+Use all six professional reviewers plus the Independent Chairman",
    }
    for mode, pattern in mode_patterns.items():
        require(errors, bool(re.search(pattern, routing, flags=re.MULTILINE)), f"routing-and-modes.md {mode} panel contract drifted")
    require(
        errors,
        bool(re.search(r'expected=\{"quick":3,"duo":2,"full":6\}\.get', record)),
        "validate_decision_record.py mode panel sizes must remain quick=3, duo=2, full=6",
    )

    require(errors, all(label in skill for label in ("`FACT`", "`INFERENCE`", "`ASSUMPTION`", "`UNKNOWN`")), "SKILL.md evidence taxonomy drifted")
    require(
        errors,
        '("facts","inferences","assumptions","unknowns")' in record,
        "validate_decision_record.py evidence taxonomy drifted",
    )

    stance_contract = "STANCE: <option> | CONFIDENCE: high|medium|low | DEALBREAKER: <observable condition>"
    require(errors, stance_contract in skill, "SKILL.md STANCE contract drifted")
    require(
        errors,
        '("reviewer","option","confidence","dealbreaker")' in record,
        "validate_decision_record.py stance field contract drifted",
    )

    require(errors, "high `1.00`, medium `0.75`, and low `0.50`" in skill, "SKILL.md confidence factors drifted")
    require(
        errors,
        'factors={"high":1.0,"medium":0.75,"low":0.5}' in record,
        "validate_decision_record.py confidence factors drifted",
    )
    require(errors, "base weight of `1.5`; all others receive `1.0`" in skill, "SKILL.md base weights drifted")
    require(
        errors,
        'base=1.5 if s.get("reviewer")==seat else 1.0' in record,
        "validate_decision_record.py domain weighting drifted",
    )
    require(errors, "two-thirds of total possible base weight" in skill, "SKILL.md recommendation threshold drifted")
    require(errors, "two-thirds recommendation threshold" in output, "output-contract.md recommendation threshold drifted")
    require(
        errors,
        "threshold=(2/3)*total if total else 0" in record,
        "validate_decision_record.py recommendation threshold drifted",
    )
    require(errors, "A split result is required when no option reaches the threshold." in output, "output-contract.md split semantics drifted")

    execution_models = literal_assignment(record, "ALLOWED_EXECUTION_MODELS")
    results = literal_assignment(record, "ALLOWED_RESULTS")
    confidence = literal_assignment(record, "ALLOWED_CONFIDENCE")
    require(errors, execution_models == EXPECTED_EXECUTION_MODELS, "validate_decision_record.py execution model enum drifted")
    require(errors, results == EXPECTED_RESULTS, "validate_decision_record.py result enum drifted")
    require(errors, confidence == EXPECTED_CONFIDENCE, "validate_decision_record.py confidence enum drifted")
    require(errors, "single-model structured deliberation" in skill, "SKILL.md must name single-model structured deliberation")
    require(errors, "Never claim provider or model independence without verification." in skill, "SKILL.md execution-honesty guard drifted")
    require(errors, "report the actual execution model" in security, "security policy must require actual execution-model reporting")

    return sorted(set(errors))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skill_root", nargs="?", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    errors = validate_contract(args.skill_root.resolve())
    if errors:
        print("Protocol contract validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("Protocol contract validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
