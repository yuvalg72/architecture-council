from __future__ import annotations

import importlib.util
import json
import tempfile
from pathlib import Path

import cairosvg
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "validate_assets.py"
SPEC = importlib.util.spec_from_file_location("validate_assets", MODULE_PATH)
assert SPEC and SPEC.loader
validate_assets = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validate_assets)


def write_manifest(root: Path, *, max_mae: float = 0.02) -> None:
    (root / ".github").mkdir(parents=True, exist_ok=True)
    data = {
        "version": 1,
        "assets": [
            {
                "id": "icon",
                "published": "assets/icon.png",
                "kind": "vector",
                "source": "assets/icon.svg",
                "expected_width": 64,
                "expected_height": 64,
                "display_width": 32,
                "minimum_scale_factor": 2.0,
                "allow_edge_contact": True,
                "max_normalized_mae": max_mae,
            }
        ],
    }
    (root / ".github" / "assets-manifest.json").write_text(
        json.dumps(data), encoding="utf-8"
    )


def write_svg(path: Path, fill: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" '
        f'viewBox="0 0 64 64"><rect width="64" height="64" fill="{fill}"/></svg>\n',
        encoding="utf-8",
    )


def render_svg(svg_path: Path, png_path: Path) -> None:
    png_path.parent.mkdir(parents=True, exist_ok=True)
    cairosvg.svg2png(
        url=str(svg_path),
        write_to=str(png_path),
        output_width=64,
        output_height=64,
    )


def test_broken_local_image_reference_fails() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        (root / "README.md").write_text(
            '<img src="assets/missing.png" alt="missing">\n',
            encoding="utf-8",
        )
        errors, _ = validate_assets.run(
            root, root / ".github" / "assets-manifest.json"
        )
        assert any("Broken local image reference" in error for error in errors)


def test_matching_svg_png_pair_passes() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        (root / "README.md").write_text(
            '<img src="assets/icon.png" alt="icon">\n',
            encoding="utf-8",
        )
        svg = root / "assets" / "icon.svg"
        png = root / "assets" / "icon.png"
        write_svg(svg, "#4D4D4D")
        render_svg(svg, png)
        write_manifest(root)

        errors, _ = validate_assets.run(
            root, root / ".github" / "assets-manifest.json"
        )
        assert errors == []


def test_deliberately_mismatched_svg_png_pair_fails() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        (root / "README.md").write_text(
            '<img src="assets/icon.png" alt="icon">\n',
            encoding="utf-8",
        )
        svg = root / "assets" / "icon.svg"
        png = root / "assets" / "icon.png"
        write_svg(svg, "#FFFFFF")
        png.parent.mkdir(parents=True, exist_ok=True)
        Image.new("RGBA", (64, 64), (0, 0, 0, 255)).save(png)
        write_manifest(root, max_mae=0.001)

        errors, _ = validate_assets.run(
            root, root / ".github" / "assets-manifest.json"
        )
        assert any("visual parity failed" in error for error in errors)


def test_template_and_fenced_examples_are_ignored() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        (root / "templates").mkdir(parents=True, exist_ok=True)
        (root / "templates" / "README.md").write_text(
            '<img src="assets/missing.png" alt="placeholder">\\n',
            encoding="utf-8",
        )
        (root / "README.md").write_text(
            '```markdown\\n<img src="assets/missing.png" alt="example">\\n```\\n',
            encoding="utf-8",
        )
        errors, _ = validate_assets.run(
            root, root / ".github" / "assets-manifest.json"
        )
        assert errors == []
