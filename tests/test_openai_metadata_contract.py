from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "architecture-council"
VALIDATOR = SKILL / "scripts" / "validate_openai_metadata.py"
SPEC = importlib.util.spec_from_file_location("validate_openai_metadata", VALIDATOR)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
BASE = (SKILL / "agents" / "openai.yaml").read_text(encoding="utf-8")


class OpenAIMetadataContractTests(unittest.TestCase):
    def errors(self, text: str) -> list[str]:
        return MODULE.validate_metadata(SKILL, text)

    def mutate(self, old: str, new: str) -> list[str]:
        self.assertIn(old, BASE)
        return self.errors(BASE.replace(old, new, 1))

    def test_current_metadata_passes(self) -> None:
        self.assertEqual([], self.errors(BASE))

    def test_missing_display_name_fails(self) -> None:
        errors = self.mutate("  display_name: Architecture Council\n", "")
        self.assertTrue(any("display_name" in error for error in errors))

    def test_empty_display_name_fails(self) -> None:
        errors = self.mutate("display_name: Architecture Council", "display_name: ''")
        self.assertTrue(any("display_name" in error for error in errors))

    def test_invalid_yaml_fails(self) -> None:
        errors = self.mutate("interface:\n", "interface\n")
        self.assertTrue(any("invalid YAML" in error for error in errors))

    def test_missing_icon_file_fails(self) -> None:
        errors = self.mutate("icon_small: ./assets/icon.svg", "icon_small: ./assets/missing.svg")
        self.assertTrue(any("missing file" in error for error in errors))

    def test_icon_path_traversal_fails(self) -> None:
        errors = self.mutate("icon_small: ./assets/icon.svg", "icon_small: ../README.md")
        self.assertTrue(any("escapes the Skill directory" in error for error in errors))

    def test_external_icon_url_fails(self) -> None:
        errors = self.mutate("icon_small: ./assets/icon.svg", "icon_small: https://example.com/icon.svg")
        self.assertTrue(any("local path" in error for error in errors))

    def test_invalid_brand_color_fails(self) -> None:
        errors = self.mutate("brand_color: '#0B1630'", "brand_color: navy")
        self.assertTrue(any("#RRGGBB" in error for error in errors))

    def test_shorthand_brand_color_fails(self) -> None:
        errors = self.mutate("brand_color: '#0B1630'", "brand_color: '#FFF'")
        self.assertTrue(any("#RRGGBB" in error for error in errors))

    def test_default_prompt_without_skill_token_fails(self) -> None:
        errors = self.mutate("$architecture-council", "Architecture Council")
        self.assertTrue(any("default_prompt" in error for error in errors))

    def test_products_scalar_fails(self) -> None:
        errors = self.mutate("  products:\n  - chatgpt\n", "  products: chatgpt\n")
        self.assertTrue(any("policy.products must be a list" in error for error in errors))

    def test_unsupported_product_fails(self) -> None:
        errors = self.mutate("  - chatgpt\n", "  - chatgpt\n  - unsupported-host\n")
        self.assertTrue(any("unsupported values" in error for error in errors))

    def test_duplicate_product_fails(self) -> None:
        errors = self.mutate("  - chatgpt\n", "  - chatgpt\n  - chatgpt\n")
        self.assertTrue(any("duplicate values" in error for error in errors))

    def test_string_boolean_fails(self) -> None:
        errors = self.mutate("allow_implicit_invocation: true", "allow_implicit_invocation: \"true\"")
        self.assertTrue(any("must be a boolean" in error for error in errors))

    def test_actual_boolean_true_passes(self) -> None:
        self.assertEqual([], self.errors(BASE))

    def test_placeholder_description_fails(self) -> None:
        errors = self.mutate(
            "Run structured executive and architecture deliberation for high-stakes decisions.",
            "TODO placeholder description for Architecture Council.",
        )
        self.assertTrue(any("placeholder" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
