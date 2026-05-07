# Content Intelligence Protocol (CIP)

> **Version:** 0.1.0-alpha
> **Status:** Draft
> **Author:** Frank Riemer (frankxai) · 2026-05-07

---

## Status

This is the alpha specification of the Content Intelligence Protocol. Breaking changes are expected during the v0.x cycle. v1.0.0 freezes the protocol after at least four weeks of real production use across two or more independent CIS instances.

If you implement this protocol, follow the repo for RFC discussions and version pinning.

---

## Goals

CIP defines:

1. **The shape of every artifact** that flows through a CIS instance — Capture, Brief, AssetBundle, Publication, LearnedPattern, Attestation.
2. **The contracts between layers** — the signatures every adapter must implement.
3. **The transparency baseline** — every Publication carries a verifiable Attestation.

CIP does *not* define:

- The UI of any specific surface.
- The choice of model provider, distribution channel, or storage backend.
- The pricing or business model of any CIS instance.

---

## Non-goals

CIP is not:

- A replacement for ActivityPub, RSS, or AT Protocol. CIP describes *creation flow*; those describe *publishing flow*. CIP outputs feed into them.
- A replacement for MCP. CIS exposes itself as an MCP server, but CIP is about the artifacts inside CIS, not the transport.
- A copyright or license registry. CIP attestations are about provenance, not ownership.

---

## Core types

All types are defined in TypeScript in `@cis/core/src/types.ts` and mirrored as JSON Schema in `@cis/core/src/schemas/cip-v0.1.json`.

### `DIDIdentity`

```ts
export interface DIDIdentity {
  did: string                  // e.g. "did:plc:..."
  handle?: string              // e.g. "frankx.bsky.social"
  publicKey: string            // base58 or multibase encoded
}
```

The creator's portable identity. CIS does not issue identities; it consumes them.

### `Capture`

```ts
export interface Capture {
  id: string                   // ULID, sortable
  source: CaptureSource        // 'voice' | 'web-clip' | 'file-drop' | 'notion' | 'obsidian' | 'email' | 'manual'
  capturedAt: string           // ISO 8601
  identity: DIDIdentity
  transcript?: string          // text representation if applicable
  rawText?: string             // freeform brief from creator
  mediaRefs: MediaRef[]        // pointers to L1 storage
  metadata: Record<string, unknown>
  // attestation chain begins here
  attestation: Attestation
}
```

A Capture is the moment the creator's intent enters the system. Every downstream artifact traces back to a Capture.

### `Brief`

```ts
export interface Brief {
  id: string                   // ULID
  captureRefs: string[]        // one or more Capture IDs
  format: FormatId             // ref to the format library
  audience?: AudienceId
  channel: ChannelId
  voicePreset: string          // ref to @cis/voice config
  hook?: string                // optional opening line anchor
  notes?: string               // freeform context for L4 producers
  scheduledFor?: string        // ISO 8601, when the published version should ship
  agentChain: AgentStep[]      // pre-planned chain (L4 may diverge)
  status: BriefStatus
  attestation: Attestation
}

export type BriefStatus =
  | 'draft'
  | 'ready'
  | 'producing'
  | 'staged'
  | 'published'
  | 'archived'
```

A Brief is the strategic decision: what to make, for whom, in what voice.

### `AssetBundle`

```ts
export interface AssetBundle {
  id: string
  briefId: string
  channel: ChannelId
  artifacts: Artifact[]        // one or more rendered files
  captions?: Record<ChannelId, string>  // per-channel caption overrides
  schemaJsonLd?: object        // VideoObject / Article / etc
  voiceIssues: VoiceIssue[]    // from @cis/voice audit; empty if clean
  costReport: CostReport       // tokens + dollars
  attestation: Attestation
}

export interface Artifact {
  kind: 'text' | 'image' | 'video' | 'audio' | 'frame'
  contentType: string          // MIME type — REQUIRED, never guessed
  bytes?: number
  url?: string                 // L1 storage URL
  inlineText?: string
  alt?: string
}
```

An AssetBundle is the output of L4 production. It is staged but not published.

### `Publication`

```ts
export interface Publication {
  id: string
  bundleId: string
  channel: ChannelId
  url: string                  // canonical URL on the platform
  postedAt: string             // ISO 8601
  identity: DIDIdentity
  platformIds: Record<string, string> // e.g. { tweetId: '...', linkedinUrn: '...' }
  attestation: Attestation     // <-- carries the whole chain
}
```

A Publication is the final fact: this thing went live, here, at this time, with this provenance.

### `LearnedPattern`

```ts
export interface LearnedPattern {
  id: string
  format: FormatId
  channel: ChannelId
  pattern: string              // natural-language description
  evidence: PublicationRef[]   // pubs that support this pattern
  windowStart: string          // ISO 8601
  windowEnd: string
  signal: PerformanceSignalKind
  weight: number               // 0..1
}
```

