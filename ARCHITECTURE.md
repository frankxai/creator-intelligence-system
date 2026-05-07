# Architecture

> The 6-layer stack of CIS, layer-by-layer.

---

## Design principles

1. **Each layer has a typed interface.** Adapters implement interfaces. No hidden coupling between layers.
2. **Defaults are open.** Every layer ships a default open-source adapter. Swap any of them without touching the rest.
3. **Substrate is sacred.** L1 is owned by the creator. We never call home, never ingest your palace into a hosted service.
4. **Attestation is mandatory.** Every artifact crossing a layer boundary carries provenance. No anonymous outputs.
5. **Composition over inheritance.** Adapters compose. The orchestrator is dumb on purpose; it reads, dispatches, attests.

---

## L1 — Substrate

**Purpose:** Identity, memory, MCP, governance.

CIS does not invent these primitives. It inherits them from [SIS](https://github.com/frankxai/Starlight-Intelligence-System), the upstream substrate that already specifies the SIP protocol, the 9-layer model, and the memory palace pattern.

**Concrete tech (defaults):**

- **Identity:** `did:plc` from the AT Protocol — portable across Bluesky, Lens, and any DID-aware service. The creator's identity does not live inside CIS.
- **Memory palace:** SIS palace as a git submodule. Everything CIS captures, produces, and learns is written to the palace. The substrate never owns memory; it borrows from SIS.
- **MCP server:** stateless HTTP transport, registered with Anthropic + OpenAI MCP registries. Any AI assistant can read CIS state and call `cis.*` tools.
- **Governance:** SIP v1.1.0 layer model + the SIP-Attest cryptographic primitive (re-exported here as the foundation of [ATTESTATION.md](./ATTESTATION.md)).

**Interface (`@cis/core/src/substrate.ts`):**

```ts
export interface Substrate {
  identity(): Promise<DIDIdentity>
  remember(scope: PalaceScope, payload: unknown): Promise<MemoryRef>
  recall(scope: PalaceScope, query: string): Promise<MemoryRecord[]>
  attest(artifact: Artifact, chain: AgentStep[]): Promise<Attestation>
  govern(decision: GovernanceQuestion): Promise<GovernanceVerdict>
}
```

**Failure modes & mitigations:**

- SIS palace not yet propagated → CIS forces propagation forward; we are the first downstream consumer.
- DID identity refresh → handle 60-day token refresh in the adapter, never in user-facing code.

---

## L2 — Capture

**Purpose:** Frictionless ingest. Capture what the creator means before the moment is gone.

**Modes:**

| Mode | Tech | Context |
|---|---|---|
| **Voice** | Whisper-on-Groq (`groq-sdk` v0.x) — 200ms latency, 1/100th OpenAI cost | Optional; rely on Claude Code / ChatGPT native dictation if you prefer |
| **Web clip** | Plasmo browser extension (`@plasmohq/plasmo` v0.88+) | Right-click → "Capture to CIS" |
| **File drop** | PWA + drag-and-drop, Vercel Blob → R2 migration when tripwire fires | Markdown, audio, video, images, PDFs |
| **Notion bridge** | `@notionhq/client` v2.4+ read-only watch | Optional |
| **Obsidian bridge** | `chokidar` watch on vault directory | Optional |
| **Email** | webhook from any inbox (Postmark, Resend) → forwarded captures | Optional |

**Interface (`@cis/core/src/capture.ts`):**

```ts
export interface CaptureAdapter {
  readonly id: string
  readonly modes: CaptureMode[]
  ingest(input: CaptureInput): Promise<Capture>
}

export interface Capture {
  id: string
  source: CaptureSource
  capturedAt: string // ISO 8601
  identity: DIDIdentity
  transcript?: string
  mediaRefs: MediaRef[]
  rawText?: string
  metadata: Record<string, unknown>
}
```

**Note:** voice capture is **not** the moat. Claude/ChatGPT/CC have native dictation. CIS supports voice for completeness, but the differentiator is what happens *after* capture, not capture itself.

---

## L3 — Strategy

**Purpose:** What to make. For whom. Why. When.

This is the *thinking* layer — where briefs are born from captures, anchored in calendar slots, mapped to formats, and locked to brand voice.

**Concrete tech (defaults):**

- **Calendar:** typed `data/content-calendar.json` rendered by `@fullcalendar/react` v6.1+
- **Format library:** typed records in `@cis/core/src/formats/`. Each format = `{ id, name, channel, lengthMs, hookPattern, structure, voicePreset, exampleSlugs }`.
- **ICP/audience:** typed records in `@cis/core/src/audiences/`.
- **Voice config:** the `@cis/voice` package — single source of truth. See [voice config docs](./packages/voice/README.md).

**Interface (`@cis/core/src/strategy.ts`):**

```ts
export interface StrategyAdapter {
  readonly id: string
  brief(capture: Capture, context: StrategyContext): Promise<Brief>
  format(briefId: string, format: FormatId): Promise<Brief>
  schedule(brief: Brief, slot: ISODateTime): Promise<Brief>
}
```

---

## L4 — Production

**Purpose:** Brief → assets. Multi-agent, multi-modal, brand-locked.

**Concrete tech (defaults):**

- **Orchestration:** Claude Agent SDK (`@anthropic-ai/claude-agent-sdk`) for autonomous loops; raw Anthropic SDK (`@anthropic-ai/sdk`) for single-turn API calls.
- **Model abstraction:** Vercel AI SDK (`ai` v4.x) — `generateText`, `generateImage`, `streamText`, `generateObject`. Provider-agnostic.
- **Image:** Vercel AI Gateway → `fal-ai/flux` or `google/imagen-3` via the AI SDK. Replaces hand-rolled Nano Banana glue. Preserves `mimeType` honesty (per [feedback memo](https://github.com/frankxai/FrankX/blob/main/CLAUDE.md)).
- **Video:** Remotion (peer dependency only — users install) for React-rendered video. HeyGen Hyperframes (Apache 2.0) for HTML-rendered agent-authored video.
- **Music:** Suno API (when public) or `suno-prompt-architect` skill for manual.
- **Distribution mini-apps:** Farcaster Frames v2 via `@farcaster/frame-sdk` (MIT).
- **Voice guard:** `@cis/voice` `auditVoice()` runs at every agent boundary. Banned phrases or quarantined terms reject the draft.

**Interface (`@cis/core/src/produce.ts`):**

```ts
export interface ProductionAdapter {
  readonly id: string
  readonly capabilities: ProductionCapability[]
  produce(brief: Brief, signal?: AbortSignal): AsyncIterable<ProductionStep>
}

export interface ProductionStep {
  agent: string
  model?: string
  inputTokens?: number
  outputTokens?: number
  cost?: number
  artifacts?: Artifact[]
  voiceIssues?: VoiceIssue[]
}
```

**Cost discipline:** every `produce()` call must report token counts. The orchestrator enforces per-brief caps. UI shows real-time cost meter.

---

## L5 — Distribution

**Purpose:** One bundle → many channels, atomically.

**Concrete tech (defaults):**

- **Bluesky** — `@atproto/api` (MIT). Free, no API key required. The MV1 default.
- **LinkedIn** — Marketing API + Posts API. OAuth 2.0, 60-day tokens, 100 calls/day/member.
- **Beehiiv** — REST API v2 + webhooks for newsletter.
- **YouTube** — Data API v3, Shorts via `#Shorts` tag.
- **TikTok** — Content Posting API (developer approval required).
- **X / Twitter** — paid tier ($0.20/URL post). Optional.
- **Instagram + Threads** — Meta Graph API (business accounts).
- **Farcaster** — `@neynar/nodejs-sdk` (MIT). Frames v2 supported.
- **Lens v3** — `@lens-protocol/client` v2 for web3 social.
- **Mastodon** — open ActivityPub.

**Interface (`@cis/core/src/distribute.ts`):**

```ts
export interface DistributionAdapter {
  readonly channel: ChannelId
  readonly capabilities: DistributionCapability[]
  publish(bundle: AssetBundle, signal?: AbortSignal): Promise<Publication>
  retract(pub: Publication): Promise<void>
}
```

**Atomic publish saga:** `p-retry` v5 + idempotency keys. All channels succeed, or none do — with compensating undos.

---

## L6 — Learning

**Purpose:** Close the loop. What worked → bias the next brief.

**Concrete tech (defaults):**

- **Storage:** AgentDB (`agentdb.dev`) — agent-native vector + structured store.
- **Pattern:** ReasoningBank (clean-room, inspired by ruflo) — store successful reasoning chains as retrievable patterns. Sliding 90-day window.
- **Performance ingest:** webhook from each platform's analytics + a daily pull job via `inngest` for durable workflows.
- **Reducer:** weekly job extracts patterns, writes to `learned/{format}/{channel}.json`, biases next brief generation.

**Interface (`@cis/core/src/learn.ts`):**

```ts
export interface LearningAdapter {
  readonly id: string
  recordOutcome(pub: Publication, signals: PerformanceSignal[]): Promise<void>
  recallPatterns(format: FormatId, channel: ChannelId): Promise<LearnedPattern[]>
  reduce(window: { since: ISODateTime; until: ISODateTime }): Promise<ReductionReport>
}
```

**Vanity-metric defense:** outcomes are weighted by *outcome* signals (replies, DMs, bookings, conversions) — not impressions. Configurable weights live in `lib/learn/weights.ts`.

---

## The orchestrator

The orchestrator is intentionally dumb. It reads CIP-typed messages, dispatches to adapters, and writes attestations. It does not generate content; it routes.

```ts
import { Conductor } from '@cis/core'

const conductor = new Conductor({
  substrate: sisSubstrate,
  capture: [whisperGroq, plasmoClipper, fileDropper],
  strategy: frontmatterStrategy,
  production: [anthropicProducer, vercelAiProducer, remotionProducer],
  distribution: [blueskyAdapter, linkedinAdapter, beehiivAdapter],
  learning: agentDbLearner,
})

const capture = await conductor.capture({ source: 'voice', audio: blob })
const brief = await conductor.brief(capture, { format: 'short-script', channel: 'bluesky' })
const bundle = await conductor.produce(brief)
const publication = await conductor.distribute(bundle, ['bluesky', 'linkedin'])
await conductor.attest(publication) // enforced — cannot publish without
```

Every step is observable. Every step is replay-safe. Every step writes to the palace.

---

## Multi-mode distribution

CIS ships in four distribution modes. The same substrate; different surfaces.

| Mode | Audience | Surface | Path |
|---|---|---|---|
| 1 | Web-first creators | Vercel template | [GenCreator-Studio](https://github.com/frankxai/GenCreator-Studio) |
| 2 | Terminal-first creators | Claude Code plugin | `starter-packs/claude-code/` |
| 3 | Chat-first creators | Claude Project | `starter-packs/claude-project/` |
| 4 | OpenAI-first creators | Custom GPT | `starter-packs/chatgpt-project/` |

The protocol is the same. The interface adapts to where the creator already lives.

---

## Versioning

CIS follows [SemVer 2.0](https://semver.org). The protocol (CIP) versions independently of the package versions. Breaking protocol changes increment CIP major. Breaking package API changes increment package major.

CIP v0.1 is alpha. CIP v1.0.0 lands when:

1. All 6 layers have at least one shipping adapter.
2. The protocol has survived 4 weeks of real production use.
3. One external creator boots CIS and ships content with it.

Until v1.0.0, expect adapter signatures to evolve. The intent stays.

---

## Open questions

These are RFCs the community can weigh in on. File issues with the `rfc:` prefix.

- Should L1 be pluggable (allow non-SIS substrates), or hard-coupled to SIS?
- Should the orchestrator support parallel agent fan-out within a single brief, or stay sequential for cost predictability?
- Should attestation be optional (per-publication flag), or always-on?
- Should learning be local-only by default, or opt-in to a federated pool of CIS instances?

Open questions are resolved by RFC. RFCs live in `docs/rfcs/`.

---

> *Composition over inheritance. Adapters over abstractions. The protocol is the artifact.*
