/**
 * @cis/voice — brand voice abstraction.
 *
 * Voice config is single-source. Every CIS adapter loads voice from here.
 * Custom voice profiles compose the base profile with overrides.
 *
 * Inspired by FrankX's lib/voice/frankx-voice.ts; refactored creator-agnostic.
 */

export interface VoiceProfile {
  /** Profile id, e.g. "frankx", "default", "yourname" */
  id: string
  /** Three-word north-star description */
  northStar: string
  /** Brand attributes (key → 1-line description) */
  attributes: Record<string, string>
  /** Things to do */
  dos: readonly string[]
  /** Things to avoid */
  donts: readonly string[]
  /** Phrases that are AI-slop or low-quality, audited at every boundary */
  bannedPhrases: readonly string[]
  /** Terms that belong to a different brand and must never appear here */
  quarantinedTerms: readonly string[]
  /** Reference brands the voice sits inside */
  referenceBrands?: ReadonlyArray<{ name: string; why: string }>
  /** Per-channel tone adapters */
  channelTones?: Partial<Record<string, string>>
}

/**
 * Sensible default voice profile for first-run setups. Creators replace with
 * their own; the shape is what matters, not the content.
 */
export const DEFAULT_VOICE: VoiceProfile = {
  id: 'default',
  northStar: 'Clear. Useful. Honest.',
  attributes: {
    clarity: 'every sentence carries one idea',
    utility: 'the reader can act on what they read',
    honesty: 'evidence over claims; receipts over rhetoric',
  },
  dos: [
    'Lead with the result',
    'Use concrete numbers and examples',
    'Show, do not tell',
    'Confident, not grandiose',
  ],
  donts: [
    'Hype language without evidence',
    'Self-help guru tone',
    'Two equal CTAs (indecision)',
    'Fake urgency or pricing tricks',
  ],
  bannedPhrases: [
    'delve',
    'delve into',
    'dive into',
    'dive deep',
    "it's worth noting",
    'it is worth noting',
    'certainly',
    'absolutely',
    'in conclusion',
    'navigate the landscape',
    'unleash',
    'harness the power',
    "in today's fast-paced",
    'cutting-edge',
    'game-changer',
    'revolutionize',
    'paradigm shift',
    'leverage synergies',
  ],
  quarantinedTerms: [],
  channelTones: {
    blog: 'Editorial. Long-form. Section-anchored.',
    linkedin: 'Professional density. Lead with the receipt.',
    bluesky: 'Conversational, not casual.',
    threads: 'Casual but sharp.',
    x: 'Compressed. Hook in line one.',
    youtube: 'Spoken cadence. Open with the result.',
    email: 'One thing per email.',
    newsletter: 'Curated. Three-to-five items.',
  },
}

export interface VoiceIssue {
  kind: 'banned' | 'quarantine'
  term: string
  index: number
  context: string
}

/**
 * Audit a draft against banned and quarantined lists.
 * Returns issues found; empty array means the draft passes.
 */
export function auditVoice(
  draft: string,
  profile: VoiceProfile = DEFAULT_VOICE,
): VoiceIssue[] {
  const issues: VoiceIssue[] = []
  const lower = draft.toLowerCase()

  for (const term of profile.bannedPhrases) {
    let idx = lower.indexOf(term)
    while (idx !== -1) {
      issues.push({
        kind: 'banned',
        term,
        index: idx,
        context: draft.slice(Math.max(0, idx - 40), idx + term.length + 40),
      })
      idx = lower.indexOf(term, idx + 1)
    }
  }

  for (const term of profile.quarantinedTerms) {
    let idx = lower.indexOf(term)
    while (idx !== -1) {
      issues.push({
        kind: 'quarantine',
        term,
        index: idx,
        context: draft.slice(Math.max(0, idx - 40), idx + term.length + 40),
      })
      idx = lower.indexOf(term, idx + 1)
    }
  }

  return issues
}

/**
 * Compose a system prompt fragment encoding the voice profile.
 * Apply with prompt caching when calling Anthropic / OpenAI.
 */
export function buildVoiceSystemPrompt(
  profile: VoiceProfile = DEFAULT_VOICE,
  channel?: string,
): string {
  const channelLine =
    channel && profile.channelTones?.[channel]
      ? `\n\nChannel: ${channel} — ${profile.channelTones[channel]}`
      : ''

  return `You are writing in the "${profile.id}" voice profile.

North star: ${profile.northStar}

Brand attributes:
${Object.entries(profile.attributes)
  .map(([k, v]) => `- ${k}: ${v}`)
  .join('\n')}

Voice DOs:
${profile.dos.map((d) => `- ${d}`).join('\n')}

Voice DON'Ts:
${profile.donts.map((d) => `- ${d}`).join('\n')}

Banned phrases (do NOT use under any circumstance):
${profile.bannedPhrases.map((p) => `- "${p}"`).join('\n')}

${
  profile.quarantinedTerms.length > 0
    ? `Quarantined terms (these belong to a different brand and must NEVER appear):\n${profile.quarantinedTerms
        .map((p) => `- "${p}"`)
        .join('\n')}\n\n`
    : ''
}${
    profile.referenceBrands?.length
      ? `Reference brands the voice sits inside:\n${profile.referenceBrands
          .map((r) => `- ${r.name}: ${r.why}`)
          .join('\n')}\n\n`
      : ''
  }Restraint test before any sentence ships:
1. Does removing this sentence make the draft worse?
2. Does it carry meaning, not decoration?
3. Will the reader notice if it's gone?
If any answer is no, cut it.${channelLine}`
}

/**
 * Compose a child profile that extends a base profile with overrides.
 * Useful for sub-brands or topical voice variations.
 */
export function extendProfile(
  base: VoiceProfile,
  overrides: Partial<VoiceProfile> & { id: string },
): VoiceProfile {
  return {
    ...base,
    ...overrides,
    attributes: { ...base.attributes, ...(overrides.attributes ?? {}) },
    dos: [...base.dos, ...(overrides.dos ?? [])],
    donts: [...base.donts, ...(overrides.donts ?? [])],
    bannedPhrases: [
      ...base.bannedPhrases,
      ...(overrides.bannedPhrases ?? []),
    ],
    quarantinedTerms: [
      ...base.quarantinedTerms,
      ...(overrides.quarantinedTerms ?? []),
    ],
    channelTones: { ...base.channelTones, ...(overrides.channelTones ?? {}) },
  }
}
