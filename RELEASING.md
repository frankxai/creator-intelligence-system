# Releasing Creator Intelligence System

CIS separates five things that are easy to confuse: protocol maturity,
repository source history, GitHub releases, npm packages, and downstream
GenCreator deployments. One never authorizes another.

## Current truth

- The source and package manifests identify `0.1.0-alpha.0`.
- Commit `8e9ad45c33ad6ffb056a8b9ab465d79adf83d284` is the complete four-commit
  alpha candidate boundary on `main`.
- No semantic Git tag or GitHub release existed at the 2026-08-10 audit.
- `creator-intelligence-system`, `@cis/core`, and `@cis/voice` did not exist on
  the public npm registry at that audit.
- The package workspaces remain private. A GitHub prerelease does not publish
  npm artifacts.
- The repository homepage routes to the related GenCreator Studio repository;
  CIS has no independently declared product website or deployed changelog.

## Meaningful-update rhythm

Update `CHANGELOG.md` when the CIP contract, exported types, voice model,
starter packs, attestation boundary, adapter surface, security posture, or
distribution path materially changes. Batch small documentation and dependency
chores into the next meaningful entry. A weekly audit should find missing
receipts; it must not manufacture releases.

Every candidate names an immutable Git boundary, commit and pull-request
receipts, validation results, package-publication state, public-surface state,
and human approvals in `docs/releases/release-ledger.json`.

## GitHub prerelease path

1. Update the changelog, candidate notes, audit, ledger, and status copy.
2. Run `pnpm audit:release` plus the normal build, typecheck, and security gates
   when machine preflight permits them.
3. Merge the governance change through a reviewed, draft-first pull request.
4. In a follow-up review, set the candidate to `ready`, record completed
   validation, and explicitly approve attestation, public-surface, and release
   decisions in the ledger.
5. Configure required reviewers on the `github-prerelease-draft` environment.
6. Manually run **Draft GitHub prerelease** from `main` with the exact version
   and target SHA in the ledger.
7. Review the generated GitHub draft. Publishing remains a human action.

The workflow rejects automatic triggers, a non-main dispatch, mismatched input,
an incomplete approval set, a non-ancestor target, a conflicting tag, or a
non-prerelease version. Safe retries may reuse the exact annotated tag or an
existing draft. It never publishes or marks a release as latest.

## npm is a separate launch

Removing `private: true` from a workspace is a deliberate product decision. It
requires package-name ownership, artifact and export inspection, provenance,
license and dependency review, registry authentication scope, dry-run packing,
and explicit human approval. The GitHub prerelease workflow has no npm token and
no registry command.

## Public trust surface

Until CIS has a dedicated website, the GitHub README, changelog, releases, and
linked GenCreator repository are its public receipts. The central FrankX domain
command may aggregate those receipts, but it cannot convert a draft candidate
into a published release.
