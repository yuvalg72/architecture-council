#!/usr/bin/env python3
"""Validate the Architecture Council repository and native ChatGPT Skill."""
from __future__ import annotations

import ast
import hashlib
import re
import sys
import xml.etree.ElementTree as ET
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
    "scripts/generate-documentation-images.py",
    ".github/FUNDING.yml",
    ".github/ISSUE_TEMPLATE/provider_support.md",
    ".github/workflows/star-chart.yml",
    ".github/workflows/export-audit-snapshot.yml",
    ".github/workflows/generate-doc-images.yml",
    "skills/architecture-council/assets/architecture-council-overview.jpg",
    "skills/architecture-council/assets/professional-review-panel.jpg",
    "skills/architecture-council/assets/council-process.jpg",
    "skills/architecture-council/assets/evidence-and-decision-model.jpg",
    "skills/architecture-council/assets/outcome-tracking.jpg",
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
# Hashes represent non-product organization identifiers that must not be
# republished in this generic public repository. Storing hashes avoids
# embedding the identifiers themselves in the validation source.
PUBLIC_IDENTIFIER_TOKEN_HASHES = {
    "0590d85677f54b835b864e958a1e077f4d2648c3f669733f0be75de5c9216bfa",
}
PUBLIC_IDENTIFIER_TOKEN_RE = re.compile(r"[A-Za-z][A-Za-z0-9_-]*")
GENERIC_SECURITY_BOUNDARY = (
    "For organizational, customer, configuration, commercial, contractual, "
    "security, or other sensitive information:"
)
SVG_PATHS = (
    "skills/architecture-council/assets/icon.svg",
    "skills/architecture-council/assets/hero-council-3d.svg",
    "skills/architecture-council/assets/review-panel-3d.svg",
    "skills/architecture-council/assets/decision-flow-3d.svg",
    "skills/architecture-council/assets/evidence-model-3d.svg",
    "skills/architecture-council/assets/outcome-loop-3d.svg",
    "skills/architecture-council/assets/social-preview.svg",
)
SKILL_README_HEADINGS = (
    "## What this Skill does",
    "## Use this Skill when",
    "## Core capabilities",
    "## Typical workflow",
    "## Expected output",
    "## Guardrails and boundaries",
    "## Example prompts",
    "## Related Skills",
    "## Skill files",
    "## Repository navigation",
)


def svg_viewbox(path: Path) -> tuple[float, float] | None:
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError:
        return None
    viewbox = root.attrib.get("viewBox", "").strip().split()
    if len(viewbox) != 4:
        return None
    try:
        width = float(viewbox[2])
        height = float(viewbox[3])
    except ValueError:
        return None
    if width <= 0 or height <= 0:
        return None
    return width, height


def image_targets(markdown: str) -> set[str]:
    targets = set(re.findall(r"!\[[^]]*\]\(([^)]+)\)", markdown))
    targets.update(re.findall(r"<img\b[^>]*\bsrc=[\"']([^\"']+)[\"']", markdown, flags=re.IGNORECASE))
    return targets


def public_hygiene_errors(text: str, rel: str) -> list[str]:
    errors: list[str] = []
    for token in PUBLIC_IDENTIFIER_TOKEN_RE.findall(text):
        digest = hashlib.sha256(token.lower().encode("utf-8")).hexdigest()
        if digest in PUBLIC_IDENTIFIER_TOKEN_HASHES:
            errors.append(f"organization-specific public identifier found in {rel}")
            break
    return errors


def validate_local_images(errors: list[str], markdown_path: Path) -> None:
    text = markdown_path.read_text(encoding="utf-8")
    for target in sorted(image_targets(text)):
        if target.startswith(("http://", "https://", "data:")):
            continue
        resolved = (markdown_path.parent / target).resolve()
        try:
            resolved.relative_to(ROOT.resolve())
        except ValueError:
            errors.append(f"image reference escapes repository: {markdown_path.relative_to(ROOT)} -> {target}")
            continue
        if not resolved.is_file():
            errors.append(f"README references missing image: {markdown_path.relative_to(ROOT)} -> {target}")


