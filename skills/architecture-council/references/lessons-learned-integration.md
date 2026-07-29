# Lessons Learned Integration

## Architecture boundary

`architecture-council` decides what should be done now.

`lessons-learned` determines what durable rule should be retained after evidence accumulates.

Do not merge the two functions.

## Escalation conditions

The Lessons Learned Skill may escalate to Architecture Council when:

- the decision is Tier 3 or equivalent;
- the decision changes an organizational, security, technical, commercial, contractual, or governance standard;
- authoritative instructions conflict and evidence cannot resolve the conflict;
- the proposed change is difficult or expensive to reverse;
- failure could materially affect security, customers, operations, compliance, or several workflows;
- several viable alternatives remain after evidence review;
- a Skill consolidation, deprecation, or portfolio-level redesign is proposed;
- evidence supports more than one materially different root-cause explanation.

## Non-escalation conditions

Do not convene the council for:

- factual lookups;
- explicit user instructions;
- routine corrections;
- low-risk reversible changes;
- formatting improvements;
- broken-reference repairs;
- standard validation failures;
- routine weekly reviews;
- no-change reviews;
- decisions already resolved by an authoritative standing rule.

## Required handoff dossier

Before escalation, provide:

- decision statement;
- current situation;
- required outcome;
- options;
- constraints;
- facts, inferences, assumptions, and unknowns;
- reversibility;
- deadline;
- decision authority;
- risk of action and inaction;
- relevant lesson IDs;
- relevant Skill IDs;
- sensitivity and provider restrictions.

## Council return contract

Return:

- recommended decision or explicit split;
- rationale;
- acceptable compromises;
- minority position;
- unresolved questions;
- kill criteria;
- exactly one immediate next action;
- owner;
- review date;
- evidence that would reverse the recommendation.

## Governance boundary

Council consensus is not evidence that a lesson is validated.

Store the result as a candidate decision or improvement action. Promote it to a validated lesson only after implementation evidence or an explicit authoritative user decision supports it.
