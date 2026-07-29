# Outcome Tracking

## Why track outcomes

A decision protocol improves only when recommendations are checked against results. Do not rewrite the original rationale after the outcome is known.

## Required checkpoint

Record before implementation:

- decision ID;
- recommendation;
- prediction;
- owner;
- implementation action;
- success evidence;
- review date or review condition;
- evidence that would reverse the recommendation;
- kill criteria;
- expected cost of reversal.

## Status lifecycle

- `proposed`: council completed, authority has not approved.
- `approved`: authorized decision recorded.
- `implemented`: action completed, outcome not yet evaluated.
- `confirmed`: observed evidence supports the prediction.
- `revised`: the decision remains directionally valid but requires material adjustment.
- `reversed`: evidence supports undoing or replacing the decision.
- `inconclusive`: available evidence does not support a reliable conclusion.

## Kill criteria

Each kill criterion must contain:

- observable condition;
- measurable indicator;
- review date or trigger;
- required response;
- decision authority for the response.

Avoid vague criteria such as "if it does not work".

## Review entry

Append a review entry:

```yaml
reviewed_on: YYYY-MM-DD
status: confirmed | revised | reversed | inconclusive
observed_evidence:
  - Evidence
prediction_result: Supported | Partially supported | Not supported | Unknown
kill_criteria_triggered:
  - Criterion or none
action_taken: Action or none
reviewed_by: Person or role
notes: Concise explanation
```

## Lessons Learned handoff

Only promote the decision to a validated lesson when:

- the authorized decision is explicit; or
- implementation evidence confirms the operating principle; or
- repeated outcomes support the same conclusion.

Council agreement alone is insufficient.
