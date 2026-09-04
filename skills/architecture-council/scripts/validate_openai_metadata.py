#!/usr/bin/env python3
"""Validate Architecture Council ChatGPT interface metadata.

The parser intentionally supports the small YAML subset used by `agents/openai.yaml`:
plain or quoted scalars, booleans, nested mappings, and scalar lists. Unsupported
YAML features fail closed instead of being guessed. Unknown metadata keys are
allowed for forward compatibility, while the repository's known contract is
validated strictly.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

ALLOWED_PRODUCTS = {"chatgpt"}
HEX_COLOR_RE = re.compile(r"#[0-9A-Fa-f]{6}")
PLACEHOLDER_RE = re.compile(r"\b(?:TODO|TBD|placeholder)\b", flags=re.IGNORECASE)


class MetadataParseError(ValueError):
    pass


def parse_scalar(raw: str, lineno: int) -> Any:
    value = raw.strip()
    if not value:
        return ""
    if value in {"true", "false"}:
        return value == "true"
    if value.startswith("'"):
        if len(value) < 2 or not value.endswith("'"):
            raise MetadataParseError(f"line {lineno}: unterminated single-quoted scalar")
        return value[1:-1].replace("''", "'")
    if value.startswith('"'):
        try:
            parsed = json.loads(value)
        except json.JSONDecodeError as exc:
            raise MetadataParseError(f"line {lineno}: invalid double-quoted scalar: {exc.msg}") from exc
        if not isinstance(parsed, str):
            raise MetadataParseError(f"line {lineno}: quoted scalar must decode to a string")
        return parsed
    if value.startswith(("[", "{", "&", "*", "!", "|", ">")):
        raise MetadataParseError(f"line {lineno}: unsupported YAML construct")
    return value


def parse_metadata_yaml(text: str) -> dict[str, Any]:
    data: dict[str, Any] = {}
    section: str | None = None
    pending_list: str | None = None

    for lineno, raw_line in enumerate(text.splitlines(), start=1):
        if "\t" in raw_line:
            raise MetadataParseError(f"line {lineno}: tabs are not allowed")
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue

        indent = len(raw_line) - len(raw_line.lstrip(" "))
        stripped = raw_line.strip()

        if indent == 0:
            if not stripped.endswith(":") or stripped.count(":") != 1:
                raise MetadataParseError(f"line {lineno}: expected top-level mapping key")
            section = stripped[:-1].strip()
            if not section:
                raise MetadataParseError(f"line {lineno}: empty top-level key")
            if section in data:
                raise MetadataParseError(f"line {lineno}: duplicate top-level key: {section}")
            data[section] = {}
            pending_list = None
            continue

        if section is None:
            raise MetadataParseError(f"line {lineno}: nested value appears before a top-level section")
        if indent not in {2, 4}:
            raise MetadataParseError(f"line {lineno}: unsupported indentation level {indent}")

        if stripped.startswith("- "):
            if pending_list is None:
                raise MetadataParseError(f"line {lineno}: list item has no parent key")
            item = parse_scalar(stripped[2:], lineno)
            data[section][pending_list].append(item)
            continue

        if indent != 2 or ":" not in stripped:
            raise MetadataParseError(f"line {lineno}: expected nested mapping key")
        key, raw_value = stripped.split(":", 1)
        key = key.strip()
        if not key:
            raise MetadataParseError(f"line {lineno}: empty nested key")
        if key in data[section]:
            raise MetadataParseError(f"line {lineno}: duplicate key in {section}: {key}")
        if raw_value.strip():
            data[section][key] = parse_scalar(raw_value, lineno)
            pending_list = None
        else:
            data[section][key] = []
            pending_list = key

    return data


def nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate_icon_path(root: Path, value: Any, field: str) -> list[str]:
    errors: list[str] = []
    if not nonempty_string(value):
        return [f"agents/openai.yaml: interface.{field} must be a non-empty local path"]
    if re.match(r"^[A-Za-z][A-Za-z0-9+.-]*://", value):
        return [f"agents/openai.yaml: interface.{field} must be a local path, not a URL"]
    path = Path(value)
    if path.is_absolute():
        return [f"agents/openai.yaml: interface.{field} must be relative"]
    candidate = (root / path).resolve()
    try:
        candidate.relative_to(root.resolve())
    except ValueError:
        return [f"agents/openai.yaml: interface.{field} escapes the Skill directory"]
    if not candidate.is_file():
        errors.append(f"agents/openai.yaml: interface.{field} points to missing file {value}")
    if candidate.is_symlink():
        errors.append(f"agents/openai.yaml: interface.{field} must not reference a symlink")
    return errors


def validate_metadata(root: Path, text: str | None = None) -> list[str]:
    root = root.resolve()
    yaml_path = root / "agents" / "openai.yaml"
    if text is None:
        try:
            text = yaml_path.read_text(encoding="utf-8")
        except FileNotFoundError:
            return ["agents/openai.yaml: file is missing"]

    try:
        data = parse_metadata_yaml(text)
    except MetadataParseError as exc:
        return [f"agents/openai.yaml: invalid YAML: {exc}"]

    errors: list[str] = []
    interface = data.get("interface")
    policy = data.get("policy")
    if not isinstance(interface, dict):
        errors.append("agents/openai.yaml: interface must be a mapping")
        interface = {}
    if not isinstance(policy, dict):
        errors.append("agents/openai.yaml: policy must be a mapping")
        policy = {}

    display_name = interface.get("display_name")
    if not nonempty_string(display_name):
        errors.append("agents/openai.yaml: interface.display_name must be a non-empty string")
    elif display_name.strip() != "Architecture Council":
        errors.append("agents/openai.yaml: interface.display_name must be Architecture Council")

    short_description = interface.get("short_description")
    if not nonempty_string(short_description) or len(short_description.strip()) < 20:
        errors.append("agents/openai.yaml: interface.short_description must be a substantive non-empty string")
    elif PLACEHOLDER_RE.search(short_description):
        errors.append("agents/openai.yaml: interface.short_description contains placeholder text")

    errors.extend(validate_icon_path(root, interface.get("icon_small"), "icon_small"))
    errors.extend(validate_icon_path(root, interface.get("icon_large"), "icon_large"))

    brand_color = interface.get("brand_color")
    if not isinstance(brand_color, str) or not HEX_COLOR_RE.fullmatch(brand_color):
        errors.append("agents/openai.yaml: interface.brand_color must match #RRGGBB")

    default_prompt = interface.get("default_prompt")
    if not nonempty_string(default_prompt):
        errors.append("agents/openai.yaml: interface.default_prompt must be a non-empty string")
    else:
        if "$architecture-council" not in default_prompt:
            errors.append("agents/openai.yaml: interface.default_prompt must reference $architecture-council")
        if PLACEHOLDER_RE.search(default_prompt):
            errors.append("agents/openai.yaml: interface.default_prompt contains placeholder text")

    products = policy.get("products")
    if not isinstance(products, list):
        errors.append("agents/openai.yaml: policy.products must be a list")
    else:
        if not products:
            errors.append("agents/openai.yaml: policy.products must not be empty")
        elif not all(nonempty_string(item) for item in products):
            errors.append("agents/openai.yaml: policy.products entries must be non-empty strings")
        else:
            if len(products) != len(set(products)):
                errors.append("agents/openai.yaml: policy.products contains duplicate values")
            unsupported = sorted(set(products) - ALLOWED_PRODUCTS)
            if unsupported:
                errors.append(f"agents/openai.yaml: policy.products contains unsupported values: {unsupported}")

    implicit = policy.get("allow_implicit_invocation")
    if not isinstance(implicit, bool):
        errors.append("agents/openai.yaml: policy.allow_implicit_invocation must be a boolean")

    return sorted(set(errors))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    errors = validate_metadata(args.root)
    if errors:
        print("OpenAI metadata validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("OpenAI metadata validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
