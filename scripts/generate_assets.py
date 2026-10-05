#!/usr/bin/env python3
"""Generate lossless PNG publication assets from Architecture Council SVG sources."""
from __future__ import annotations

from pathlib import Path

import cairosvg
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
ASSET_DIR = ROOT / "skills" / "architecture-council" / "assets"
ASSETS = (
    ("icon", 256, 256),
    ("hero-council-3d", 1600, 900),
    ("review-panel-3d", 1600, 760),
    ("decision-flow-3d", 1600, 720),
    ("evidence-model-3d", 1600, 760),
    ("outcome-loop-3d", 1600, 720),
    ("social-preview", 1280, 640),
)


def generate() -> None:
    for name, width, height in ASSETS:
        source = ASSET_DIR / f"{name}.svg"
        published = ASSET_DIR / f"{name}.png"
        cairosvg.svg2png(
            bytestring=source.read_bytes(),
            write_to=str(published),
            output_width=width,
            output_height=height,
        )
        with Image.open(published) as image:
            image.verify()


if __name__ == "__main__":
    generate()
