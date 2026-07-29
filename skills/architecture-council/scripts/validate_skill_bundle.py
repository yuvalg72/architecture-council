#!/usr/bin/env python3
"""Validate the Architecture Council Skill bundle."""

from __future__ import annotations

import argparse
import ast
import hashlib
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

REQUIRED_FILES = {
    "SKILL.md",
    "VERSION",
    "CHANGELOG.md",
    "NOTICE.md",
    "agents/openai.yaml",
    "assets/icon.svg",
    "assets/architecture-council-overview.jpg",
    "assets/professional-review-panel.jpg",
    "assets/council-process.jpg",
    "assets/evidence-and-decision-model.jpg",
    "assets/outcome-tracking.jpg",
    "LICENSES/council-of-high-intelligence-MIT.txt",
    "references/council-protocol.md",
    "references/reviewer-roles.md",
    "references/routing-and-modes.md",
    "references/decision-dossier.md",
    "references/output-contract.md",
    "references/security-and-provider-policy.md",
    "references/outcome-tracking.md",
    "references/lessons-learned-integration.md",
    "references/examples.md",
    "scripts/validate_decision_dossier.py",
    "scripts/validate_decision_record.py",
    "scripts/validate_skill_bundle.py",
    "tests/test_validators.py",
}
PLACEHOLDER_MARKERS = ("TO" + "DO", "example_" + "asset", "api_" + "reference.md")
JPEG_FILES = (
    "assets/architecture-council-overview.jpg",
    "assets/professional-review-panel.jpg",
    "assets/council-process.jpg",
    "assets/evidence-and-decision-model.jpg",
    "assets/outcome-tracking.jpg",
)
SECRET_PATTERNS = [
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
]


