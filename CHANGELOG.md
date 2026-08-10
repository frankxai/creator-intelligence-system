# Changelog

All notable repository changes are documented here. Protocol versions, GitHub
releases, npm packages, and downstream GenCreator deployments are separate
surfaces; an entry here does not silently publish any of them.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
and this project uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- A machine-verifiable release ledger, human release audit, and protected,
  manual-only GitHub prerelease drafting path.
- Dependency-free release validation in local development and CI.

### Changed

- The core and voice packages are explicitly private until a separate package
  publication review approves names, artifacts, provenance, and registry scope.
- Public status wording now distinguishes the alpha source candidate from an
  actually tagged or published release.

## [0.1.0-alpha.0] - Candidate (unpublished)

### Added

- The CIP v0.1 protocol foundation and typed artifact model for capture,
  strategy, production, distribution, learning, and attestation.
- `@cis/core` and `@cis/voice` source workspaces.
- Starter packs for Claude Code, Claude Projects, and ChatGPT Custom GPTs.
- Architecture, roadmap, contribution, MIT licensing, and attestation guidance.

### Changed

- The GitHub landing experience gained an accessible system diagram and concise
  runtime, protocol, licensing, and contribution signals.

### Release truth

- Candidate boundary: `8e9ad45c33ad6ffb056a8b9ab465d79adf83d284`
- Commits included: 4
- Merged pull requests included: #1
- Semantic Git tags at the audit: none
- GitHub releases at the audit: none
- npm packages at the audit: none

This section records a candidate. It is not evidence that a tag, GitHub
prerelease, npm package, website deployment, or downstream product release
exists.
