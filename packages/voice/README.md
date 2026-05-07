# @cis/voice

Brand voice abstraction + audit. Single source of truth for voice config in a CIS instance.

## Install

```bash
pnpm add @cis/voice
```

## Usage

```ts
import { DEFAULT_VOICE, auditVoice, buildVoiceSystemPrompt, extendProfile } from '@cis/voice'

// Audit a draft
const issues = auditVoice('This will revolutionize your business with cutting-edge AI.')
console.log(issues)
// → [
//   { kind: 'banned', term: 'revolutionize', index: 10, context: '...' },
//   { kind: 'banned', term: 'cutting-edge', index: 38, context: '...' },
// ]

// Build a Claude / OpenAI system prompt
const systemPrompt = buildVoiceSystemPrompt(DEFAULT_VOICE, 'linkedin')

// Compose a custom profile
const myVoice = extendProfile(DEFAULT_VOICE, {
  id: 'my-brand',
  northStar: 'Bold. Specific. Earned.',
  bannedPhrases: ['journey', 'transformation'],
  quarantinedTerms: ['some-other-brand-name'],
})
```

## Apply prompt caching

When calling Anthropic SDK, mark the voice system prompt as ephemeral-cacheable:

```ts
const message = await anthropic.messages.create({
  model: 'claude-sonnet-4-6',
  max_tokens: 4096,
  system: [
    {
      type: 'text',
      text: buildVoiceSystemPrompt(myVoice, 'blog'),
      cache_control: { type: 'ephemeral' },
    },
  ],
  messages: [{ role: 'user', content: brief }],
})
```

The voice fragment is stable across requests. Prompt caching cuts cost by ~90% on subsequent calls within the cache window.

## Schema

See `src/index.ts` for the full `VoiceProfile` shape.

## License

MIT.
