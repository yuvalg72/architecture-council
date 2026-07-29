# Architecture Council

A native ChatGPT Skill for structured executive and architecture decision-making.

![Architecture Council overview](skills/architecture-council/assets/architecture-council-overview.jpg)

## Professional review panel

Architecture Council uses professional operating roles rather than historical characters or theatrical personas. Each reviewer owns a distinct decision lens. The Independent Chairman synthesizes the result and does not vote.

![Professional review panel](skills/architecture-council/assets/professional-review-panel.jpg)

| Role | Review responsibility |
|---|---|
| Strategic and Business Reviewer | Business value, priorities, strategic alignment, opportunity cost, and long-term impact |
| Technical and Security Architect | Technical correctness, security, supportability, resilience, lifecycle, and technical debt |
| Delivery and PMO Reviewer | Scope, dependencies, ownership, sequencing, timeline, acceptance, rollback readiness, and closure |
| Risk and Governance Reviewer | Risk, compliance, auditability, decision rights, controls, residual exposure, and rollback governance |
| Operational Simplicity Reviewer | Practicality, maintainability, supportability, clarity, and unnecessary complexity |
| Customer and Stakeholder Reviewer | Customer impact, communication, commitments, responsibility split, usability, and stakeholder alignment |
| Independent Chairman | Synthesis only, weighted tally verification, dissent preservation, kill criteria, and one immediate next action |

## Method

Choose the smallest council that can still expose a decision-changing disagreement.

- **Quick Council** - three reviewers for an important but reversible decision.
- **Duo Review** - two opposing professional lenses when one core tension defines the decision.
- **Full Council** - all six reviewers plus the Independent Chairman for high-impact, cross-functional, or difficult-to-reverse decisions.

### Council process

![Council process](skills/architecture-council/assets/council-process.jpg)

1. Build and validate a Decision Dossier.
2. Select the mode and panel before positions exist.
3. Produce independent opening positions.
4. Classify evidence explicitly.
5. Challenge assumptions and require self-correction.
6. Calculate confidence-weighted support.
7. Preserve dissent and unresolved questions.
8. Produce one decision record with kill criteria, one next action, an owner, and a review checkpoint.

### Evidence and decision model

![Evidence and decision model](skills/architecture-council/assets/evidence-and-decision-model.jpg)

Material claims are labeled as `FACT`, `INFERENCE`, `ASSUMPTION`, or `UNKNOWN`. The final recommendation requires at least two-thirds of total possible base weight. When no option reaches the threshold, the result is recorded as split rather than forced into consensus.

### Outcome tracking

![Outcome tracking](skills/architecture-council/assets/outcome-tracking.jpg)

A verdict is treated as a hypothesis with a prediction, owner, review date or condition, success evidence, reversal evidence, and observable kill criteria. The later outcome is appended as `confirmed`, `revised`, `reversed`, or `inconclusive` without rewriting the original rationale.

## Repository structure

```text
.github/
  ISSUE_TEMPLATE/
  workflows/
scripts/
  build-chatgpt-skill.py
  validate-repository.py
skills/architecture-council/
  SKILL.md
  VERSION
  agents/openai.yaml
  assets/
  references/
  scripts/
  tests/
```

The canonical Skill source is `skills/architecture-council/`.

## Build and validate

```bash
python scripts/validate-repository.py
python scripts/build-chatgpt-skill.py
```

The distributable package is generated as `dist/skill.zip`.

## Version

Current Skill version: `1.0.2`

## Security

Do not include credentials, private keys, authentication material, raw customer configurations, or unapproved internal information. Use approved connected environments for internal or sensitive dossiers.

## License

See `LICENSE` and the bundled third-party license file under `skills/architecture-council/LICENSES/`.
