# Contributing

Architecture Council is maintained as a native ChatGPT Skill.

## Change rules

1. Start from the latest `main` branch.
2. Keep `skills/architecture-council/SKILL.md` concise and below 500 lines.
3. Place detailed operating rules in `references/`.
4. Use the six professional reviewers and the Independent Chairman only.
5. Do not add historical-character personas, host-specific installers, provider-routing scripts, or unsupported multi-agent claims.
6. Update `VERSION`, the root changelog, and the Skill changelog for material changes.
7. Test every changed script.
8. Run `python scripts/validate-repository.py`.
9. Run `python scripts/build-chatgpt-skill.py`.
10. Verify `dist/skill.zip` after the final source change.
11. Preserve the MIT license files.
12. Do not publish secrets, customer configurations, or unapproved internal material.

## Pull requests

Describe the decision-quality problem being solved, list the affected contracts or validators, and provide the exact validation commands and results. Keep unrelated cleanup out of the same pull request.
