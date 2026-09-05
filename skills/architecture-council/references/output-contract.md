# Decision Record Contract

Newly generated Decision Records use `schema_version: "1.1"`. A complete schema 1.1 record includes result, recommended option, decision authority, mode, execution model, panel, domain-weight seat, one stance per reviewer, evidence summary, protocol interventions, recommendation, rationale, acceptable compromises, weighted tally, minority position, unresolved questions, kill criteria, exactly one next action, implementation action, owner, due date or trigger, prediction, review checkpoint, success evidence, reversal evidence, expected cost of reversal, status, confidence, and limitations.

`protocol_interventions` contains `total` plus an exact breakdown for `insufficient_dissent`, `novelty_failure`, `premature_consensus`, `missing_stance`, and `evidence_gap`. Each corrective pass is assigned one primary category, so `total` must equal the sum of the five category counts. Normal mode-defined deliberation steps are not interventions. The field measures process-quality corrections, not model calls or provider dispatches.

Records without `schema_version` are treated as legacy schema 1.0 records for backward compatibility. Schema 1.1 records require `protocol_interventions`.

The validator recalculates the weighted tally from reviewer stances, verifies the domain seat, and enforces the two-thirds recommendation threshold. A split result is required when no option reaches the threshold. Protocol intervention metadata does not alter vote weight, recommendation thresholds, or Chairman voting status.
