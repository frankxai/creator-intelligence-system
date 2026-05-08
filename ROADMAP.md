# Roadmap

> Where CIS goes from here. Updated as milestones land.

---

## v0.1.0-alpha · 2026-05-07 (today)

The foundation commit.

- [x] Repo created, MIT licensed
- [x] README, ARCHITECTURE, SPEC, ATTESTATION drafted
- [x] CIP v0.1 protocol shape locked
- [ ] `@cis/core` types compile
- [ ] `@cis/voice` audit + buildSystemPrompt working
- [ ] First adapter stub (`adapters/distribute-bluesky/`)

---

## MV1 · Friday May 9 2026

The first proof: capture → publish via the system, on the open repo.

- [ ] All MV1 work runs against this repo (creator-intelligence-system) as the substrate
- [ ] [GenCreator-Studio](https://github.com/frankxai/GenCreator-Studio) deploys to a Vercel preview as gallery, distributor, and attestation endpoint
- [ ] One short authored in a creator-owned agent workspace, imported as a CIP bundle, and published to Bluesky via `@cis/distribute-bluesky`
- [ ] First Attestation rendered in the published post
- [ ] CIP v0.1 spec frozen for the week

---

## MV2 · End of May 2026

The substrate is real. The amplifier is live.

- [ ] All 6 layers have at least one shipping adapter:
  - L1 — SIS submodule
  - L2 — `capture-whisper-groq` + `capture-file-drop`
  - L3 — `strategy-frontmatter` + Format Library v0.1 (10 formats)
  - L4 — `produce-anthropic` + `produce-vercel-ai-sdk-image`
  - L5 — `distribute-bluesky` + `distribute-linkedin` + `distribute-beehiiv`
  - L6 — `learn-agentdb` (writing only; reducer comes later)
- [ ] CIP v0.1.0 published as `@cis/core@0.1.0` to npm
- [ ] MCP server published, registered with Anthropic + OpenAI MCP registries
- [ ] Starter packs shipped: claude-code, claude-project, chatgpt-project
- [ ] First non-Frank creator boots a starter pack, ships through GenCreator-Studio, and does not need a server-side LLM key unless they opt into hosted automation

---

## MV3 · End of July 2026

100 creators. Real protocol adoption.

- [ ] CIP v1.0.0 frozen after 4+ weeks of production use
- [ ] Hyperframes + Farcaster Frames v2 distribution adapters shipped
- [ ] Federated learning RFC-001 implemented (opt-in pool)
- [ ] One non-reference implementation of CIP exists (community contribution)
- [ ] 100+ creators running their own CIS instances (telemetry opt-in)
- [ ] Tauri desktop wrapper alpha for GenCreator-Studio

---

## v1.0 · End of October 2026

The 100-year artifact ships.

- [ ] CIP v1.0.0 final spec published
- [ ] Reference verifier (`@cis/verify`) shipped as a single-file ESM module
- [ ] Multi-creator briefs (collaborative captures + reviews)
- [ ] Music as first-class content type (Suno end-to-end)
- [ ] Self-hosted deployment guide (`docs/self-host.md`) for any Node 22+ box
- [ ] [GenCreator-Studio](https://github.com/frankxai/GenCreator-Studio) v1.0 — production-ready Vercel template
- [ ] First sponsored CIS instance for a non-Frank creator (paid services on top of OSS)

---

## v2.0 · 2027

The protocol becomes a category.

- [ ] CIP adopted by at least one other major OSS project as their content protocol
- [ ] Browser extensions verify attestations on any webpage
- [ ] Audience-side verification UI ships (a Chrome extension that surfaces `cis://` references on social platforms)
- [ ] Web3-anchored timestamp opt-in (Arweave / Filecoin) for permanent attestations

---

## Beyond

The protocol outlives the implementation. By 2030, the original CIS reference implementation should be one of dozens. By 2125, nobody should remember it was a Next.js app on a laptop in Madrid in 2026.

The protocol is what they remember.

---

> *Ship the protocol, not just the code.*
