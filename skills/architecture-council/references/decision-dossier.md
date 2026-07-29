# Decision Dossier

## Purpose

Create the smallest complete evidence package needed for a serious decision. Do not start with personas. Start with the decision boundary.

## Required fields

Use this structure as a default:

```yaml
decision_id: DEC-YYYY-NNN
title: Short descriptive title
question: The exact decision to be made
required_outcome: What the decision must accomplish
options:
  - id: option-a
    name: Option A
    description: Short description
  - id: option-b
    name: Option B
    description: Short description
constraints:
  - Constraint or non-negotiable
success_criteria:
  - Observable success condition
evidence:
  - label: FACT
    statement: Directly supported statement
    source: Authoritative source or supplied evidence
  - label: INFERENCE
    statement: Conclusion derived from evidence
    source: Supporting evidence reference
  - label: ASSUMPTION
    statement: Unverified premise required by an option
    source: null
  - label: UNKNOWN
    statement: Missing information that could change the decision
    source: null
reversibility: reversible | partially-reversible | difficult-to-reverse | irreversible
deadline: YYYY-MM-DD or null
decision_authority: Person, role, or group authorized to decide
risk_of_action:
  - Material risk created by acting
risk_of_inaction:
  - Material risk created by delaying or doing nothing
sensitivity: public | internal | confidential | restricted
external_provider_allowed: false
related_decisions: []
related_skills: []
related_lessons: []
```

## Evidence labels

- `FACT`: directly supported by supplied or retrieved evidence.
- `INFERENCE`: follows from evidence but is not directly observed.
- `ASSUMPTION`: required for the argument and still unverified.
- `UNKNOWN`: missing information that could materially change the decision.

A confident statement is not automatically a fact.

## Framing check

Before deliberation, write:

- **Observed question**: the question as originally asked.
- **Decision question**: the choice the authorized decision-maker must actually make.
- **Alternative framing**: a materially different but plausible way to define the problem.
- **Non-decision**: matters explicitly outside the council's authority or scope.

## Sensitivity gate

When sensitivity is `confidential` or `restricted`, set `external_provider_allowed` to `false` unless an approved data-handling basis explicitly permits otherwise.

## Validation

Save structured dossiers as JSON and run:

```bash
python scripts/validate_decision_dossier.py decision-dossier.json
```
