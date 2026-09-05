from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = ROOT / "skills" / "architecture-council" / "scripts" / "validate_decision_record.py"
SPEC = importlib.util.spec_from_file_location("validate_decision_record", VALIDATOR_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def base_record() -> dict:
    return {
        "decision_id": "DEC-2026-001",
        "result": "recommended",
        "recommended_option": "a",
        "decision_authority": "Architecture owner",
        "mode": "full",
        "execution_model": "single-model structured deliberation",
        "panel": ["strategy", "technical", "delivery", "risk", "operations", "stakeholder"],
        "domain_weight_seat": "technical",
        "reviewer_stances": [
            {"reviewer": "strategy", "option": "a", "confidence": "high", "dealbreaker": "ROI fails"},
            {"reviewer": "technical", "option": "a", "confidence": "high", "dealbreaker": "Security fails"},
            {"reviewer": "delivery", "option": "a", "confidence": "high", "dealbreaker": "No rollback"},
            {"reviewer": "risk", "option": "a", "confidence": "medium", "dealbreaker": "Control fails"},
            {"reviewer": "operations", "option": "b", "confidence": "medium", "dealbreaker": "Support load high"},
            {"reviewer": "stakeholder", "option": "a", "confidence": "medium", "dealbreaker": "Customer rejects"},
        ],
        "evidence_summary": {"facts": ["fact"], "inferences": ["inference"], "assumptions": ["assumption"], "unknowns": ["unknown"]},
        "recommendation": "Proceed with A.",
        "rationale": ["Secure", "Supportable"],
        "acceptable_compromises": ["Phased rollout"],
        "vote_tally": {"a": 5.0, "b": 0.75},
        "minority_position": "Choose B if support capacity fails.",
        "unresolved_questions": ["Final support capacity"],
        "kill_criteria": [{"condition": "Support load exceeds threshold", "measure": "More than 10 incidents", "trigger": "First 30 days", "response": "Pause rollout", "decision_authority": "Architecture owner"}],
        "concrete_next_action": "Validate operating capacity against the target support model.",
        "implementation_action": "Run a controlled pilot.",
        "owner": "Architecture owner",
        "due_or_trigger": "Before production approval",
        "prediction": "A will reduce variation without breaching support thresholds.",
        "review_date": "2026-08-15",
        "review_condition": None,
        "success_evidence": ["Acceptance tests pass"],
        "reversal_evidence": ["Support capacity is insufficient"],
        "expected_cost_of_reversal": "One maintenance window and rollback effort.",
        "status": "proposed",
        "confidence": "medium",
        "limitations": ["Single-model structured deliberation"],
    }


def errors(record: dict) -> list[str]:
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "record.json"
        path.write_text(json.dumps(record), encoding="utf-8")
        return MODULE.validate(path)


class ProtocolRuntimeRegressionTests(unittest.TestCase):
    def test_independent_chairman_cannot_vote(self) -> None:
        record = base_record()
        record["panel"][-1] = "Independent Chairman"
        record["reviewer_stances"][-1]["reviewer"] = "Independent Chairman"
        self.assertTrue(any("Independent Chairman" in error for error in errors(record)))

    def test_no_threshold_winner_requires_split(self) -> None:
        record = base_record()
        for index, stance in enumerate(record["reviewer_stances"]):
            stance["option"] = "a" if index < 3 else "b"
            stance["confidence"] = "high"
        record["vote_tally"] = {"a": 3.5, "b": 3.0}
        record["recommended_option"] = None
        record["result"] = "defer"
        self.assertTrue(any("requires result split" in error for error in errors(record)))
        record["result"] = "split"
        self.assertEqual([], errors(record))


if __name__ == "__main__":
    unittest.main()
