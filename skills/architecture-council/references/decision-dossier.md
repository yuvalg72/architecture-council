# Decision Dossier

Create the smallest complete evidence package needed for a serious decision.

Required fields include decision ID, title, exact question, required outcome, at least two options, constraints, success criteria, evidence, no-material-unknowns declaration, reversibility, deadline, decision authority, risks of action and inaction, sensitivity, external-provider controls, and related decisions, Skills, and lessons.

Use `FACT`, `INFERENCE`, `ASSUMPTION`, and `UNKNOWN` labels. FACT and INFERENCE require a source. Use `no_material_unknowns: true` only when no material unknown remains and no UNKNOWN item is present.

For confidential or restricted material, external providers require a documented approval reference. Otherwise set `external_provider_allowed` to `false` and `external_provider_approval` to `null`.

Validate with:

```bash
python scripts/validate_decision_dossier.py decision-dossier.json
```
