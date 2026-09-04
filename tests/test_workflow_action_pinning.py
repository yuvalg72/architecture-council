from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate-repository.py"
SPEC = importlib.util.spec_from_file_location("validate_repository", VALIDATOR)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class WorkflowActionPinningTests(unittest.TestCase):
    def errors_for(self, target: str) -> list[str]:
        text = f"jobs:\n  test:\n    steps:\n      - uses: {target}\n"
        return MODULE.workflow_action_reference_errors(text, ".github/workflows/test.yml")

    def test_rejects_mutable_major_tag(self) -> None:
        self.assertTrue(self.errors_for("actions/checkout@v4"))

    def test_rejects_mutable_setup_python_major_tag(self) -> None:
        self.assertTrue(self.errors_for("actions/setup-python@v5"))

    def test_rejects_branch_ref(self) -> None:
        self.assertTrue(self.errors_for("vendor/action@main"))

    def test_rejects_short_sha(self) -> None:
        self.assertTrue(self.errors_for("vendor/action@abc1234"))

    def test_rejects_39_character_sha(self) -> None:
        self.assertTrue(self.errors_for("vendor/action@" + "a" * 39))

    def test_accepts_full_40_character_sha(self) -> None:
        self.assertEqual([], self.errors_for("vendor/action@" + "a" * 40))

    def test_accepts_local_action_path(self) -> None:
        self.assertEqual([], self.errors_for("./.github/actions/example"))

    def test_docker_reference_is_explicitly_outside_git_sha_rule(self) -> None:
        self.assertEqual([], self.errors_for("docker://alpine:3.20"))


if __name__ == "__main__":
    unittest.main()
