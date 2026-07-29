# Routing and Modes

## Decision boundary

Use the lightest mode that can materially improve the decision.

| Condition | Direct answer | Quick Council | Duo Review | Full Council |
|---|---:|---:|---:|---:|
| Factual lookup | Yes | No | No | No |
| Cheap and reversible experiment | Usually | Sometimes | No | No |
| Important but reversible trade-off | Sometimes | Yes | Sometimes | No |
| One dominant polarity | No | Sometimes | Yes | Sometimes |
| Cross-functional decision | No | Sometimes | Sometimes | Yes |
| Policy, architecture, security, or contractual change | No | No | Sometimes | Yes |
| Difficult or expensive to reverse | No | No | Sometimes | Yes |
| Several plausible root causes or options | No | Sometimes | Sometimes | Yes |

## Quick Council

Use three reviewers. Default patterns:

- **Architecture**: Technical and Security + Operational Simplicity + Delivery and PMO
- **Security**: Technical and Security + Risk and Governance + Operational Simplicity
- **Strategy**: Strategic and Business + Customer and Stakeholder + Risk and Governance
- **Delivery**: Delivery and PMO + Operational Simplicity + Customer and Stakeholder
- **Organizational process**: Strategic and Business + Delivery and PMO + Operational Simplicity
- **Customer commitment**: Customer and Stakeholder + Delivery and PMO + Risk and Governance

Do not select three roles that are likely to repeat the same method.

## Duo Review

Select one central tension:

- security versus usability;
- speed versus stability;
- standardization versus flexibility;
- strategic redesign versus tactical fix;
- automation versus human control;
- centralization versus autonomy;
- formal assurance versus operational simplicity;
- customer urgency versus supportability;
- immediate cost versus lifecycle cost;
- resilience versus efficiency.

Name the polarity in the report.

## Full Council

Use all six voting reviewers and one independent chair.

Full Council is the default for:

- architecture standards;
- security policy;
- responsibility model changes;
- Skill portfolio consolidation or deprecation;
- make-or-buy decisions;
- broad operational model changes;
- decisions affecting multiple customers, teams, or systems;
- decisions with compliance, contractual, or substantial commercial consequences.

## Domain-weight seat

Designate the seat before analysis.

- Base weight for each reviewer: 1.0
- Clearly closest domain seat: 1.5
- Ambiguous domain match: no weighted seat

Never select the weighted seat after reading positions.

## Confidence weighting

Multiply base weight by:

- high: 1.00
- medium: 0.75
- low: 0.50

Calculate:

```text
weighted_support(option) = sum(base_weight x confidence_factor)
required_threshold = 2/3 x total_possible_base_weight
```

Keep the denominator at total possible base weight. Low confidence should make consensus harder, not easier.

## Split result

Return a split decision when no option reaches the threshold.

A split result must state:

- the leading options and weights;
- the unresolved evidence gap;
- the decision authority;
- the smallest next action that could resolve the split;
- the deadline or review condition.
