#!/usr/bin/env python3
"""Generate clear baseline JPEG documentation assets for Architecture Council."""
from __future__ import annotations

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "skills" / "architecture-council" / "assets"
W, H = 1600, 900
BG = (247, 244, 236)
CARD = (255, 252, 244)
INK = (31, 41, 55)
BLUE = (26, 95, 160)
GOLD = (160, 119, 48)
MUTED = (86, 96, 110)


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype(name, size)


def wrap(draw: ImageDraw.ImageDraw, text: str, width: int, selected: ImageFont.FreeTypeFont) -> list[str]:
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


def text_box(draw: ImageDraw.ImageDraw, text: str, box: tuple[int, int, int, int], size: int, *, bold: bool = False, center: bool = False, fill=INK) -> None:
    selected = font(size, bold)
    lines = wrap(draw, text, box[2] - box[0], selected)
    line_height = size + 8
    y = box[1]
    for line in lines:
        x = box[0]
        if center:
            x += ((box[2] - box[0]) - draw.textlength(line, font=selected)) / 2
        draw.text((x, y), line, font=selected, fill=fill)
        y += line_height


def canvas(title: str, subtitle: str) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    image = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, W, 132), fill=(255, 255, 255))
    draw.line((55, 118, W - 55, 118), fill=(205, 211, 220), width=2)
    text_box(draw, title, (55, 28, W - 55, 82), 46, bold=True, fill=INK)
    text_box(draw, subtitle, (55, 84, W - 55, 116), 22, fill=MUTED)
    return image, draw


def card(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], title: str, body: str, number: str | None = None) -> None:
    draw.rounded_rectangle(box, radius=18, fill=CARD, outline=(190, 177, 149), width=3)
    x1, y1, x2, y2 = box
    if number:
        draw.ellipse((x1 + 20, y1 + 20, x1 + 78, y1 + 78), fill=BLUE)
        text_box(draw, number, (x1 + 20, y1 + 29, x1 + 78, y1 + 68), 25, bold=True, center=True, fill=(255, 255, 255))
        title_x = x1 + 94
    else:
        title_x = x1 + 28
    text_box(draw, title, (title_x, y1 + 22, x2 - 24, y1 + 92), 25, bold=True)
    text_box(draw, body, (x1 + 28, y1 + 105, x2 - 28, y2 - 22), 19, fill=MUTED)


