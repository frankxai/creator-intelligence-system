/**
 * Creator Intelligence Protocol (CIP) v0.1 — TypeScript types.
 *
 * These are the canonical shapes every CIS artifact must conform to.
 * The JSON Schema mirror lives at `src/schemas/cip-v0.1.json`.
 *
 * Versioning: types in this file are part of the protocol surface.
 * Breaking changes go through an RFC and bump the protocol version.
 */

// ============================================================================
// Identity
// ============================================================================

export interface DIDIdentity {
  /** Decentralized Identifier, e.g. "did:plc:...", "did:web:frankx.ai" */
  did: string
  /** Human-readable handle, e.g. "frankx.bsky.social" */
  handle?: string
  /** Multibase-encoded public key for verification */
  publicKey: string
}

// ============================================================================
// Common
// ============================================================================

/** ISO 8601 string */
export type ISODateTime = string

/** ULID — sortable, URL-safe, 128-bit unique identifier */
export type ULID = string

export interface MediaRef {
  url: string
  contentType: string // MIME type — REQUIRED, never guessed
  bytes?: number
  width?: number
  height?: number
  durationMs?: number
}

// ============================================================================
// L2 — Capture
// ============================================================================

export type CaptureSource =
  | 'voice'
  | 'web-clip'
  | 'file-drop'
  | 'notion'
  | 'obsidian'
  | 'email'
  | 'manual'
  | 'cli'

export type CaptureMode = 'sync' | 'async'

export interface CaptureInput {
  source: CaptureSource
  identity: DIDIdentity
  rawText?: string
  audio?: { ref: MediaRef } | { blob: Blob }
  url?: string
  files?: MediaRef[]
  metadata?: Record<string, unknown>
}

export interface Capture {
  id: ULID
  source: CaptureSource
  capturedAt: ISODateTime
  identity: DIDIdentity
  transcript?: string
  rawText?: string
  mediaRefs: MediaRef[]
  metadata: Record<string, unknown>
  attestation: Attestation
}

// ============================================================================
// L3 — Strategy
// ============================================================================

export type FormatId = string // ref to format library, e.g. "talking-head-90s"
export type AudienceId = string
export type ChannelId =
  | 'bluesky'
  | 'linkedin'
  | 'x'
  | 'threads'
  | 'instagram'
  | 'youtube'
  | 'tiktok'
  | 'farcaster'
  | 'lens'
  | 'mastodon'
  | 'beehiiv'
  | 'rss'
  | 'mcp'
  | string // open extension point

export type BriefStatus =
  | 'draft'
  | 'ready'
  | 'producing'
  | 'staged'
  | 'published'
  | 'archived'

export interface Brief {
  id: ULID
  captureRefs: ULID[]
  format: FormatId
  audience?: AudienceId
  channel: ChannelId
  voicePreset: string
  hook?: string
  notes?: string
  scheduledFor?: ISODateTime
  agentChain: AgentStep[]
  status: BriefStatus
  attestation: Attestation
}

export interface FormatDefinition {
  id: FormatId
  name: string
  channel: ChannelId
  approxLengthMs?: number
  approxLengthChars?: number
  hookPattern?: string
  structure: string[]
  voicePreset: string
  exampleSlugs?: string[]
  notes?: string
}

export interface AudienceDefinition {
  id: AudienceId
  name: string
  description: string
  pains: string[]
  desiredOutcomes: string[]
  channels: ChannelId[]
}

// ============================================================================
// L4 — Production
// ============================================================================

export type ArtifactKind = 'text' | 'image' | 'video' | 'audio' | 'frame'

export interface Artifact {
  kind: ArtifactKind
  contentType: string
  bytes?: number
  url?: string
  inlineText?: string
  alt?: string
  metadata?: Record<string, unknown>
}

export interface AssetBundle {
  id: ULID
  briefId: ULID
  channel: ChannelId
  artifacts: Artifact[]
  captions?: Partial<Record<ChannelId, string>>
  schemaJsonLd?: Record<string, unknown>
  voiceIssues: VoiceIssue[]
  costReport: CostReport
  attestation: Attestation
}

export interface VoiceIssue {
  kind: 'banned' | 'quarantine' | 'tone' | 'length'
  term?: string
  severity: 'warn' | 'reject'
  message: string
  context?: string
}

export interface CostReport {
  totalUsd: number
  byProvider: Array<{
    provider: string
    model?: string
    inputTokens?: number
    outputTokens?: number
    images?: number
    durationSeconds?: number
    usd: number
  }>
}

export interface ProductionCapability {
  kind: ArtifactKind
  channels?: ChannelId[]
}

export interface ProductionStep {
  agent: string
  step: string
  startedAt: ISODateTime
  endedAt?: ISODateTime
  model?: ModelInvocation
  artifacts?: Artifact[]
  voiceIssues?: VoiceIssue[]
  notes?: string
}

// ============================================================================
// L5 — Distribution
// ============================================================================

export interface DistributionCapability {
  channel: ChannelId
  artifactKinds: ArtifactKind[]
  supportsScheduled: boolean
  supportsRetract: boolean
}

export interface Publication {
  id: ULID
  bundleId: ULID
  channel: ChannelId
  url: string
  postedAt: ISODateTime
  identity: DIDIdentity
  platformIds: Record<string, string>
  attestation: Attestation
}

export interface PublicationRef {
  id: ULID
  channel: ChannelId
  url: string
  postedAt: ISODateTime
}

// ============================================================================
// L6 — Learning
// ============================================================================

