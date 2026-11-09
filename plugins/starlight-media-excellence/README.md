# Starlight Media Excellence

A portable, private **skills-only** plugin. It does not contain credentials, scheduled agents, MCP server endpoints, external app bindings or executable publishing tools. It works with the host's **actually observed** capabilities.

## Ownership and authority

- The canonical cross-format architecture is `frankxai/creator-intelligence-system` and `docs/VIDEO_PRODUCTION_OS.md`.
- GenCreator Studio owns creation, recording, review and edition UX.
- The accepted portfolio media policy is architecture_media_fabric_v3 in agentic-ops: R2 owns canonical binary media, Supabase owns metadata/approval records, Vercel handles web image delivery, and Drive holds human working files. Verify actual catalog connections and ingestion per session; the accepted architecture does not prove an end-to-end deployed DAM.
- Starlight Plugin Forge verifies packaging/installation. Official Plugin Creator saves this plugin; neither grants source access or makes an always-on worker.

## Route

- **media-director**: new or materially revised creative package, demo, carousel, animation, social campaign.
- **media-release-critic**: final or candidate visual, video, motion or copy review.
- **media-continuity**: find and reuse existing images/characters, inspect source coverage, resume a production or prepare an asset handoff.

Explicit plugin invocation or a matched skill may activate a relevant route. No plugin can promise universal automatic invocation in every chat. For agent-code repositories, copy the companion `AGENTS.md` instructions under the owning repo and keep native runtime jobs separate.

## Release meanings

`PROPOSED`, `SOURCE_READY`, `RENDERED`, `QA_PASS`, `FOUNDER_APPROVED`, `PUBLISHED`, `PERFORMANCE_OBSERVED` each requires a distinct receipt. Earlier states do not imply later ones.

## Offline reference and repository adoption

`scripts/render_media_pack.py` implements the four-beat conceptual media exercise in
`assets/reference/scene.json`; `scripts/verify_media_manifest.py` validates artifact
bytes and status constraints. Canonical GitHub source, tests, CI and `AGENTS.md` live in
`frankxai/creator-intelligence-system` instead of duplicating repository files inside the plugin.

Use a reviewed pull request to adopt those templates. Copying files alone does not
turn on hosted renders, third-party permissions or publishing.

PDF document IDs are derived from the source digest; in the tested Python/FFmpeg environment, both full renders produced identical hashes for all 18 output artifacts.
