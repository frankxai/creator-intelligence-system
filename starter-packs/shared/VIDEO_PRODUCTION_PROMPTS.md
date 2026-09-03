# CIS Video Production Prompt Pack

These prompts are short operator contracts. The video-director skill and canonical production doctrine carry the deeper rules.

## 1. Recording Pack

```text
PACK: {{idea}}

Operate as CIS video director. Inspect relevant brand, product, evidence, prior content, and current market context before drafting.

Produce one high-conviction recording pack:
- thesis and audience tension;
- evidence/claims that must be verified;
- 3–5 hooks ranked by expected retention and strategic value;
- one selected script or beat sheet in natural spoken language;
- beat-level delivery cues;
- storyboard with a real visual plan for every beat;
- stable beat_id and asset_id values;
- generate/draft deterministic graphics and visual references before recording where possible;
- queue independent cinematic B-roll jobs in parallel;
- create/update the episode manifest.

Prefer real product/UI/evidence over decorative B-roll. Do not make the creator imagine visuals that can be prepared now.
```

## 2. Cut Latest

```text
CUT LATEST

Resolve the newest intended raw recording from the configured media inbox. Do not move raw media through model context.

Use transcript-native editing to:
- choose the strongest takes;
- remove failed takes, repetition, and dead space;
- preserve human cadence and idiosyncratic language;
- map the final spoken sequence to the existing beat_ids;
- identify only visuals invalidated by what was actually said;
- assemble prepared assets by asset_id;
- create the first 9:16 review cut.

Use one comprehensive Descript edit instruction rather than a chain of micro-edits. While transcription/editing runs, generate unresolved HyperFrames assets, real screenshots, and Higgsfield B-roll in parallel.

Return: review URL/reference, unresolved defects, and manifest state.
```

## 3. Render Missing

```text
RENDER MISSING: {{episode_id}}

Inspect unresolved visual slots only. For each slot choose the cheapest tool that preserves quality:
- real screenshot/screen recording for proof;
- HyperFrames for diagrams, charts, captions, typography, UI composites, transitions, and reusable branded motion;
- Higgsfield for cinematic/generated scenes and visual metaphors;
- Hypernatural only when a fully synthetic storyboard lane is genuinely simpler.

Batch independent jobs. Never regenerate accepted assets without a reason. Update asset_id status and provenance in the manifest.
```

## 4. Review

```text
REVIEW: {{episode_id}}

Act as a ruthless final editorial board. Review only material shipping risks:
- signal/originality;
- factual support and correct screenshots;
- hook/tension;
- voice authenticity;
- pacing and information density;
- evidence over decoration;
- brand design/motion/caption contract;
- audio, safe areas, aspect ratio, cover;
- rights/provenance;
- CTA;
- attestation completeness.

Classify each finding BLOCK / FIX / ACCEPT. Recommend SHIP when no BLOCK remains. Do not invent polish work to keep the loop open.
```

## 5. Ship

```text
SHIP: {{episode_id}}

Render the approved master and required platform variants. Generate native platform copy from the same thesis without changing the claim. Publish only through configured approval-safe distribution adapters.

Persist:
- publication URLs/IDs;
- final manifest;
- attestation;
- source and asset references;
- hook/format/CTA metadata for later learning.
```

## 6. Learn

```text
LEARN: {{episode_id}}

Ingest available outcome signals. Explain what should change next, not merely what performed.

Attribute outcomes to topic, hook, format, length, visual grammar, CTA, and channel where evidence permits. Distinguish repeatable pattern from outlier. Promote only validated patterns into the next PACK context.
```

## 7. Spontaneous founder recording

```text
CUT SPONTANEOUS: {{source}}

Treat the founder's raw performance as the primary creative source. Transcribe, locate the strongest coherent thesis, preserve surprising phrasing, and construct a 30–90 second cut around one tension.

Only after selecting the spoken cut, build the episode manifest and generate the smallest visual layer needed to make the idea clearer, more credible, and more watchable. Do not over-produce a strong human moment.
```
