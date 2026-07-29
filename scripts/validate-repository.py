#!/usr/bin/env python3
"""Validate the Architecture Council repository and native ChatGPT Skill."""
from __future__ import annotations

import ast
import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "architecture-council"

FORBIDDEN_PATHS = {
    ".claude-plugin",
    "configs",
    "install.sh",
    "scripts/convert-agents-opencode.py",
    "scripts/council-simulation-checklist.sh",
    "scripts/detect-providers.sh",
    "scripts/gen-star-history.py",
    ".github/FUNDING.yml",
    ".github/ISSUE_TEMPLATE/provider_support.md",
    ".github/workflows/star-chart.yml",
    ".github/workflows/export-audit-snapshot.yml",
}
FORBIDDEN_TERMS = (
    "Council" + " of High Intelligence",
    "0x" + "Nyk",
    "Claude" + " Code",
    "Gemini" + " CLI",
    "Ol" + "lama",
    "Open" + "Code",
    "historical" + " persona",
    "historical" + "-persona",
    "18 AI" + " personas",
    "multi" + "-persona",
)
SECRET_PATTERNS = (
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
)
IMAGE_PATHS = (
    "skills/architecture-council/assets/architecture-council-overview.jpg",
    "skills/architecture-council/assets/professional-review-panel.jpg",
    "skills/architecture-council/assets/council-process.jpg",
    "skills/architecture-council/assets/evidence-and-decision-model.jpg",
    "skills/architecture-council/assets/outcome-tracking.jpg",
)

def jpeg_dimensions(data: bytes) -> tuple[int, int] | None:
    if len(data) < 4 or data[:2] != b"\xff\xd8" or data[-2:] != b"\xff\xd9":
        return None
    i = 2
    while i + 9 < len(data):
        if data[i] != 0xFF:
            i += 1
            continue
        marker = data[i + 1]
        i += 2
        if marker in {0xD8, 0xD9}:
            continue
        if i + 2 > len(data):
            return None
        length = int.from_bytes(data[i:i+2], "big")
        if length < 2 or i + length > len(data):
            return None
        if marker in {0xC0,0xC1,0xC2,0xC3,0xC5,0xC6,0xC7,0xC9,0xCA,0xCB,0xCD,0xCE,0xCF}:
            if length < 7:
                return None
            height = int.from_bytes(data[i+3:i+5], "big")
            width = int.from_bytes(data[i+5:i+7], "big")
            return width, height
        i += length
    return None

def main() -> int:
    errors: list[str] = []
    for rel in sorted(FORBIDDEN_PATHS):
        if (ROOT / rel).exists():
            errors.append(f"obsolete path remains: {rel}")

    versions = {
        "VERSION": (SKILL / "VERSION").read_text(encoding="utf-8").strip(),
    }
    for rel in ("README.md", "CHATGPT.md", "CHANGELOG.md", "skills/architecture-council/CHANGELOG.md"):
        text = (ROOT / rel).read_text(encoding="utf-8")
        match = re.search(r"1\.0\.2", text)
        if not match:
            errors.append(f"version 1.0.2 missing from {rel}")
    if versions["VERSION"] != "1.0.2":
        errors.append("VERSION must be 1.0.2")

    digests: dict[str, str] = {}
    for rel in IMAGE_PATHS:
        path = ROOT / rel
        if not path.is_file():
            errors.append(f"missing JPEG asset: {rel}")
            continue
        data = path.read_bytes()
        dims = jpeg_dimensions(data)
        if dims is None:
            errors.append(f"invalid JPEG asset: {rel}")
            continue
        width, height = dims
        if width < 500 or height < 300:
            errors.append(f"JPEG asset is too small: {rel} ({width}x{height})")
        if len(data) < 50000:
            errors.append(f"JPEG asset appears incomplete: {rel} ({len(data)} bytes)")
        digest = hashlib.sha256(data).hexdigest()
        if digest in digests:
            errors.append(f"duplicate JPEG content: {rel} and {digests[digest]}")
        digests[digest] = rel

    text_suffixes = {".md", ".py", ".yaml", ".yml", ".json", ".txt", ".svg", ".sh"}
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        rel = path.relative_to(ROOT).as_posix()
        if path.suffix.lower() in text_suffixes or path.name in {"LICENSE", "VERSION"}:
            text = path.read_text(encoding="utf-8")
            if "\u2014" in text:
                errors.append(f"em dash found in {rel}")
            if rel not in {"LICENSE", "skills/architecture-council/LICENSES/council-of-high-intelligence-MIT.txt", "scripts/validate-repository.py"}:
                for term in FORBIDDEN_TERMS:
                    if term.lower() in text.lower():
                        errors.append(f"stale source-project term found in {rel}: {term}")
            for pattern in SECRET_PATTERNS:
                if pattern.search(text):
                    errors.append(f"possible secret detected in {rel}")
            if path.suffix == ".py":
                try:
                    ast.parse(text, filename=rel)
                except SyntaxError as exc:
                    errors.append(f"Python syntax error in {rel}: {exc}")

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for target in re.findall(r"!\[[^]]*\]\(([^)]+)\)", readme):
        if not (ROOT / target).is_file():
            errors.append(f"README references missing image: {target}")

    required = {
        "README.md", "CONTRIBUTING.md", "SECURITY.md", "CHATGPT.md", "CHANGELOG.md", "LICENSE",
        "scripts/build-chatgpt-skill.py", "scripts/validate-repository.py",
        "skills/architecture-council/SKILL.md", "skills/architecture-council/agents/openai.yaml",
    }
    for rel in sorted(required):
        if not (ROOT / rel).is_file():
            errors.append(f"missing required repository file: {rel}")

    if errors:
        print("Repository validation failed:", file=sys.stderr)
        for error in sorted(set(errors)):
            print(f"- {error}", file=sys.stderr)
        return 1
    print("Repository validation passed.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
