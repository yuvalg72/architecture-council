---
name: architecture-council
description: Convene a structured executive architecture and decision council for high-stakes, ambiguous, or cross-functional choices. Use when the user asks for an architecture council, executive decision council, multi-perspective review, red-team debate, quick council, duo debate, full council, trade-off analysis, minority report, kill criteria, decision dossier, or a consequential decision involving architecture, cybersecurity, operations, delivery, strategy, governance, customer impact, or organizational standards. Do not use for simple factual lookups, routine formatting, low-cost reversible experiments, or decisions already resolved by an authoritative instruction.
---

# Architecture Council

## Purpose

Convene a disciplined council that tests a material decision through independent professional lenses, direct disagreement, evidence classification, and an independent synthesis. Produce an actionable decision record without manufacturing consensus.

This Skill adapts the Council of High Intelligence protocol for native ChatGPT use. Use professional reviewer roles by default. Preserve the original historical lenses only as an optional compatibility mode.

## Operating boundary

Use the council when the decision has material downside, competing values, incomplete evidence, cross-functional consequences, or meaningful irreversibility.

Do not convene the council for:

- factual questions that primary sources can resolve;
- routine corrections or formatting;
- low-risk reversible choices better tested through a small experiment;
- explicit user instructions that already settle the decision;
- ceremonial support for a decision that has already been made.

When a council is not justified, answer directly and state why a council would add little value.

## Load references selectively

- Read `references/decision-dossier.md` before structuring the decision input.
- Read `references/routing-and-modes.md` before selecting a mode or panel.
- Read `references/reviewer-roles.md` before assigning reviewer contracts.
- Read `references/council-protocol.md` before running the deliberation.
- Read `references/output-contract.md` before drafting the verdict.
- Read `references/security-and-provider-policy.md` whenever internal, customer, security, configuration, commercial, or otherwise sensitive information is involved.
- Read `references/outcome-tracking.md` when the result must be reviewed after implementation.
- Read `references/lessons-learned-integration.md` when this Skill is invoked by or hands off to `lessons-learned`.
- Read `references/legacy-lenses.md` only when the user explicitly requests the original historical lenses or a legacy-compatible council.

## Workflow

Follow these steps in order. Do not merge the independent analysis and synthesis stages.

### 1. Establish the decision boundary

Determine whether the request is a decision, recommendation, architecture review, or unresolved trade-off.

Create a compact decision dossier containing:

- decision statement;
- required outcome;
- options under consideration;
- constraints and non-negotiables;
- evidence;
- facts, inferences, assumptions, and unknowns;
- reversibility;
- deadline;
- decision authority;
- risk of action and risk of inaction;
- sensitivity classification;
- relevant existing decisions, Skills, standards, or lesson IDs.

Use available files, connectors, repositories, company knowledge, and official sources when they materially improve the decision. Never claim a source was reviewed when it was unavailable.

Proceed with explicit assumptions when missing information does not block a useful analysis. Mark material unknowns instead of inventing answers.

### 2. Select the mode

Choose the lightest mode that can change the outcome:

- **Quick Council**: three reviewers, independent rapid analysis, final positions, and chair synthesis. Use for important but reversible decisions.
- **Duo Review**: two reviewers representing the central tension, direct response, final positions, and chair synthesis. Use when one polarity defines the choice.
- **Full Council**: six professional reviewers plus an independent chair, blind opening positions, anonymized cross-examination, final positions, weighted tally, and synthesis. Use for high-impact, difficult-to-reverse, cross-functional, or policy-level decisions.

State the selected mode and why it is proportionate.

### 3. Select the panel before analysis

Use the professional roles in `references/reviewer-roles.md`:

1. Strategic and Business Reviewer
2. Technical and Security Architect
3. Delivery and PMO Reviewer
4. Risk and Governance Reviewer
5. Operational Simplicity Reviewer
6. Customer and Stakeholder Reviewer
7. Independent Chair

For Quick Council, select the three roles most likely to disagree productively.

For Duo Review, select the two roles or polarity pair that best represents the central tension.

For Full Council, use all six reviewers and the independent chair.

Designate one domain-weight seat before any position is known. Give it a 1.5 base weight only when one role is clearly closest to the decision domain. If the match is ambiguous, designate no weighted seat.

### 4. Run the problem restatement gate

Before analysis, require each reviewer to provide:

