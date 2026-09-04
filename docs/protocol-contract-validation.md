# Protocol Contract Validation

Architecture Council intentionally represents parts of its decision protocol in more than one committed surface. The cross-source validator exists to detect semantic drift between those surfaces before a release or pull request can be treated as valid.

## Authority model

- `skills/architecture-council/SKILL.md` remains authoritative for Skill triggering and execution behavior.
- Executable validators remain authoritative for machine validation mechanics applied to Decision Dossiers and Decision Records.
- Files under `skills/architecture-council/references/` are human-facing explanations and must remain consistent with the authoritative behavior.
- `validate_protocol_contract.py` is a regression guard. It does not replace `SKILL.md` with a second hidden product configuration.

## Protected invariants

The validator checks the professional reviewer roster, non-voting Independent Chairman, Quick/Duo/Full panel sizes, confidence factors, domain-weight base weight, two-thirds recommendation threshold, evidence taxonomy, structured reviewer stance contract, result enums, and execution-model honesty.

## Mutation testing

The protocol contract tests intentionally introduce isolated drift into temporary copies of the Skill. CI must fail when one surface changes without the corresponding authoritative or derived surfaces being updated.

Current mutation coverage includes panel-size drift, confidence-factor drift, domain-weight drift, reviewer-roster drift, Chairman voting drift, recommendation-threshold drift, execution-model enum drift, and STANCE-format drift.

## Change rule

A deliberate protocol change is valid only when every affected source, validator, test, and human-facing reference is updated together and the mutation suite remains green. Do not weaken the validator merely to make a partial protocol edit pass.
