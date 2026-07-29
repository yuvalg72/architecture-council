# Output Contract

## Default report

Use this structure for Full Council. Remove inapplicable detail for Quick Council or Duo Review, but preserve the decision, evidence, dissent, kill criteria, and next action.

```markdown
# Architecture Council Decision Record

## Executive Verdict
**Result:** Recommended | Split | Defer | Reject
**Recommended option:** [Option or None]
**Decision authority:** [Owner or authority]
**Council confidence:** High | Medium | Low

[One concise paragraph stating the decision and why.]

## Decision Boundary
- **Decision:**
- **Required outcome:**
- **Options:**
- **Constraints:**
- **Reversibility:**
- **Deadline:**
- **Mode:** Quick | Duo | Full
- **Execution model:** Single-model structured deliberation | Verified isolated agents | Verified multi-provider
- **Domain-weight seat:**

## Evidence State
### Facts
- [FACT]

### Inferences
- [INFERENCE]

### Assumptions
- [ASSUMPTION]

### Unknowns
- [UNKNOWN]

## Problem Restatements
| Reviewer | Restatement | Alternative framing |
|---|---|---|

## Review Positions
### Strategic and Business
[Position]

### Technical and Security
[Position]

### Delivery and PMO
[Position]

### Risk and Governance
[Position]

### Operational Simplicity
[Position]

### Customer and Stakeholder
[Position]

## Challenge Round Findings
- Strongest challenge:
- Strongest counterargument:
- Material self-correction:
- Evidence request:

## Final Stances
```text
STANCE: ...
```

## Vote Tally
| Option | Weighted support | Threshold reached |
|---|---:|---:|

## Recommendation
[Recommendation or explicit split.]

## Rationale
1. [Reason]
2. [Reason]
3. [Reason]

## Acceptable Compromises
- [Compromise that does not destroy the required outcome]

## Minority Position
[Strongest dissenting case and when it should prevail.]

## Unresolved Questions
- [Question that could change the result]

## Kill Criteria
| Observable condition | Measure | Review date or trigger | Required response |
|---|---|---|---|

## Concrete Next Action
**Action:** [Exactly one immediate action]
**Owner:** [Owner]
**Due or trigger:** [Date or condition]

## Outcome Checkpoint
- **Prediction:**
- **Review date or condition:**
- **Success evidence:**
- **Evidence that would reverse the recommendation:**
- **Status:** proposed

## Limitations
- [Source, access, model isolation, or confidence limitation]
```

## Quick Council reductions

Keep:

- Executive Verdict
- Decision Boundary
- Evidence State
- three reviewer positions
- Final Stances
- Vote Tally
- Recommendation or Split
- Minority Position
- Kill Criteria
- Concrete Next Action
- Limitations

Omit the challenge round.

## Duo Review additions

Add:

- named central polarity;
- opening position from each side;
- direct response from each side;
- the strongest opposing point each side accepts.

## Machine-readable record

When persistence or validation is required, append or save a JSON record with:

```json
{
  "decision_id": "DEC-YYYY-NNN",
  "mode": "full",
  "execution_model": "single-model structured deliberation",
  "panel": [],
  "domain_weight_seat": null,
  "evidence_summary": {
    "facts": [],
    "inferences": [],
    "assumptions": [],
    "unknowns": []
  },
  "recommendation": "",
  "vote_tally": {},
  "minority_position": "",
  "unresolved_questions": [],
  "kill_criteria": [],
  "concrete_next_action": "",
  "owner": "",
  "review_date": null,
  "reversal_evidence": [],
  "status": "proposed",
  "confidence": "medium",
  "limitations": []
}
```

Run `scripts/validate_decision_record.py` before treating the record as complete.
