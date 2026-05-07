---
name: cis
description: Creator Intelligence System — content substrate with capture, strategy, production, distribution, learning. Use when working with the CIS protocol or building a CIS-powered surface.
---

# Creator Intelligence System (CIS) skill

This skill loads the CIS protocol contract into your Claude Code session. After installing, the assistant can dispatch CIS-typed work via the conductor and refer to the canonical types in `@cis/core`.

## When this skill fires

- The user asks to "capture", "brief", "produce", "publish", or "learn from" content.
- The working dir contains a `creator-intelligence-system/` checkout or a project that depends on `@cis/core`.
- The user mentions CIP, attestation, or asks "what does CIS think about X".

## What the assistant should do

1. **Read the local CIS docs** — `creator-intelligence-system/README.md`, `ARCHITECTURE.md`, `SPEC.md`, `ATTESTATION.md`.
2. **Use `@cis/core` types** for any new code. Never define ad-hoc shapes for `Capture`, `Brief`, `Publication`, etc.
3. **Honor the attestation contract** — every code path that produces a publishable artifact must accumulate `AgentStep[]`, `ModelInvocation[]`, and `HumanReview[]`.
4. **Run the voice audit** at every L4 production boundary. Use `@cis/voice` `auditVoice()`. If issues are non-empty, surface them to the user before proceeding.
5. **Default to open OSS** — when picking a dependency, prefer MIT/Apache. Never recommend tldraw (proprietary $6k/yr); use react-flow / xyflow instead.

## Slash commands this skill exposes

These commands are scaffolded in `starter-packs/claude-code/commands/`:

- `/cis-capture` — start a capture from voice / clip / file drop
- `/cis-brief` — create a Brief from one or more Captures
- `/cis-produce` — run the production chain on a Brief
- `/cis-distribute` — publish an AssetBundle to one or more channels (atomic saga)
- `/cis-attest` — render the attestation footer for any artifact
- `/cis-audit` — run the voice audit on any draft

## Companion agents

These agents are scaffolded in `starter-packs/claude-code/agents/`:

- `cis-orchestrator` — the conductor; routes briefs, dispatches adapters
- `cis-voice-guard` — runs voice audit at every L4 boundary; rejects banned/quarantined terms
- `cis-attestor` — signs attestations, writes to the well-known endpoint

## Cross-AI portability

The same skill markdown works in:

- **Claude Code** (this file)
- **Cursor** (rename to `.cursor/rules/cis.md`)
- **Gemini CLI** (use as a system prompt)
- **Codex** (paste into project instructions)
