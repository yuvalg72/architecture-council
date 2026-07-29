# Security and Provider Policy

## Data classes

- `public`: approved for public disclosure.
- `internal`: organizational information not intended for public disclosure.
- `confidential`: customer, commercial, security, personnel, architecture, or operational information requiring controlled access.
- `restricted`: secrets, credentials, sensitive configurations, regulated data, or material whose disclosure could create significant harm.

## Default routing policy

For `internal`, `confidential`, or `restricted` information:

- use only approved connected environments;
- do not route content to multiple external providers by default;
- prefer one approved model with structured independent passes;
- redact unnecessary customer, employee, system, and commercial identifiers;
- minimize copied source content;
- preserve exact technical identifiers only when they are necessary for the decision and permitted in the active environment.

## Prohibited content

Never place in a council dossier, prompt, log, output, or committed Skill asset:

- passwords;
- access tokens;
- API keys;
- private keys;
- authentication cookies;
- recovery codes;
- unredacted secret values;
- full customer configuration exports when a sanitized summary is sufficient;
- unnecessary personal data.

## Provider claims

Do not claim that:

- multiple models were used;
- reviewers were isolated;
- an external provider was queried;
- data was redacted;
- a connector was accessed;
- a result was independently verified;

unless the action actually occurred and was verified.

Record one execution model:

- `single-model structured deliberation`;
- `verified isolated agents`;
- `verified multi-provider`.

## Cross-provider approval gate

Cross-provider deliberation requires all of the following:

1. the data sensitivity allows it;
2. each provider is approved for the data class;
3. unnecessary identifiers are removed;
4. the user or governing policy authorizes the routing;
5. provider and model use can be verified;
6. failures and fallbacks are reported.

If any condition is missing, use single-model structured deliberation.

## Repository safety

Before publishing Skill or decision assets:

- scan for secrets;
- remove raw customer data;
- remove unapproved configuration extracts;
- verify that examples are generic;
- preserve the third-party MIT notice;
- verify the diff contains only intended files.
