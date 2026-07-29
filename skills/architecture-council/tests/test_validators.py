#!/usr/bin/env python3
"""Self-contained tests for Architecture Council validators."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOSSIER_VALIDATOR = ROOT / "scripts" / "validate_decision_dossier.py"
RECORD_VALIDATOR = ROOT / "scripts" / "validate_decision_record.py"
BUNDLE_VALIDATOR = ROOT / "scripts" / "validate_skill_bundle.py"


def run(script: Path, target: Path, expected: int) -> None:
    result = subprocess.run(
        [sys.executable, str(script), str(target)],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != expected:
        raise AssertionError(
            f"{script.name} returned {result.returncode}, expected {expected}\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )


def valid_dossier() -> dict:
    return {
        "decision_id": "DEC-2026-001",
        "title": "Select a target architecture",
        "question": "Which architecture best meets the approved outcome?",
        "required_outcome": "A supportable and secure target architecture",
        "options": [
            {"id": "a", "name": "Option A", "description": "Centralized design"},
            {"id": "b", "name": "Option B", "description": "Distributed design"},
        ],
        "constraints": ["Preserve rollback"],
        "success_criteria": ["Acceptance tests pass"],
        "evidence": [
            {"label": "FACT", "statement": "Current dependency is documented", "source": "approved inventory"},
            {"label": "INFERENCE", "statement": "Centralization may reduce variation", "source": "current operating data"},
            {"label": "ASSUMPTION", "statement": "The operating team can support the target", "source": None},
            {"label": "UNKNOWN", "statement": "Final adoption rate is unknown", "source": None},
        ],
        "reversibility": "partially-reversible",
        "deadline": "2026-08-15",
        "decision_authority": "Architecture owner",
        "risk_of_action": ["Migration disruption"],
        "risk_of_inaction": ["Continued inconsistency"],
        "sensitivity": "internal",
        "external_provider_allowed": False,
        "related_decisions": [],
        "related_skills": [],
        "related_lessons": [],
    }


def valid_record() -> dict:
    return {
        "decision_id": "DEC-2026-001",
        "mode": "full",
        "execution_model": "single-model structured deliberation",
        "panel": ["strategy", "technical", "delivery", "risk", "operations", "stakeholder"],
        "domain_weight_seat": "technical",
        "evidence_summary": {"facts": ["fact"], "inferences": ["inference"], "assumptions": ["assumption"], "unknowns": ["unknown"]},
        "recommendation": "Proceed with Option A subject to the kill criteria.",
        "vote_tally": {"a": 4.5, "b": 1.5},
        "minority_position": "Option B should prevail if operating capacity is not confirmed.",
        "unresolved_questions": ["Can the operating team support the target?"],
        "kill_criteria": [
            {"condition": "Support load exceeds threshold", "measure": "More than 10 incidents", "trigger": "First 30 days", "response": "Pause rollout"}
        ],
        "concrete_next_action": "Validate operating capacity against the target support model.",
        "owner": "Architecture owner",
        "review_date": "2026-08-15",
        "reversal_evidence": ["Support capacity is insufficient"],
        "status": "proposed",
        "confidence": "medium",
        "limitations": ["Single-model structured deliberation"],
    }


def main() -> int:
    with tempfile.TemporaryDirectory() as directory:
        temp = Path(directory)

        dossier_path = temp / "dossier.json"
        dossier_path.write_text(json.dumps(valid_dossier(), indent=2), encoding="utf-8")
        run(DOSSIER_VALIDATOR, dossier_path, 0)

        bad_dossier = valid_dossier()
        bad_dossier["decision_id"] = "bad"
        bad_dossier["evidence"][0]["statement"] = "api_key=" + "sk-" + ("a" * 30)
        bad_dossier_path = temp / "bad-dossier.json"
        bad_dossier_path.write_text(json.dumps(bad_dossier, indent=2), encoding="utf-8")
        run(DOSSIER_VALIDATOR, bad_dossier_path, 1)

        record_path = temp / "record.json"
        record_path.write_text(json.dumps(valid_record(), indent=2), encoding="utf-8")
        run(RECORD_VALIDATOR, record_path, 0)

        bad_record = valid_record()
        bad_record["mode"] = "ceremonial"
        bad_record["kill_criteria"] = [{}]
        bad_record_path = temp / "bad-record.json"
        bad_record_path.write_text(json.dumps(bad_record, indent=2), encoding="utf-8")
        run(RECORD_VALIDATOR, bad_record_path, 1)

    run(BUNDLE_VALIDATOR, ROOT, 0)
    print("All Architecture Council validator tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
