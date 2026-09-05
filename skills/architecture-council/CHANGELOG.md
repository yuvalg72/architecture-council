# Changelog

## [Unreleased]

## [1.1.0] - 04/09/2026

### Changed

- Added a dedicated human-facing Skill landing page that documents capabilities, workflow, outputs, boundaries, examples, files, and repository navigation.
- Replaced legacy JPEG documentation graphics with an accessible vector-first isometric 3D asset set and refreshed Skill icon.
- Aligned the Skill interface brand color with the new public visual system.
- Generalized the security boundary so the public Skill contains no organization-specific wording while preserving the same sensitive-data controls.
- Added Decision Record schema 1.1 and structured `protocol_interventions` process-quality metadata.
- Defined five intervention categories: `insufficient_dissent`, `novelty_failure`, `premature_consensus`, `missing_stance`, and `evidence_gap`.
- Preserved legacy records without `schema_version` as schema 1.0 for backward compatibility.
- Clarified that intervention counts are not model calls, provider dispatches, extra votes, or evidence of independent execution.

### Validation

- Added deterministic landing-page contract checks and regression coverage.
- Added repository-wide public-identifier hygiene validation so organization-specific context cannot silently re-enter public text assets.
- Added Decision Record validation for schema version, required schema 1.1 intervention metadata, allowed categories, non-negative integer counts, and total-to-breakdown consistency.
- Added positive, negative, and legacy-compatibility regression cases for protocol intervention metadata.

## [1.0.2] - 29/07/2026

### Changed

- Replaced malformed JPEG assets with valid, distinct documentation graphics.
- Updated active documentation to describe only the professional Architecture Council operating model.
- Added repository-level integrity checks for stale code, stale terminology, image validity, version consistency, and package contents.
- Clarified the Independent Chairman as a synthesis-only role.

### Removed

- Obsolete host-specific installers, provider-routing utilities, plugin metadata, and unrelated repository automation.

## [1.0.1] - 29/07/2026

### Changed

- Completed the Decision Dossier and Decision Record schemas.
- Enforced dates, success criteria, provider approval, evidence completeness, reviewer stances, vote calculation, recommendation thresholds, outcome tracking, and kill-criterion authority.
- Added regression tests for identified validation gaps.
- Standardized the panel on professional executive and architecture reviewer roles.

## [1.0.0] - 29/07/2026

- Initial native ChatGPT Architecture Council Skill.
