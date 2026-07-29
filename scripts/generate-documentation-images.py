#!/usr/bin/env python3
"""Generate Architecture Council documentation JPEGs."""
from __future__ import annotations

import random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "skills" / "architecture-council" / "assets"
W, H = 1600, 900
INK = (49, 37, 25)
ACCENT = (110, 54, 44)
GOLD = (126, 96, 45)
PAPER = (232, 215, 179)
PANEL = (239, 226, 196)


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype("DejaVuSerif-Bold.ttf" if bold else "DejaVuSerif.ttf", size)


def parchment() -> Image.Image:
    rng = random.Random(42)
    image = Image.new("RGB", (W, H), PAPER)
    pixels = image.load()
    for y in range(H):
        for x in range(W):
            edge = min(x, y, W - 1 - x, H - 1 - y)
            shade = max(0, 28 - edge) * 2
            noise = rng.randint(-7, 7)
            pixels[x, y] = tuple(max(0, min(255, value + noise - shade)) for value in PAPER)
    return image.filter(ImageFilter.GaussianBlur(0.35))


def frame(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], width: int = 5) -> None:
    draw.rounded_rectangle(box, radius=14, fill=PANEL, outline=INK, width=width)
    draw.rounded_rectangle((box[0]+9, box[1]+9, box[2]-9, box[3]-9), radius=10, outline=GOLD, width=2)


def centered(draw: ImageDraw.ImageDraw, text: str, y: int, size: int, bold: bool = False, fill=INK) -> None:
    selected = font(size, bold)
    bounds = draw.textbbox((0, 0), text, font=selected)
    draw.text(((W - (bounds[2] - bounds[0])) / 2, y), text, font=selected, fill=fill)


