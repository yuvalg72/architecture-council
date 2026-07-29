# ChatGPT Skill Distribution

The repository includes a native ChatGPT Skill at:

```text
skills/architecture-council/
```

The ChatGPT Skill adapts the Council of High Intelligence protocol into a
professional architecture and executive decision council while preserving the
original multi-host implementation at the repository root.

## Source of truth

Use the following authority order:

1. `skills/architecture-council/SKILL.md` for native ChatGPT behavior.
2. `skills/architecture-council/references/` for detailed ChatGPT protocols.
3. Root `SKILL.md` and host mirrors for Claude Code, Codex CLI, Gemini CLI, and
   OpenCode behavior.

The two distributions share protocol principles but are not byte-for-byte
mirrors. Host-specific routing and subagent execution remain in the original
files. The ChatGPT Skill reports the actual execution model and uses structured
single-model deliberation when independent agents or approved providers are not
available.

## Build and validate

Run:

```bash
python scripts/build-chatgpt-skill.py
```

The command:

1. validates the Skill bundle;
2. runs the positive and negative validator tests;
3. creates `dist/skill.zip`;
4. verifies that the archive contains the final Skill source.

The distributable filename is always `skill.zip`.

## Install in ChatGPT

Upload `dist/skill.zip` through the supported ChatGPT Skill installation flow.
After installation, verify:

- display name: `Architecture Council`;
- internal name: `architecture-council`;
- version: the value in `skills/architecture-council/VERSION`;
- the installed Skill contains the same `SKILL.md` as the repository version.

Do not claim installation or version parity without verifying both copies.

## Invocation examples

```text
Convene the Architecture Council to decide whether this platform should use a
centralized or distributed control plane.
```

```text
Run a Duo Review on security isolation versus operational simplicity.
```

```text
Run a Full Council on this customer-facing architecture change. Preserve the
minority position, define kill criteria, and state exactly one next action.
```

## Security boundary

For customer, Mornex, security, commercial, contractual, configuration, or
internal information, use only approved environments and providers. Do not
route sensitive material across multiple external providers by default. Never
include credentials, tokens, private keys, authentication material, or full
sensitive configurations.

## Lessons Learned integration

The Skill contains an explicit integration contract for the future
`lessons-learned` Skill. A council verdict is advisory and remains a candidate
decision until an authoritative approval or verified implementation outcome
supports promotion to a validated lesson.
