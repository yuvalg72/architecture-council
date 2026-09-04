from __future__ import annotations

import importlib.util
import shutil
import tempfile
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = SKILL_ROOT / "scripts" / "validate_protocol_contract.py"
SPEC = importlib.util.spec_from_file_location("validate_protocol_contract", VALIDATOR_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class ProtocolContractMutationTests(unittest.TestCase):
    def mutated_errors(self, relative: str, old: str, new: str) -> list[str]:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "architecture-council"
            shutil.copytree(SKILL_ROOT, target)
            path = target / relative
            text = path.read_text(encoding="utf-8")
            self.assertIn(old, text, f"mutation source missing in {relative}")
            path.write_text(text.replace(old, new, 1), encoding="utf-8")
            return MODULE.validate_contract(target)

    def test_current_contract_passes(self) -> None:
        self.assertEqual([], MODULE.validate_contract(SKILL_ROOT))

    def test_quick_panel_size_drift_fails(self) -> None:
        errors = self.mutated_errors(
            "references/routing-and-modes.md",
            "Use three relevant professional reviewers",
            "Use four relevant professional reviewers",
        )
        self.assertTrue(any("quick panel" in error for error in errors))

    def test_medium_confidence_drift_fails(self) -> None:
        errors = self.mutated_errors("SKILL.md", "medium `0.75`", "medium `0.70`")
        self.assertTrue(any("confidence factors" in error for error in errors))

    def test_domain_weight_drift_fails(self) -> None:
        errors = self.mutated_errors("SKILL.md", "base weight of `1.5`", "base weight of `2.0`")
        self.assertTrue(any("base weights" in error for error in errors))

    def test_reviewer_roster_drift_fails(self) -> None:
        errors = self.mutated_errors(
            "references/reviewer-roles.md",
            "## Customer and Stakeholder Reviewer",
            "## Customer Reviewer",
        )
        self.assertTrue(any("missing reviewer heading" in error for error in errors))

    def test_chairman_voting_drift_fails(self) -> None:
        errors = self.mutated_errors(
            "references/reviewer-roles.md",
            "Synthesize only. Do not vote.",
            "Synthesize and vote.",
        )
        self.assertTrue(any("Chairman non-voting" in error for error in errors))

    def test_threshold_drift_fails(self) -> None:
        errors = self.mutated_errors(
            "references/output-contract.md",
            "two-thirds recommendation threshold",
            "three-quarters recommendation threshold",
        )
        self.assertTrue(any("recommendation threshold" in error for error in errors))

    def test_execution_model_enum_drift_fails(self) -> None:
        errors = self.mutated_errors(
            "scripts/validate_decision_record.py",
            '"verified multi-provider"}',
            '"verified multi-provider","experimental model"}',
        )
        self.assertTrue(any("execution model enum" in error for error in errors))

    def test_stance_contract_drift_fails(self) -> None:
        errors = self.mutated_errors(
            "SKILL.md",
            "DEALBREAKER: <observable condition>",
            "BLOCKER: <observable condition>",
        )
        self.assertTrue(any("STANCE contract" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
