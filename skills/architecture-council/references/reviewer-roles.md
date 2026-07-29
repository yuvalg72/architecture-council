# Professional Reviewer Roles

## Selection principle

Select roles for method diversity, not decorative breadth. The panel should contain lenses that can disagree for different reasons.

## 1. Strategic and Business Reviewer

**Mandate**

Evaluate strategic fit, business value, opportunity cost, prioritization, incentives, and long-term optionality.

**Method**

- compare the decision with stated objectives;
- identify the value mechanism;
- test whether the work solves a priority problem;
- evaluate opportunity cost and lock-in;
- separate strategic advantage from activity.

**Common blind spot**

May underweight implementation friction or technical constraints.

**Required questions**

- What business outcome does this create?
- What is displaced by choosing it?
- Does the option preserve future options?
- Which stakeholder incentives could undermine the plan?

## 2. Technical and Security Architect

**Mandate**

Evaluate architecture correctness, security, resilience, integration, lifecycle, supportability, exact technical dependencies, and technical debt.

**Method**

- test assumptions against architecture and evidence;
- map dependencies and failure domains;
- assess security boundaries and data flows;
- examine compatibility, scale, rollback, and lifecycle;
- identify hidden coupling and unsupported states.

**Common blind spot**

May prefer technical completeness over business urgency or operational simplicity.

**Required questions**

- What can fail and what is the blast radius?
- Which technical facts remain unverified?
- Is rollback realistic?
- What new dependency or support burden is created?

## 3. Delivery and PMO Reviewer

**Mandate**

Evaluate scope, sequencing, prerequisites, responsibilities, milestones, acceptance, change control, capacity, and delivery confidence.

**Method**

- split discovery, design, implementation, validation, acceptance, and closure;
- identify missing owners and dependencies;
- test whether acceptance criteria are observable;
- assess schedule and resource realism;
- identify scope expansion and handover gaps.

**Common blind spot**

May optimize for delivery certainty at the expense of strategic ambition.

**Required questions**

- What must be true before work starts?
- Who owns each dependency and decision?
- What proves completion?
- What change would require reapproval?

## 4. Risk and Governance Reviewer

**Mandate**

Evaluate security, compliance, auditability, contractual exposure, accepted risk, decision rights, policy alignment, and tail events.

**Method**

- identify high-impact low-frequency failures;
- distinguish owned, transferred, accepted, and unmitigated risk;
- test approval and evidence trails;
- identify policy conflicts and legal or contractual consequences;
- define control and escalation requirements.

**Common blind spot**

May overvalue control and delay when experimentation would be safe.

**Required questions**

- What is the worst credible outcome?
- Who can accept the residual risk?
- What evidence must be retained?
- Which action creates an irreversible commitment?

## 5. Operational Simplicity Reviewer

**Mandate**

Evaluate maintainability, support burden, usability, monitoring, failure recovery, staffing, cognitive load, and day-two operations.

**Method**

- remove unnecessary complexity;
- test the solution under routine support conditions;
- evaluate observability and troubleshooting paths;
- identify manual steps and operational bottlenecks;
- prefer simple controls that fail visibly.

**Common blind spot**

May underweight future scale, strategic differentiation, or formal assurance.

**Required questions**

- Can the operating team support this reliably?
- What happens at 03:00 during a failure?
- Which step depends on one person's memory?
- What can be simplified without weakening the outcome?

## 6. Customer and Stakeholder Reviewer

**Mandate**

Evaluate user impact, customer value, communication, expectations, responsibility boundaries, commercial commitments, adoption, and trust.

**Method**

- identify affected stakeholders and success definitions;
- test whether commitments are clear and deliverable;
- evaluate usability and adoption barriers;
- examine responsibility splits and expectation gaps;
- identify communication and acceptance requirements.

**Common blind spot**

May prioritize immediate stakeholder preference over architecture integrity or long-term maintainability.

**Required questions**

- Who experiences the benefit and the disruption?
- What has been promised, and by whom?
- What must stakeholders test or approve?
- Could the decision damage trust even if technically successful?

## 7. Independent Chair

**Mandate**

Synthesize without advocating during the review rounds.

**Method**

- preserve dissent and unresolved questions;
- verify evidence labels;
- calculate the weighted tally;
- identify the decision threshold;
- convert analysis into one decision, one next action, and testable kill criteria.

**Prohibitions**

- do not vote;
- do not invent consensus;
- do not hide source or execution limitations;
- do not replace a split result with ambiguous prose.
