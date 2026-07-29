---
name: architecture-council
description: Convene a structured executive architecture and decision council for high-stakes, ambiguous, or cross-functional choices. Use for architecture council, executive decision council, multi-perspective review, red-team debate, Quick Council, Duo Review, Full Council, trade-off analysis, minority report, kill criteria, decision dossier, or consequential decisions involving architecture, cybersecurity, operations, delivery, strategy, governance, customer impact, or organizational standards. Do not use for simple factual lookups, routine formatting, low-cost reversible experiments, or decisions already resolved by an authoritative instruction.
---

# Architecture Council

## Purpose

Test a material decision through independent professional lenses, explicit evidence classification, productive disagreement, weighted final stances, and independent synthesis. Produce an actionable decision record without manufacturing consensus.

## Operating boundary

Use the council when a decision has material downside, competing values, incomplete evidence, cross-functional consequences, or meaningful irreversibility. Answer directly when primary evidence settles the question or a low-cost experiment is more appropriate.

## Required references

- Read `references/decision-dossier.md` before structuring the input.
- Read `references/routing-and-modes.md` before selecting a mode.
- Read `references/reviewer-roles.md` before assigning reviewers.
- Read `references/council-protocol.md` before deliberation.
- Read `references/output-contract.md` before drafting the verdict.
- Read `references/security-and-provider-policy.md` for internal or sensitive material.
- Read `references/outcome-tracking.md` when implementation will be reviewed later.
- Read `references/lessons-learned-integration.md` for handoff to `lessons-learned`.

## Professional panel

Use these roles:

1. Strategic and Business Reviewer
2. Technical and Security Architect
3. Delivery and PMO Reviewer
4. Risk and Governance Reviewer
5. Operational Simplicity Reviewer
6. Customer and Stakeholder Reviewer
7. Independent Chairman

The Chairman synthesizes only and does not vote.

## Workflow

1. Build a decision dossier with the decision, outcome, options, constraints, success criteria, evidence, reversibility, authority, risks, sensitivity, and related controls.
2. Choose the lightest mode that can change the outcome: Quick, Duo, or Full.
3. Select the panel before any position is known. Designate a domain-weight seat only when one reviewer clearly owns the closest domain.
4. Run the problem-restatement gate. Require each reviewer to state the core decision and one alternative framing.
5. Produce independent opening positions using `FACT`, `INFERENCE`, `ASSUMPTION`, and `UNKNOWN` labels.
6. Run the mode-specific challenge round. Full Council uses anonymized cross-examination and explicit self-correction. Duo Review uses direct responses. Quick Council omits cross-examination.
7. Require one final stance per reviewer:

```text
STANCE: <option> | CONFIDENCE: high|medium|low | DEALBREAKER: <observable condition>
```

8. Calculate weighted support. Use confidence factors high `1.00`, medium `0.75`, and low `0.50`. Give the preselected domain seat a base weight of `1.5`; all others receive `1.0`. Require at least two-thirds of total possible base weight for a recommendation.
9. Let the Independent Chairman synthesize the evidence, tally, dissent, compromises, kill criteria, exactly one immediate action, owner, and review checkpoint.
10. Validate structured JSON records with the bundled scripts before treating them as complete.

## Execution honesty

When isolated agents are unavailable, run separate structured passes and identify the execution model as `single-model structured deliberation`. Never claim provider or model independence without verification.

## Security boundary

For Mornex, customer, configuration, commercial, contractual, security, or internal information:

- use only approved connected environments and providers;
- do not distribute material across external providers by default;
- redact unnecessary identifiers;
- never include passwords, tokens, private keys, authentication material, or full sensitive configurations;
- report the actual execution model and routing limitations.

## Lessons Learned boundary

A council verdict is advisory. Transfer it as a candidate decision or improvement action. Promote it to a validated lesson only after explicit authoritative approval or verified implementation evidence.

## Validation

```bash
python scripts/validate_decision_dossier.py decision-dossier.json
python scripts/validate_decision_record.py decision-record.json
python scripts/validate_skill_bundle.py .
```

A failed validation means the artifact is incomplete.
