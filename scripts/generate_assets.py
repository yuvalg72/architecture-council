#!/usr/bin/env python3
"""Generate GitHub-facing PNG assets from canonical Architecture Council SVG sources."""
from __future__ import annotations

from pathlib import Path

import cairosvg
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
ASSET_DIR = ROOT / "skills" / "architecture-council" / "assets"

ASSETS = (
    ("icon", ASSET_DIR / "icon.svg", 256, 256, 48),
    ("hero-council-3d", ASSET_DIR / "source" / "hero-council-3d.svg", 1600, 900, 64),
    ("review-panel-3d", ASSET_DIR / "source" / "review-panel-3d.svg", 1600, 760, 64),
    ("decision-flow-3d", ASSET_DIR / "source" / "decision-flow-3d.svg", 1600, 720, 64),
    ("evidence-model-3d", ASSET_DIR / "source" / "evidence-model-3d.svg", 1600, 760, 64),
    ("outcome-loop-3d", ASSET_DIR / "source" / "outcome-loop-3d.svg", 1600, 720, 64),
    ("social-preview", ASSET_DIR / "source" / "social-preview.svg", 1280, 640, 64),
)


def generate() -> None:
    for name, source, width, height, colors in ASSETS:
        published = ASSET_DIR / f"{name}.png"
        rendered = ASSET_DIR / f"{name}.rendered.png"
        cairosvg.svg2png(
            bytestring=source.read_bytes(),
            write_to=str(rendered),
            output_width=width,
            output_height=height,
        )
        with Image.open(rendered) as image:
            quantized = image.convert("RGBA").quantize(
                colors=colors,
                method=Image.Quantize.FASTOCTREE,
                dither=Image.Dither.NONE,
            )
            quantized.save(published, optimize=True)
        rendered.unlink()


if __name__ == "__main__":
    generate()
