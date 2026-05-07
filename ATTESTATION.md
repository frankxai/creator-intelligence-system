# Attestation — the Transparency Moat

> Every published piece carries a verifiable record of human idea, models used, agent chain, and reviewers. This is the moat nobody else builds.

---

## The trust crisis

By 2027, the average internet reader will assume any text was written by a model unless proven otherwise. By 2028, they will assume the same of every image, video, and song. The trust premium for content with verifiable human authorship will be enormous, and the discount for content without it will be catastrophic.

Every existing content tool — Buffer, Hootsuite, Hypefury, Adobe GenStudio, Notion AI, Webflow Designer — is racing to make AI generation faster. None is solving the trust gap that comes after.

CIS does both. Generation faster *and* trust verifiable. Together. Inseparably.

---

## The attestation contract

Every Publication produced by a CIS instance carries an `Attestation` object. It records:

1. **The human idea** — verbatim. The creator's brief, voice memo transcript, or sentence that started this piece.
2. **The agent chain** — every adapter that touched the artifact, in order, with timestamps.
3. **The models** — every LLM call, the model name, the version, input/output tokens, dollar cost.
4. **The reviewers** — every human who approved, edited, or rejected, with timestamps and comments.
5. **A signature** — ed25519 over a canonical encoding, signed by the creator's DID key.

The attestation is **mandatory**. The orchestrator refuses to publish without one. Distribution adapters refuse to send without one. There is no `--skip-attest` flag. By design.

---

## Two failure modes attestation prevents

### 1. The "I didn't write that" disaster

An audience member screenshots a CIS-published post that contained an inaccuracy. The creator says: "I didn't write that, my agent did." The audience trusts the creator less for not knowing, less for trying to dodge, and less for using AI without saying so.

With attestation, that conversation looks different:

> "This was drafted by claude-sonnet-4-6, edited by my hook-author and voice-guard agents, and approved by me at 2026-05-09T07:00Z. The inaccuracy is on me — I approved it. Here's the correction."

The same fact. A different relationship with the audience.

### 2. The "is this even real?" cynicism

The audience starts assuming everything is generated. Trust evaporates everywhere, including from creators who were honest the whole time.

With attestation, the audience can verify. Click the `cis://attest/...` link, see the chain. The creator who has nothing to hide gets a permanent moat over the creator who hides.

---

## The rendering contract

By default, every Publication renders a one-line attestation footer at the bottom of the channel-native caption. Examples:

**LinkedIn:**

> [post body]
>
> ---
> Captured by Frank · Drafted by claude-sonnet-4-6 · Edited by hook-author + voice-guard · Reviewed by Frank · cis://attest/01HX9...

**YouTube description:**

> [description]
>
> ---
> Provenance: human idea by Frank → script by claude-sonnet-4-6 → voice-guard audit → manual review by Frank → published. Verify: cis://attest/01HX9...

**Bluesky (compressed for character limit):**

> [post body]
>
> 🔗 cis://attest/01HX9...

**Newsletter:**

> [body]
>
> ---
> *This issue was captured by Frank, drafted by claude-sonnet-4-6 via Frank's Creator Intelligence System, audited for voice and brand, and reviewed by Frank before sending. Full provenance: cis://attest/01HX9...*

The exact text is configurable per format. The presence of the attestation is not.

---

## How verification works

The `cis://attest/{id}` URI resolves to a public attestation document at:

```
https://<creator-domain>/.well-known/cis/attestations/{id}
```

The document is canonical-JSON-encoded, signed, and includes the creator's DID public key for verification. A simple verifier (which CIS ships as `@cis/verify`):

```ts
import { verify } from '@cis/verify'

const attestation = await fetch('https://frankx.ai/.well-known/cis/attestations/01HX9...').then(r => r.json())
const result = await verify(attestation)

if (result.ok) {
  console.log('Verified:', {
    creator: result.signerDid,
    humanIdea: result.humanIdea,
    models: result.models.map(m => m.model),
    publishedAt: result.signedAt,
  })
}
```

The verifier runs in browser, Node, Deno, or Bun. No API call needed beyond fetching the document.

---

## Privacy considerations

Attestations are designed to be public. Some creators may want partial privacy — for example, redacting the verbatim humanIdea while keeping the agent chain and models visible.

CIP supports this via field-level redaction:

```ts
{
  v: 1,
  artifactId: '...',
  humanIdea: { redacted: true, hashHex: 'a3f...' }, // SHA-256 of original
  agentChain: [...],
  models: [...],
  reviewers: [...],
  signedAt: '...',
  signature: '...',
  signerDid: '...',
}
```

The hash lets the creator prove later (in disputes) what the original idea was, without showing it now.

---

## What attestation is NOT

- **Not copyright registration.** CIS does not file claims with any registry. If you need copyright, do that separately.
- **Not a hashing service for stolen content.** Attestations describe how a piece was *made*, not whether the inputs were lawfully sourced.
- **Not a deepfake defense.** A signed attestation says "this came from this creator's CIS instance." It does not verify that any claims inside the content are factually true.
- **Not anti-AI.** CIS is an AI-first creator stack. Attestation says "yes, AI helped — here's exactly how" — proudly, transparently.

---

## Adoption strategy

CIS attestations work even if no other tool implements CIP. The verification page is HTML; the URI is HTTP; the cryptography is ed25519.

If a second tool implements CIP, attestations cross-verify. If a hundred do, attestation becomes the norm — and the trust premium accrues to the creators who started early.

The thesis: by mid-2027, audiences will start checking attestations. By 2028, the absence of one will be a yellow flag. By 2030, it will be a red flag.

If you build with CIS in 2026, you are early. Early gets the moat.

---

## Roadmap

- **v0.1 (now)** — local file-based attestations, single-creator signing.
- **v0.2** — well-known endpoint resolution, browser verifier, CIP `User-Agent` discovery.
- **v0.3** — multi-reviewer attestation (collaborative content), redaction support.
- **v1.0** — RFC-frozen schema, formal cryptographic spec, multi-signature attestations.
- **v1.x** — federated cross-creator attestation pools, web3-anchored timestamps (optional, opt-in).

---

> *Provenance is the only honest answer to the trust crisis. Build for it now.*
