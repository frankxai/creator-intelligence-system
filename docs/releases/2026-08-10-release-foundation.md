# Creator Intelligence System release-foundation audit — 2026-08-10

## Decision

Bless the existing source as a traceable `v0.1.0-alpha.0` candidate, not a
stable release. The exact source boundary is
`8e9ad45c33ad6ffb056a8b9ab465d79adf83d284`.

## Repository evidence

- Canonical repository: `frankxai/creator-intelligence-system`
- Default branch: `main`
- Visibility: public
- Audited history: 2026-05-07 through 2026-07-14
- Commit count: 4
- Merged pull requests: #1
- Semantic tags: 0
- GitHub releases: 0

The four boundary commits are the initial repository seed, the CIP alpha
foundation, the subscription-first architecture clarification, and the merged
GitHub landing polish.

## Package evidence

The root, `@cis/core`, and `@cis/voice` manifests all declare
`0.1.0-alpha.0`. Registry lookups on 2026-08-10 returned `E404` for all three
names. The root was already private; this foundation makes every workspace
private so a repository release cannot accidentally become an npm launch.

## Public-surface evidence

The repository homepage points to the related public GenCreator Studio GitHub
repository. CIS does not declare a dedicated production domain. Its truthful
public surface is therefore GitHub: README, changelog, source history, and any
future reviewed releases. No website deployment is created by this lane.

## Validation and gates

- The dependency-free contract verifies repository identity, immutable history,
  receipts, package privacy, documentation consistency, and workflow safety.
- The GitHub workflow is manual-only, protected by an environment, creates only
  a draft prerelease, and requires explicit approvals in the ledger.
- Full build-class validation is deferred while the machine-performance gate is
  HOLD. This does not weaken release publication: the ledger remains draft and
  validation approval remains false.

## Next boundary

`0.1.0-alpha.1` has no invented target. It begins only after the first
prerelease decision and a later coherent, audited source boundary.