def wrapped(draw: ImageDraw.ImageDraw, text: str, width: int, selected: ImageFont.FreeTypeFont) -> list[str]:
    lines: list[str] = []
    current = ""
    for word in text.split():
        trial = f"{current} {word}".strip()
        if draw.textlength(trial, font=selected) <= width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def paragraph(draw: ImageDraw.ImageDraw, text: str, box: tuple[int, int, int, int], size: int = 24, bold: bool = False, left: bool = False) -> None:
    selected = font(size, bold)
    lines = wrapped(draw, text, box[2] - box[0], selected)
    height = size + 8
    y = box[1] + max(0, (box[3] - box[1] - len(lines) * height) // 2)
    for line in lines:
        x = box[0] if left else box[0] + ((box[2] - box[0]) - draw.textlength(line, font=selected)) / 2
        draw.text((x, y), line, font=selected, fill=INK)
        y += height


def seal(draw: ImageDraw.ImageDraw, x: int, y: int, label: str) -> None:
    draw.ellipse((x-42, y-42, x+42, y+42), fill=(214, 191, 143), outline=INK, width=4)
    selected = font(28, True)
    bounds = draw.textbbox((0, 0), label, font=selected)
    draw.text((x-(bounds[2]-bounds[0])/2, y-(bounds[3]-bounds[1])/2-4), label, font=selected, fill=ACCENT)


def save(image: Image.Image, name: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    image.save(OUT / name, "JPEG", quality=94, optimize=True, progressive=True)


def make_overview() -> None:
    image = parchment(); draw = ImageDraw.Draw(image)
    centered(draw, "Architecture Council", 36, 56, True)
    centered(draw, "Executive and architecture decision framework", 105, 27, False, ACCENT)
    frame(draw, (65, 175, 1535, 330))
    paragraph(draw, "Six professional reviewers examine strategy, technology, delivery, governance, operations, and stakeholder impact. The Independent Chairman synthesizes only and does not vote.", (115, 200, 1485, 305), 28)
    sections = [
        ("1. Dossier", "Define the decision, options, evidence, authority, risk, and success criteria."),
        ("2. Independent review", "Generate opening positions before reviewers see one another's conclusions."),
        ("3. Productive challenge", "Expose assumptions, blind spots, and genuine disagreement."),
        ("4. Weighted verdict", "Apply confidence factors and preserve minority positions."),
        ("5. Outcome checkpoint", "Assign an owner, prediction, review date, evidence, and kill criteria."),
    ]
    for index, (title, description) in enumerate(sections):
        column, row = index % 3, index // 3
        x, y = 65 + column * 500, 385 + row * 205
        frame(draw, (x, y, x + 455, y + 170))
        paragraph(draw, title, (x+25, y+18, x+430, y+68), 27, True, True)
        paragraph(draw, description, (x+25, y+70, x+430, y+150), 19, False, True)
    frame(draw, (565, 770, 1035, 850))
    paragraph(draw, "One decision record. One owner. One next action.", (595, 785, 1005, 835), 24, True)
    save(image, "architecture-council-overview.jpg")


def make_panel() -> None:
    image = parchment(); draw = ImageDraw.Draw(image)
    centered(draw, "Architecture Council - Professional Review Panel", 38, 46, True)
    centered(draw, "Useful friction through complementary professional lenses", 98, 25, False, ACCENT)
    roles = [
        ("Strategic and Business Reviewer", "Business value, priorities, strategic alignment, opportunity cost, and long-term impact."),
        ("Technical and Security Architect", "Technical correctness, security, resilience, supportability, lifecycle, and technical debt."),
        ("Delivery and PMO Reviewer", "Scope, dependencies, ownership, sequencing, timeline, acceptance, rollback readiness, and closure."),
        ("Risk and Governance Reviewer", "Risk, compliance, auditability, decision rights, controls, residual exposure, and rollback governance."),
        ("Operational Simplicity Reviewer", "Practicality, maintainability, supportability, clarity, and unnecessary complexity."),
        ("Customer and Stakeholder Reviewer", "Customer impact, communication, commitments, responsibility split, usability, and alignment."),
    ]
    for index, (title, description) in enumerate(roles):
        row, column = divmod(index, 3)
        x, y = 55 + column * 515, 155 + row * 300
        frame(draw, (x, y, x + 470, y + 270))
        seal(draw, x + 68, y + 72, str(index + 1))
        paragraph(draw, title, (x+125, y+25, x+445, y+110), 27, True, True)
        paragraph(draw, description, (x+35, y+125, x+435, y+245), 20, False, True)
    frame(draw, (400, 760, 1200, 855))
    seal(draw, 465, 807, "7")
    paragraph(draw, "Independent Chairman - Synthesis Only", (535, 770, 1170, 810), 29, True, True)
    paragraph(draw, "Verifies the weighted tally, preserves dissent, defines kill criteria, and issues one immediate next action.", (535, 808, 1170, 850), 18, False, True)
    save(image, "professional-review-panel.jpg")


def make_process() -> None:
    image = parchment(); draw = ImageDraw.Draw(image)
    centered(draw, "Architecture Council - Deliberation Process", 38, 46, True)
    centered(draw, "Select the smallest mode that can still change the decision", 98, 25, False, ACCENT)
    steps = [
        "Ground the decision with a validated dossier",
        "Select mode and panel before positions exist",
        "Produce independent opening positions",
        "Challenge assumptions and require self-correction",
        "Calculate confidence-weighted support",
        "Chairman synthesizes dissent, kill criteria, and one action",
    ]
    for index, step in enumerate(steps):
        y = 160 + index * 110
        seal(draw, 125, y + 35, str(index + 1))
        frame(draw, (200, y - 8, 1485, y + 78), 4)
        paragraph(draw, step, (235, y, 1450, y + 70), 27, False, True)
        if index < len(steps) - 1:
            draw.line((125, y + 77, 125, y + 102), fill=INK, width=5)
    paragraph(draw, "Quick Council: 3 reviewers | Duo Review: 2 opposing lenses | Full Council: 6 reviewers + Chairman", (120, 820, 1480, 875), 23, True)
    save(image, "council-process.jpg")


def make_evidence() -> None:
    image = parchment(); draw = ImageDraw.Draw(image)
    centered(draw, "Evidence and Decision Quality Model", 38, 46, True)
    centered(draw, "Separate what is known from what is believed before debate begins", 98, 25, False, ACCENT)
    labels = [
        ("FACT", "Directly observed or verified."),
        ("INFERENCE", "A logical interpretation of facts."),
        ("ASSUMPTION", "Required for the argument but not verified."),
        ("UNKNOWN", "Missing information that could change the decision."),
    ]
    for index, (name, description) in enumerate(labels):
        y = 175 + index * 145
        frame(draw, (70, y, 760, y + 115))
        seal(draw, 140, y + 58, str(index + 1))
        paragraph(draw, name, (200, y+10, 410, y+60), 30, True, True)
        paragraph(draw, description, (200, y+58, 725, y+105), 20, False, True)
    frame(draw, (840, 175, 1530, 720))
    paragraph(draw, "Weighted Decision Rule", (900, 205, 1470, 270), 34, True)
    paragraph(draw, "Every reviewer starts with a base weight of 1.0. One preselected domain seat may receive 1.5. Confidence factors are high 1.00, medium 0.75, and low 0.50.", (900, 290, 1470, 470), 24, False, True)
    paragraph(draw, "A recommendation requires at least two-thirds of total possible base weight. Otherwise return a split decision and preserve the strongest minority position.", (900, 500, 1470, 680), 25, True, True)
    paragraph(draw, "Do not manufacture consensus.", (420, 785, 1180, 850), 31, True)
    save(image, "evidence-and-decision-model.jpg")


def make_outcome() -> None:
    image = parchment(); draw = ImageDraw.Draw(image)
    centered(draw, "A Verdict Is a Hypothesis with a Review Date", 38, 46, True)
    centered(draw, "Record what would change the recommendation before acting", 98, 25, False, ACCENT)
    fields = ["Decision", "Recommendation", "Prediction", "Owner", "Review checkpoint", "Success evidence", "Reversal evidence", "Kill criteria"]
    for index, name in enumerate(fields):
        row, column = divmod(index, 2)
        x, y = 70 + column * 780, 170 + row * 145
        frame(draw, (x, y, x + 700, y + 110))
        paragraph(draw, name, (x+35, y+15, x+665, y+95), 27, True, True)
    for index, state in enumerate(("CONFIRMED", "REVISED", "REVERSED", "INCONCLUSIVE")):
        x = 70 + index * 380
        frame(draw, (x, 770, x + 330, 845))
        paragraph(draw, state, (x+15, 780, x+315, 835), 23, True)
    save(image, "outcome-tracking.jpg")


def main() -> int:
    make_overview()
    make_panel()
    make_process()
    make_evidence()
    make_outcome()
    print(f"Generated documentation images in {OUT}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
