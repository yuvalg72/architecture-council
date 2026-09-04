# Outcome Tracking

Treat every verdict as a hypothesis with a review checkpoint.

Before acting, record the decision, recommendation, prediction, owner, implementation action, review date or condition, success evidence, reversal evidence, expected cost of reversal, kill criteria with decision authority, and schema 1.1 protocol intervention metadata when the record is newly generated.

Keep `protocol_interventions` as a process-quality signal that can later be correlated with outcomes. Do not reinterpret intervention counts as extra vote weight, model-call counts, or evidence that independent agents or providers were used.

At review, append one result without rewriting the original rationale: `confirmed`, `revised`, `reversed`, or `inconclusive`.