def skill_readme_contract_errors(text: str, skill_dir: Path = SKILL) -> list[str]:
    errors: list[str] = []
    for heading in SKILL_README_HEADINGS:
        if heading not in text:
            errors.append(f"Skill README missing required heading: {heading}")
    if "assets/icon.svg" not in text:
        errors.append("Skill README must reference assets/icon.svg")
    if "@architecture-council" not in text:
        errors.append("Skill README must include an exact @architecture-council invocation example")
    if "SKILL.md" not in text or "authoritative control-plane" not in text:
        errors.append("Skill README must distinguish human-facing documentation from authoritative SKILL.md behavior")
    if re.search(r"\b(?:TODO|TBD)\b", text, flags=re.IGNORECASE):
        errors.append("Skill README contains placeholder text")
    if len(text.strip()) < 2500:
        errors.append("Skill README is too short to function as a substantive landing page")

    related = re.search(r"## Related Skills\n(?P<body>.*?)(?:\n## |\Z)", text, flags=re.DOTALL)
    if related:
        for target in re.findall(r"\[[^]]+\]\(([^)]+)\)", related.group("body")):
            if target.startswith(("http://", "https://", "#")):
                continue
            resolved = (skill_dir / target).resolve()
            try:
                resolved.relative_to(ROOT.resolve())
            except ValueError:
                errors.append(f"Skill README related-Skill link escapes repository: {target}")
                continue
            if not resolved.exists():
                errors.append(f"Skill README related-Skill link does not resolve: {target}")
    return errors


def validate_skill_readme(errors: list[str]) -> None:
    path = SKILL / "README.md"
    if not path.is_file():
        errors.append("missing required Skill landing page: skills/architecture-council/README.md")
        return
    errors.extend(skill_readme_contract_errors(path.read_text(encoding="utf-8"), SKILL))


def main() -> int:
    errors: list[str] = []
    for rel in sorted(FORBIDDEN_PATHS):
        if (ROOT / rel).exists():
            errors.append(f"obsolete path remains: {rel}")

    version = (SKILL / "VERSION").read_text(encoding="utf-8").strip()
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        errors.append("VERSION must contain a semantic version")
    for rel in (
        "README.md",
        "CHATGPT.md",
        "CHANGELOG.md",
        "skills/architecture-council/README.md",
        "skills/architecture-council/CHANGELOG.md",
    ):
        path = ROOT / rel
        if not path.is_file():
            errors.append(f"missing version-bearing file: {rel}")
            continue
        text = path.read_text(encoding="utf-8")
        if version and version not in text:
            errors.append(f"version {version} missing from {rel}")

    skill_text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    if GENERIC_SECURITY_BOUNDARY not in skill_text:
        errors.append("SKILL.md security boundary must remain organization-neutral")

    digests: dict[str, str] = {}
    for rel in SVG_PATHS:
        path = ROOT / rel
        if not path.is_file():
            errors.append(f"missing SVG asset: {rel}")
            continue
        dims = svg_viewbox(path)
        if dims is None:
            errors.append(f"invalid SVG viewBox or XML: {rel}")
            continue
        width, height = dims
        if rel.endswith("icon.svg"):
            if width < 256 or height < 256:
                errors.append(f"icon SVG is too small: {rel} ({width:g}x{height:g})")
        elif width < 1000 or height < 500:
            errors.append(f"documentation SVG is too small: {rel} ({width:g}x{height:g})")

        text = path.read_text(encoding="utf-8")
        lowered = text.lower()
        if "<script" in lowered or "<foreignobject" in lowered:
            errors.append(f"unsafe or non-portable SVG element found: {rel}")
        if re.search(r"(?:href|xlink:href)=[\"']https?://", text, flags=re.IGNORECASE):
            errors.append(f"external SVG dependency found: {rel}")
        if "role=\"img\"" not in text or "<title" not in text or "<desc" not in text:
            errors.append(f"SVG accessibility metadata missing: {rel}")

        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest in digests:
            errors.append(f"duplicate SVG content: {rel} and {digests[digest]}")
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
            errors.extend(public_hygiene_errors(text, rel))
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

    validate_local_images(errors, ROOT / "README.md")
    validate_local_images(errors, SKILL / "README.md")
    validate_skill_readme(errors)

    required = {
        "README.md",
        "CONTRIBUTING.md",
        "SECURITY.md",
        "CHATGPT.md",
        "CHANGELOG.md",
        "LICENSE",
        "docs/visual-system.md",
        "scripts/build-chatgpt-skill.py",
        "scripts/validate-repository.py",
        "skills/architecture-council/README.md",
        "skills/architecture-council/SKILL.md",
        "skills/architecture-council/agents/openai.yaml",
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
