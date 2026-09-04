from __future__ import annotations

import hashlib
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


class PublicRepositoryHygieneTests(unittest.TestCase):
    def test_skill_security_boundary_is_organization_neutral(self) -> None:
        skill_text = (ROOT / "skills" / "architecture-council" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn(validator.GENERIC_SECURITY_BOUNDARY, skill_text)

    def test_hashed_identifier_guard_detects_a_configured_token(self) -> None:
        original = validator.PUBLIC_IDENTIFIER_TOKEN_HASHES
        fake_token = "ExampleInternalOrganization"
        fake_hash = hashlib.sha256(fake_token.lower().encode("utf-8")).hexdigest()
        validator.PUBLIC_IDENTIFIER_TOKEN_HASHES = {fake_hash}
        try:
            errors = validator.public_hygiene_errors(
                f"This text mentions {fake_token} directly.",
                "sample.md",
            )
        finally:
            validator.PUBLIC_IDENTIFIER_TOKEN_HASHES = original
        self.assertTrue(any("organization-specific public identifier" in error for error in errors))

    def test_generic_public_text_passes_identifier_guard(self) -> None:
        errors = validator.public_hygiene_errors(
            "Use approved environments for organizational or customer-sensitive information.",
            "sample.md",
        )
        self.assertEqual([], errors)


if __name__ == "__main__":
    unittest.main()
