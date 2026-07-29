# Council Protocol

## Enforcement principles

- Separate initial analysis from peer influence.
- Preserve method diversity.
- Require reviewers to identify flaws in their own arguments.
- Preserve minority positions.
- Do not confuse confidence with evidence.
- Use a bounded round count.
- End with one next action.

## Common opening contract

Every reviewer produces:

1. problem restatement;
2. alternative framing;
3. evidence inventory using `FACT`, `INFERENCE`, `ASSUMPTION`, and `UNKNOWN`;
4. strongest case for the preferred option;
5. strongest case against it;
6. material failure mode;
7. evidence that would change the view;
8. opening recommendation and confidence.

## Quick Council protocol

1. Select three reviewers and the independent chair.
2. Lock the domain-weight seat.
3. Run the restatement gate.
4. Produce independent analyses of no more than 250 words each.
5. Present all analyses to the chair.
6. Require each reviewer to produce a final stance of no more than 100 words and the machine-readable `STANCE` line.
7. Calculate the tally.
8. Produce a concise verdict with recommendation or split, minority position, unknowns, kill criteria, and one next action.

Do not run cross-examination in Quick Council.

## Duo Review protocol

1. Define the central polarity.
2. Select two opposing professional roles or two optional legacy lenses.
3. Lock the domain-weight seat only if one side is clearly closer to the decision domain.
4. Run the restatement gate.
5. Produce independent opening positions.
6. Exchange positions.
7. Require each side to:
   - identify the strongest opposing point;
   - identify one flaw in its own opening position;
   - answer the opposing argument directly;
   - state what remains unresolved.
8. Produce final stances and the machine-readable `STANCE` lines.
9. Let the independent chair synthesize the decision, split, or experiment.

## Full Council protocol

### Round 0 - Framing

- Validate the dossier.
- Select all six reviewers and the chair.
- Lock the domain-weight seat.
- Run the restatement gate.
- Record framing disagreements.

### Round 1 - Blind analysis

Generate each opening position independently. Do not expose peer positions.

### Enforcement scan 1

Check:

- every evidence label is used correctly;
- each reviewer names at least one unknown;
- each reviewer states disconfirming evidence;
- methods are distinct;
- no reviewer claims access or verification that did not occur.

### Round 2 - Anonymized cross-examination

Mask positions behind stable labels. Give each reviewer all peer positions without revealing the role name attached to each position.

Require each reviewer to:

- challenge one material claim;
- identify one strong peer argument;
- identify one flaw in its own earlier argument;
- propose one test or evidence request;
- preserve its position or update it explicitly.

### Enforcement scan 2

Check:

- dissent has not disappeared without new evidence;
- repeated claims are not counted as independent evidence;
- reviewers did not merely converge on the most confident wording;
- unresolved questions remain visible;
- no new unsupported fact appeared during debate.

### Round 3 - Final stance

Require each reviewer to produce:

```text
STANCE: <option> | CONFIDENCE: high|medium|low | DEALBREAKER: <observable condition>
```

A reviewer may choose `DEFER` when a specific missing fact must be resolved first.

### Round 4 - Independent synthesis

The chair:

- verifies the dossier and evidence labels;
- calculates the weighted tally;
- states whether the threshold was reached;
- preserves the minority view;
- identifies unresolved questions;
- defines acceptable compromises;
- defines kill criteria;
- gives exactly one immediate next action;
- records owner, review date, and reversal evidence.

## Anti-recursion rule

Do not convene additional councils inside a council. When the panel identifies a separate decision, place it in `Unresolved Questions` or `Follow-on Decisions`.

## Anti-ceremony rule

When the user has already decided, do not present a council as independent validation. Offer a pre-mortem, red-team review, or implementation risk review instead.
