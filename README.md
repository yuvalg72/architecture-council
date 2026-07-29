# Architecture Council

A native ChatGPT Skill for structured executive and architecture decision-making.

![Architecture Council professional review panel](skills/architecture-council/assets/professional-review-panel.jpg)

## Professional review panel

- **Strategic and Business Reviewer** - evaluates business value, priorities, return, and long-term impact.
- **Technical and Security Architect** - evaluates technical correctness, security, supportability, and technical debt.
- **Delivery and PMO Reviewer** - evaluates scope, dependencies, ownership, timeline, and acceptance.
- **Risk and Governance Reviewer** - evaluates risk, compliance, auditability, and rollback governance.
- **Operational Simplicity Reviewer** - evaluates practicality, maintainability, and unnecessary complexity.
- **Customer and Stakeholder Reviewer** - evaluates customer impact, communication, commitments, and responsibility split.
- **Independent Chairman** - performs synthesis only and does not vote.

## Decision process

1. Build and validate a Decision Dossier.
2. Choose Quick Council, Duo Review, or Full Council.
3. Produce independent reviewer positions.
4. Classify evidence as FACT, INFERENCE, ASSUMPTION, or UNKNOWN.
5. Challenge assumptions and preserve dissent.
6. Calculate confidence-weighted support.
7. Produce one decision record with kill criteria, one next action, an owner, and a review checkpoint.

## ChatGPT Skill

The canonical Skill is located at `skills/architecture-council/`.

Build and validate:

```bash
python scripts/build-chatgpt-skill.py
```

The resulting package is `dist/skill.zip`.

## Version

Current Skill version: `1.0.1`

## License

See `LICENSE` and `skills/architecture-council/LICENSES/council-of-high-intelligence-MIT.txt`.