def save(image: Image.Image, name: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    target = OUT / name
    image.save(target, "JPEG", quality=94, optimize=True, progressive=False, subsampling=0)
    with Image.open(target) as check:
        check.verify()


def make_panel() -> None:
    image, draw = canvas(
        "Architecture Council - Professional Review Panel",
        "Professional decision lenses replace historical characters and theatrical personas.",
    )
    roles = [
        ("Strategic and Business Reviewer", "Business value, priorities, strategic alignment, opportunity cost, and long-term impact."),
        ("Technical and Security Architect", "Technical correctness, security, resilience, supportability, lifecycle, and technical debt."),
        ("Delivery and PMO Reviewer", "Scope, dependencies, ownership, sequencing, timeline, acceptance, rollback readiness, and closure."),
        ("Risk and Governance Reviewer", "Risk, compliance, auditability, decision rights, residual exposure, and rollback governance."),
        ("Operational Simplicity Reviewer", "Practicality, maintainability, supportability, clarity, and unnecessary complexity."),
        ("Customer and Stakeholder Reviewer", "Customer impact, communication, commitments, responsibility split, usability, and alignment."),
    ]
    for index, (title, body) in enumerate(roles):
        row, col = divmod(index, 3)
        x = 55 + col * 510
        y = 165 + row * 280
        card(draw, (x, y, x + 470, y + 245), title, body, str(index + 1))
    draw.rounded_rectangle((335, 742, 1265, 852), radius=20, fill=(239, 230, 204), outline=GOLD, width=4)
    text_box(draw, "7. Independent Chairman - Synthesis Only", (370, 760, 1235, 800), 28, bold=True, center=True)
    text_box(draw, "Verifies the tally, preserves dissent, defines kill criteria, and issues one immediate next action. The Chairman does not vote.", (385, 807, 1220, 842), 18, center=True, fill=MUTED)
    save(image, "professional-review-panel.jpg")


def make_process() -> None:
    image, draw = canvas("Architecture Council - Deliberation Process", "Use the smallest mode that can expose a decision-changing disagreement.")
    steps = [
        "Validate the Decision Dossier",
        "Select mode and reviewers before positions exist",
        "Produce independent opening positions",
        "Challenge assumptions and require self-correction",
        "Calculate confidence-weighted support",
        "Chairman synthesizes dissent, kill criteria, and one action",
    ]
    for index, step in enumerate(steps):
        y = 160 + index * 105
        card(draw, (100, y, 1500, y + 82), step, "", str(index + 1))
    text_box(draw, "Quick Council: 3 reviewers   |   Duo Review: 2 opposing lenses   |   Full Council: 6 reviewers plus Chairman", (100, 815, 1500, 855), 22, bold=True, center=True, fill=BLUE)
    save(image, "council-process.jpg")


def make_evidence() -> None:
    image, draw = canvas("Evidence and Decision Quality Model", "Label evidence before deliberation and do not manufacture consensus.")
    labels = [
        ("FACT", "Directly observed or verified."),
        ("INFERENCE", "A logical interpretation of facts."),
        ("ASSUMPTION", "Believed to be true but not verified."),
        ("UNKNOWN", "Missing information that could change the decision."),
    ]
    for index, (title, body) in enumerate(labels):
        y = 165 + index * 150
        card(draw, (65, y, 760, y + 120), title, body, str(index + 1))
    draw.rounded_rectangle((830, 165, 1535, 765), radius=20, fill=CARD, outline=(190, 177, 149), width=3)
    text_box(draw, "Weighted Decision Rule", (880, 205, 1485, 255), 34, bold=True, center=True)
    text_box(draw, "Base weight", (885, 305, 1115, 345), 25, bold=True, center=True, fill=BLUE)
    text_box(draw, "Every reviewer starts at 1.0", (875, 355, 1125, 415), 20, center=True, fill=MUTED)
    text_box(draw, "Domain seat", (1240, 305, 1470, 345), 25, bold=True, center=True, fill=BLUE)
    text_box(draw, "One preselected reviewer may receive 1.5", (1220, 355, 1490, 435), 20, center=True, fill=MUTED)
    draw.line((1120, 465, 1240, 465), fill=GOLD, width=5)
    text_box(draw, "Recommendation threshold", (920, 505, 1445, 550), 28, bold=True, center=True)
    text_box(draw, "At least two-thirds of total possible base weight", (925, 570, 1440, 640), 24, center=True, fill=MUTED)
    text_box(draw, "Otherwise return a Split Decision and preserve the minority position.", (900, 675, 1465, 735), 22, bold=True, center=True)
    save(image, "evidence-and-decision-model.jpg")


def make_outcome() -> None:
    image, draw = canvas("A Verdict Is a Hypothesis with a Review Date", "Record what would change the recommendation before acting.")
    fields = ["Decision", "Recommendation", "Prediction", "Owner", "Review checkpoint", "Success evidence", "Reversal evidence", "Kill criteria"]
    for index, title in enumerate(fields):
        row, col = divmod(index, 2)
        x = 65 + col * 770
        y = 160 + row * 145
        card(draw, (x, y, x + 700, y + 112), title, "")
    states = ["CONFIRMED", "REVISED", "REVERSED", "INCONCLUSIVE"]
    for index, state in enumerate(states):
        x = 65 + index * 380
        draw.rounded_rectangle((x, 770, x + 330, 842), radius=16, fill=(239, 230, 204), outline=GOLD, width=3)
        text_box(draw, state, (x + 15, 790, x + 315, 828), 23, bold=True, center=True)
    save(image, "outcome-tracking.jpg")


def make_overview() -> None:
    image, draw = canvas("Architecture Council", "A professional executive and architecture decision framework.")
    text_box(draw, "Six professional reviewers examine strategy, technology, delivery, governance, operations, and stakeholder impact. The Independent Chairman synthesizes only and does not vote.", (90, 165, 1510, 245), 27, center=True)
    sections = [
        ("1. Decision Dossier", "Define the decision, options, constraints, evidence, authority, risk, and success criteria."),
        ("2. Independent Review", "Generate opening positions before reviewers see one another's conclusions."),
        ("3. Productive Challenge", "Expose assumptions, blind spots, and genuine disagreement."),
        ("4. Weighted Verdict", "Apply confidence factors and preserve minority positions."),
        ("5. Outcome Checkpoint", "Assign an owner, prediction, review date, evidence, and kill criteria."),
    ]
    for index, (title, body) in enumerate(sections):
        col = index % 3
        row = index // 3
        x = 65 + col * 510
        y = 300 + row * 245
        card(draw, (x, y, x + 470, y + 205), title, body)
    draw.rounded_rectangle((390, 790, 1210, 850), radius=16, fill=BLUE)
    text_box(draw, "One decision record. One owner. One next action.", (420, 805, 1180, 840), 25, bold=True, center=True, fill=(255, 255, 255))
    save(image, "architecture-council-overview.jpg")


def main() -> int:
    make_overview()
    make_panel()
    make_process()
    make_evidence()
    make_outcome()
    print(f"Generated baseline JPEG documentation images in {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