export type PerformanceSignalKind =
  | 'impressions'
  | 'reactions'
  | 'replies'
  | 'reposts'
  | 'saves'
  | 'clicks'
  | 'completes'
  | 'watch-time-ms'
  | 'conversions'
  | 'subscribes'
  | 'bookings'
  | 'revenue-usd'

export interface PerformanceSignal {
  kind: PerformanceSignalKind
  value: number
  measuredAt: ISODateTime
  channel: ChannelId
  source?: string // analytics provider
}

export interface LearnedPattern {
  id: ULID
  format: FormatId
  channel: ChannelId
  pattern: string
  evidence: PublicationRef[]
  windowStart: ISODateTime
  windowEnd: ISODateTime
  signal: PerformanceSignalKind
  weight: number // 0..1
}

export interface ReductionReport {
  windowStart: ISODateTime
  windowEnd: ISODateTime
  publicationsScanned: number
  patternsDetected: number
  patternsRetained: number
  patternsDropped: number
}

// ============================================================================
// Attestation — the moat
// ============================================================================

export interface AgentStep {
  agent: string
  step: string
  startedAt: ISODateTime
  endedAt: ISODateTime
  inputs?: Array<{ kind: string; ref?: string }>
  outputs?: Array<{ kind: string; ref?: string }>
}

export interface ModelInvocation {
  provider: string
  model: string
  inputTokens?: number
  outputTokens?: number
  imageCount?: number
  audioSeconds?: number
  costUsd?: number
}

export interface HumanReview {
  did: string
  decision: 'approve' | 'edit' | 'reject'
  reviewedAt: ISODateTime
  comment?: string
}

export interface AttestationRendering {
  format: 'short' | 'long' | 'compressed' | 'custom'
  templateOverride?: string
}

export interface Attestation {
  /** Protocol version */
  v: 1
  artifactId: ULID
  artifactKind: ArtifactKind | 'capture' | 'brief' | 'bundle' | 'publication'
  /** The creator's brief, verbatim — or a redaction descriptor */
  humanIdea: string | { redacted: true; hashHex: string }
  /** Every agent that touched this artifact, in order */
  agentChain: AgentStep[]
  /** Every LLM call, with token + cost telemetry */
  models: ModelInvocation[]
  /** Every human approval / edit / rejection */
  reviewers: HumanReview[]
  /** When this attestation was signed */
  signedAt: ISODateTime
  /** ed25519 signature over canonical JSON */
  signature: string
  /** The signer's DID */
  signerDid: string
  /** Optional: parent attestations this one composes */
  parents?: ULID[]
  /** Optional: rendering hint for downstream display */
  rendering?: AttestationRendering
}

// ============================================================================
// Substrate — L1
// ============================================================================

export type PalaceScope =
  | 'captures'
  | 'briefs'
  | 'bundles'
  | 'publications'
  | 'patterns'
  | 'attestations'
  | string

export interface MemoryRef {
  scope: PalaceScope
  id: ULID
  uri: string
}

export interface MemoryRecord {
  ref: MemoryRef
  payload: unknown
  storedAt: ISODateTime
}

export interface GovernanceQuestion {
  kind: string
  payload: Record<string, unknown>
}

export interface GovernanceVerdict {
  decision: 'allow' | 'deny' | 'review'
  rationale: string
  reviewers?: string[]
}

// ============================================================================
// Adapter contracts (re-exported to give a single import surface)
// ============================================================================

export interface Substrate {
  id: string
  identity(): Promise<DIDIdentity>
  remember(scope: PalaceScope, payload: unknown): Promise<MemoryRef>
  recall(scope: PalaceScope, query: string): Promise<MemoryRecord[]>
  attest(artifact: { id: ULID; kind: Attestation['artifactKind'] }, chain: AgentStep[]): Promise<Attestation>
  govern(decision: GovernanceQuestion): Promise<GovernanceVerdict>
}

export interface CaptureAdapter {
  readonly id: string
  readonly modes: CaptureMode[]
  readonly sources: CaptureSource[]
  ingest(input: CaptureInput): Promise<Capture>
}

export interface StrategyContext {
  recentPublications?: PublicationRef[]
  patterns?: LearnedPattern[]
  calendarSlot?: ISODateTime
}

export interface StrategyAdapter {
  readonly id: string
  brief(capture: Capture, context: StrategyContext): Promise<Brief>
  reformat(briefId: ULID, format: FormatId): Promise<Brief>
  schedule(brief: Brief, slot: ISODateTime): Promise<Brief>
}

export interface ProductionAdapter {
  readonly id: string
  readonly capabilities: ProductionCapability[]
  produce(brief: Brief, signal?: AbortSignal): AsyncIterable<ProductionStep>
}

export interface DistributionAdapter {
  readonly channel: ChannelId
  readonly capabilities: DistributionCapability
  publish(bundle: AssetBundle, signal?: AbortSignal): Promise<Publication>
  retract(pub: Publication): Promise<void>
}

export interface LearningAdapter {
  readonly id: string
  recordOutcome(pub: Publication, signals: PerformanceSignal[]): Promise<void>
  recallPatterns(format: FormatId, channel: ChannelId): Promise<LearnedPattern[]>
  reduce(window: { since: ISODateTime; until: ISODateTime }): Promise<ReductionReport>
}

// ============================================================================
// Conductor — the orchestrator
// ============================================================================

export interface ConductorConfig {
  substrate: Substrate
  capture: CaptureAdapter[]
  strategy: StrategyAdapter
  production: ProductionAdapter[]
  distribution: DistributionAdapter[]
  learning: LearningAdapter
}

export const CIP_VERSION = '0.1.0' as const
