from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = ROOT / "scripts" / "validate-repository.py"

spec = importlib.util.spec_from_file_location("repository_validator", VALIDATOR_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError("Unable to load repository validator")
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class SkillLandingPageContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.readme = (ROOT / "skills" / "architecture-council" / "README.md").read_text(encoding="utf-8")

    def test_current_skill_readme_satisfies_contract(self) -> None:
        self.assertEqual([], validator.skill_readme_contract_errors(self.readme))

    def test_missing_related_skills_heading_fails(self) -> None:
        mutated = self.readme.replace("## Related Skills", "## Local ecosystem", 1)
        errors = validator.skill_readme_contract_errors(mutated)
        self.assertTrue(any("Related Skills" in error for error in errors))

    def test_unknown_related_skill_link_fails(self) -> None:
        mutated = self.readme.replace(
            "This repository contains one authoritative Skill, so there is no sibling Skill to link locally. Do not invent a related Skill merely to fill this section.",
            "See [Ghost Skill](../ghost-skill/README.md).",
            1,
        )
        errors = validator.skill_readme_contract_errors(mutated)
        self.assertTrue(any("does not resolve" in error for error in errors))

    def test_exact_invocation_example_is_required(self) -> None:
        mutated = self.readme.replace("@architecture-council", "architecture-council")
        errors = validator.skill_readme_contract_errors(mutated)
        self.assertTrue(any("exact @architecture-council" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