A LearnedPattern is what the system has noticed about what works.

---

## Attestation

The attestation type is the moat. See [ATTESTATION.md](./ATTESTATION.md) for the full discussion.

```ts
export interface Attestation {
  v: 1                              // protocol version
  artifactId: string                // what's being attested
  artifactKind: ArtifactKind
  humanIdea: string                 // creator's brief, verbatim
  agentChain: AgentStep[]           // every agent that touched it, in order
  models: ModelInvocation[]         // every LLM call, with token counts
  reviewers: HumanReview[]          // who approved, when
  signedAt: string                  // ISO 8601
  signature: string                 // ed25519 over a canonical JSON encoding
  signerDid: string                 // the creator's DID
  // optional fields
  parents?: string[]                // attestations this one composes
  rendering?: AttestationRendering  // hint for how to display this in published content
}

export interface AgentStep {
  agent: string                     // adapter ID, e.g. "produce-anthropic"
  step: string                      // e.g. "draft-hook", "voice-guard", "schema-emit"
  startedAt: string
  endedAt: string
  inputs?: { kind: string; ref?: string }[]
  outputs?: { kind: string; ref?: string }[]
}

export interface ModelInvocation {
  provider: string                  // 'anthropic' | 'openai' | 'google' | 'fal' | etc.
  model: string                     // 'claude-sonnet-4-6' | 'gpt-5' | 'imagen-3' etc.
  inputTokens?: number
  outputTokens?: number
  imageCount?: number
  costUsd?: number
}

export interface HumanReview {
  did: string                       // reviewer's DID (often the creator)
  decision: 'approve' | 'edit' | 'reject'
  reviewedAt: string
  comment?: string
}
```

### Signature canonicalization

The attestation signature covers a deterministic JSON encoding of every field except `signature` itself. The canonicalization rules:

1. Sort all object keys alphabetically.
2. Drop `undefined` and `null` values.
3. Use UTF-8 encoded JSON with no whitespace.
4. Serialize numbers per RFC 8785 (JSON Canonicalization Scheme).
5. Sign the resulting bytes with ed25519 over the creator's DID key.

Verifiers MUST reject any attestation where the signature does not validate against the canonical encoding.

### Rendering

By default, every published Publication renders an attestation footer:

```
Captured by Frank · Drafted by claude-sonnet-4-6 via @cis/produce-anthropic
Edited by hook-author + voice-guard · Reviewed by Frank · Published 2026-05-09T07:00Z
Attestation: cis://attest/01HX9...
```

The `cis://` URI resolves to a public attestation document at `<host>/.well-known/cis/attestations/{id}`. Anyone can verify provenance.

The `rendering` field on Attestation lets briefs override the default footer for stylistic reasons (different channels, different lengths). The full attestation is always reachable via the URI.

---

## Adapter contracts

Each layer defines an interface. Adapters implement the interface. Conductors compose adapters.

See [ARCHITECTURE.md](./ARCHITECTURE.md) for each layer's interface signature. The full TypeScript declarations live in `@cis/core/src/`:

- `substrate.ts` — Substrate
- `capture.ts` — CaptureAdapter
- `strategy.ts` — StrategyAdapter
- `produce.ts` — ProductionAdapter
- `distribute.ts` — DistributionAdapter
- `learn.ts` — LearningAdapter

---

## Compatibility

CIP v0.x is alpha and may break. CIP v1.x will follow strict SemVer:

- **Major** bump: removed fields, type changes, signature scheme changes.
- **Minor** bump: new optional fields, new adapter capabilities.
- **Patch** bump: documentation, clarifications, no schema change.

Implementations SHOULD include the protocol version they support in their MCP capabilities and HTTP `User-Agent` headers:

```
User-Agent: cis-impl/0.1.0 (+cip/0.1.0; +https://example.com)
```

---

## RFCs

Anything that changes the protocol surface goes through an RFC. RFCs live in `docs/rfcs/`. Discussion in GitHub Issues with the `rfc:` prefix.

Initial RFC backlog (drafts to write):

- RFC-001: Federated learning across CIS instances (opt-in pool of LearnedPatterns)
- RFC-002: Multi-creator briefs (collaborative captures and reviews)
- RFC-003: Pluggable substrates (non-SIS L1 implementations)
- RFC-004: Streaming attestations (signing partial outputs of long-running productions)
- RFC-005: Cross-protocol bridges (CIP → ActivityPub Activity, CIP → AT Protocol record)

---

## Reference implementation

This repository is the reference implementation. Anyone is free to write a competing implementation in any language; conformance means: types validate against `cip-v0.1.json`, attestations sign + verify per the canonicalization rules, and the layer contracts are honored.

The first non-reference implementation is a stretch goal for v1.0.0.

---

> *A protocol that makes provenance verifiable is the only honest answer to the AI-content trust crisis.*