1. one sentence stating the core decision through that reviewer's lens;
2. one alternative framing that the original question may have missed.

Identify materially divergent framings. Do not silently collapse them.

### 5. Produce independent opening positions

Generate each reviewer's first position without exposing the other reviewers' positions.

Each opening position must include:

- evidence labels: `FACT`, `INFERENCE`, `ASSUMPTION`, or `UNKNOWN`;
- the strongest argument for the preferred option;
- the strongest argument against it;
- the reviewer's main concern;
- what evidence would change the position;
- an initial recommendation and confidence.

When genuine isolated subagents are unavailable, perform separate structured passes and record the execution model as `single-model structured deliberation`. Do not claim model or provider independence that did not occur.

### 6. Run the mode-specific challenge round

- **Quick Council**: omit cross-examination. Require concise final positions after reviewing the dossier and restatements.
- **Duo Review**: give each side the other side's opening position. Require a direct response, identification of the strongest opposing point, and correction of one weakness in its own argument.
- **Full Council**: anonymize opening positions as stable labels such as Reviewer A, Reviewer B, and Reviewer C. Require each reviewer to challenge at least one material claim, identify one weakness in its own argument, and name one unresolved issue.

Do not reward agreement. Preserve valid dissent.

### 7. Require final stances

Each reviewer must end with exactly one line in this format:

```text
STANCE: <option> | CONFIDENCE: high|medium|low | DEALBREAKER: <observable condition>
```

Use confidence factors:

- high: 1.00
- medium: 0.75
- low: 0.50

Multiply the factor by the reviewer's base weight. Require at least two-thirds of total possible weighted support for a council recommendation. If the threshold is not reached, return a split decision instead of manufacturing consensus.

### 8. Perform independent chair synthesis

The chair must not act as a voting reviewer.

The chair must:

- restate the actual decision;
- distinguish facts from inferences, assumptions, and unknowns;
- present the weighted tally;
- lead with unresolved issues that could change the result;
- recommend one option only when the threshold and evidence justify it;
- preserve the strongest minority position;
- define acceptable compromises;
- define observable kill criteria;
- state exactly one immediate next action;
- assign an owner or decision authority;
- set a review date or review condition;
- state what evidence would reverse the recommendation;
- identify limitations in source access, execution model, or confidence.

Use the exact output structure in `references/output-contract.md`.

### 9. Create an outcome checkpoint

For decisions that will be implemented, record:

- prediction;
- owner;
- implementation status;
- review date or condition;
- success evidence;
- evidence that would change the recommendation;
- kill criteria;
- eventual result: `confirmed`, `revised`, `reversed`, or `inconclusive`.

Do not rewrite the original rationale after the outcome is known. Append the result as a separate checkpoint.

## Evidence and confidence rules

- Treat explicit user instructions and verified evidence as authoritative within their scope.
- Do not treat a previous assistant response as verified evidence unless the user approved it, an authoritative source confirmed it, or a validated outcome supports it.
- Separate `FACT`, `INFERENCE`, `ASSUMPTION`, and `UNKNOWN` in every material argument.
- Distinguish evidence strength from reviewer confidence.
- State source gaps clearly.
- Search current authoritative sources when the decision depends on changing facts, standards, software, prices, laws, vendor support, security advisories, or current roles.

## Security and provider rules

For Mornex, customer, security, configuration, commercial, contractual, or internal information:

- use only approved connected environments and providers;
- do not distribute the material across external providers by default;
- redact unnecessary identifiers before any cross-provider deliberation;
- never include secrets, passwords, tokens, private keys, full sensitive configurations, or authentication material;
- use `single-model structured deliberation` when provider approval or isolation cannot be verified;
- report the actual execution model and any routing limitations.

## Lessons Learned boundary

A council recommendation is advisory. It is not a validated organizational lesson merely because multiple reviewers agree.

When handing off to `lessons-learned`:

- record the result as a candidate decision or improvement action;
- include the decision record, kill criteria, owner, and review checkpoint;
- promote it to a validated lesson only after explicit authoritative approval or verified implementation evidence.

## Scripts

Use the bundled scripts when a structured JSON dossier or record is created:

```bash
python scripts/validate_decision_dossier.py decision-dossier.json
python scripts/validate_decision_record.py decision-record.json
python scripts/validate_skill_bundle.py .
```

A failed validation means the dossier, record, or Skill is not complete.
