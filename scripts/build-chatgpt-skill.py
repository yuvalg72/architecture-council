#!/usr/bin/env python3
"""Validate and package the native ChatGPT Architecture Council Skill."""

from __future__ import annotations

import argparse
import hashlib
import subprocess
import sys
import zipfile
from pathlib import Path

EXCLUDED_PARTS = {"__pycache__", ".DS_Store"}


def run(command: list[str], cwd: Path) -> None:
    result = subprocess.run(command, cwd=cwd, check=False, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"command failed with exit code {result.returncode}: {' '.join(command)}")


def should_include(path: Path) -> bool:
    return not any(part in EXCLUDED_PARTS or part.endswith(".pyc") for part in path.parts)


def build(repo_root: Path, output: Path) -> tuple[Path, str]:
    skill_root = repo_root / "skills" / "architecture-council"
    if not skill_root.is_dir():
        raise FileNotFoundError(f"Skill directory not found: {skill_root}")

    run([sys.executable, str(skill_root / "scripts" / "validate_skill_bundle.py"), str(skill_root)], repo_root)
    run([sys.executable, str(skill_root / "tests" / "test_validators.py")], repo_root)

    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists():
        output.unlink()

    files = sorted(path for path in skill_root.rglob("*") if path.is_file() and should_include(path.relative_to(skill_root)))
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in files:
            relative = path.relative_to(skill_root)
            info = zipfile.ZipInfo.from_file(path, arcname=str(Path("architecture-council") / relative))
            info.date_time = (2026, 7, 29, 0, 0, 0)
            info.create_system = 3
            info.external_attr = 0o644 << 16
            archive.writestr(info, path.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)

    with zipfile.ZipFile(output) as archive:
        names = set(archive.namelist())
        required = {
            "architecture-council/SKILL.md",
            "architecture-council/agents/openai.yaml",
            "architecture-council/VERSION",
        }
        missing = required - names
        if missing:
            raise RuntimeError(f"archive is missing required files: {sorted(missing)}")
        if any("__pycache__" in name or name.endswith(".pyc") for name in names):
            raise RuntimeError("archive contains generated cache files")

    digest = hashlib.sha256(output.read_bytes()).hexdigest()
    return output, digest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()
    output = args.output.resolve() if args.output else repo_root / "dist" / "skill.zip"

    try:
        archive, digest = build(repo_root, output)
    except (FileNotFoundError, RuntimeError, OSError, zipfile.BadZipFile) as exc:
        print(f"ChatGPT Skill build failed: {exc}", file=sys.stderr)
        return 1

    print(f"ChatGPT Skill package: {archive}")
    print(f"SHA256: {digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