def jpeg_dimensions(data: bytes) -> tuple[int, int] | None:
    if len(data) < 4 or data[:2] != b"\xff\xd8" or data[-2:] != b"\xff\xd9":
        return None
    index = 2
    while index + 9 < len(data):
        if data[index] != 0xFF:
            index += 1
            continue
        marker = data[index + 1]
        index += 2
        if marker in {0xD8, 0xD9}:
            continue
        if index + 2 > len(data):
            return None
        length = int.from_bytes(data[index:index + 2], "big")
        if length < 2 or index + length > len(data):
            return None
        if marker in {0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF}:
            if length < 7:
                return None
            height = int.from_bytes(data[index + 3:index + 5], "big")
            width = int.from_bytes(data[index + 5:index + 7], "big")
            return width, height
        index += length
    return None


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        raise ValueError("SKILL.md must start with YAML frontmatter")
    end = text.find("\n---\n", 4)
    if end == -1:
        raise ValueError("SKILL.md frontmatter is not closed")
    raw = text[4:end]
    fields: dict[str, str] = {}
    for line in raw.splitlines():
        if not line.strip():
            continue
        if ":" not in line:
            raise ValueError(f"invalid frontmatter line: {line}")
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip().strip('"')
    return fields, text[end + 5:]


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    root = root.resolve()

    for relative in sorted(REQUIRED_FILES):
        if not (root / relative).is_file():
            errors.append(f"missing required file: {relative}")

    if root.name != "architecture-council":
        errors.append("Skill folder must be named architecture-council")

    skill_path = root / "SKILL.md"
    if skill_path.exists():
        text = skill_path.read_text(encoding="utf-8")
        try:
            frontmatter, body = parse_frontmatter(text)
            if set(frontmatter) != {"name", "description"}:
                errors.append("SKILL.md frontmatter must contain only name and description")
            if frontmatter.get("name") != "architecture-council":
                errors.append("SKILL.md name must be architecture-council")
            description = frontmatter.get("description", "")
            if len(description) < 180:
                errors.append("SKILL.md description is too short to provide reliable triggering context")
            for trigger in ("architecture council", "duo", "full council", "high-stakes"):
                if trigger.lower() not in description.lower():
                    errors.append(f"SKILL.md description missing trigger context: {trigger}")
            if len(text.splitlines()) > 500:
                errors.append("SKILL.md exceeds 500 lines")
            if any(marker in body for marker in PLACEHOLDER_MARKERS):
                errors.append("SKILL.md contains placeholder text")
        except ValueError as exc:
            errors.append(str(exc))

    version_path = root / "VERSION"
    if version_path.exists():
        version = version_path.read_text(encoding="utf-8").strip()
        if not re.fullmatch(r"\d+\.\d+\.\d+", version):
            errors.append("VERSION must contain a semantic version")

    yaml_path = root / "agents" / "openai.yaml"
    if yaml_path.exists():
        yaml_text = yaml_path.read_text(encoding="utf-8")
        for required in ("display_name:", "short_description:", "products:", "allow_implicit_invocation:"):
            if required not in yaml_text:
                errors.append(f"agents/openai.yaml missing {required}")

    icon_path = root / "assets" / "icon.svg"
    if icon_path.exists():
        try:
            ET.parse(icon_path)
        except ET.ParseError as exc:
            errors.append(f"invalid SVG icon: {exc}")

    image_digests: dict[str, str] = {}
    for relative in JPEG_FILES:
        path = root / relative
        if not path.is_file():
            continue
        data = path.read_bytes()
        dimensions = jpeg_dimensions(data)
        if dimensions is None:
            errors.append(f"invalid JPEG asset: {relative}")
            continue
        width, height = dimensions
        if width < 500 or height < 300:
            errors.append(f"JPEG asset is too small: {relative} ({width}x{height})")
        if len(data) < 50000:
            errors.append(f"JPEG asset appears incomplete: {relative} ({len(data)} bytes)")
        digest = hashlib.sha256(data).hexdigest()
        if digest in image_digests:
            errors.append(f"duplicate JPEG content: {relative} and {image_digests[digest]}")
        image_digests[digest] = relative

    forbidden_terms = (
        "Council" + " of High Intelligence",
        "Aristotle",
        "Socrates",
        "Sun Tzu",
        "Machiavelli",
        "Feynman",
        "Torvalds",
        "Lao Tzu",
    )
    total_size = 0
    for path in root.rglob("*"):
        if path.is_symlink():
            errors.append(f"symlinks are not allowed in packaged Skill: {path.relative_to(root)}")
            continue
        if not path.is_file():
            continue
        relative = path.relative_to(root)
        total_size += path.stat().st_size
        if path.stat().st_size > 5 * 1024 * 1024:
            errors.append(f"file exceeds 5 MB: {relative}")
        if path.suffix.lower() in {".md", ".py", ".yaml", ".yml", ".json", ".txt", ".svg"}:
            text = path.read_text(encoding="utf-8")
            if path.suffix.lower() == ".md":
                for term in forbidden_terms:
                    if term in text and path.name != "council-of-high-intelligence-MIT.txt":
                        errors.append(f"legacy source-project term found in {relative}: {term}")
            if "\u2014" in text:
                errors.append(f"em dash found in {relative}")
            if any(marker in text for marker in PLACEHOLDER_MARKERS):
                errors.append(f"placeholder content found in {relative}")
            for pattern in SECRET_PATTERNS:
                if pattern.search(text):
                    errors.append(f"possible secret detected in {relative}")
            if path.suffix == ".py":
                try:
                    ast.parse(text, filename=str(relative))
                except SyntaxError as exc:
                    errors.append(f"Python syntax error in {relative}: {exc}")

    if total_size > 25 * 1024 * 1024:
        errors.append("Skill package exceeds 25 MB")

    if skill_path.exists():
        skill_text = skill_path.read_text(encoding="utf-8")
        for match in re.finditer(r"`((?:references|scripts)/[^`]+)`", skill_text):
            target = root / match.group(1)
            if not target.exists():
                errors.append(f"SKILL.md references missing file: {match.group(1)}")

    return sorted(set(errors))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    errors = validate(args.root)
    if errors:
        print("Skill bundle validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(f"Skill bundle is valid: {args.root.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
