---
name: cis-video-director
description: Plan, direct, assemble, review, and learn from human-led or synthetic video using CIS. Use for recording packs, founder shorts, reels, explainers, cinematic B-roll, CUT LATEST, video QA, and agentic video-production workflows.
---

# CIS Video Director

Use this skill when video work must move through the CIS production system rather than becoming a one-off edit.

## Read first

1. `docs/VIDEO_PRODUCTION_OS.md`
2. `docs/ADR-VIDEO-RENDERER.md`
3. `SPEC.md` and `ATTESTATION.md` when the work will be published
4. the active brand voice/design contract

## Core posture

The creator is the source of signal, performance, and final taste. The system is the production company.

Do not ask the creator to perform work that a deterministic renderer, agent, or generation adapter can own reliably.

Do not put raw multi-GB video into model context. Operate on references, transcripts, scene summaries, hashes, manifests, and selected frames.

## Choose one production mode

### A. Human-led / visual-first

Default for founder content.

1. research the claim and audience tension;
2. generate 3–5 hooks and select one;
3. create a beat-level recording pack;
4. generate or draft the visuals *before* recording where feasible;
5. write an episode manifest with stable `beat_id` and `asset_id` values;
6. record the human performance;
7. reconcile the transcript to the planned beats;
8. assemble and QA.

### B. Human-led / spontaneous

Use when the creator riffs without a script.

1. ingest the raw recording;
2. transcribe and identify candidate claims/beats;
3. choose the strongest coherent thesis;
4. create the manifest after capture;
5. preserve idiosyncratic human phrasing where it carries signal;
6. build only the visuals the final cut actually needs.

### C. Fully synthetic

Use for faceless channels, concept tests, or campaigns that do not need the founder's physical presence.

Create the storyboard and assets first, then route to HyperFrames, Higgsfield, Hypernatural, or another approved adapter based on the visual job.

### D. Remote interview / long-form

Use a remote-capture layer first, then enter normal transcript/manifest production. Do not force short-form assumptions onto a long conversation.

## Tool router

Route by job.

- **Descript** — transcript, take selection, dead air, narrative A-roll edit, initial assembly.
- **HyperFrames** — default deterministic renderer: diagrams, charts, captions, titles, UI composites, kinetic type, branded motion, presenter+visual layouts, repeatable templates.
- **Remotion** — compatibility/specialist renderer when an existing React composition or React-first requirement makes it the better tool.
- **Higgsfield** — cinematic/generated B-roll, visual metaphors, reference-consistent synthetic shots, high-impact motion inserts.
- **Hypernatural** — optional end-to-end synthetic/storyboard lane; do not make it the default founder A-roll editor.
- **Real screenshots / screen recordings** — prefer for proof of real products, repos, results, interfaces, or experiments.
- **Figma / Canva** — design authority and source references; avoid recurring manual timeline assembly there.
- **Google Drive** — raw media ingress; reference URLs instead of moving bytes through chat.

## Operator intents

### `PACK <idea>`

Return:

1. thesis / audience tension;
2. evidence required;
3. hook bank;
4. selected script or beat sheet;
5. recording cues;
6. storyboard with actual or planned visual assets;
7. episode manifest;
8. unresolved generation jobs.

Prepare independent visual jobs in parallel.

### `CUT LATEST`

Resolve the latest intended source media, then:

1. transcribe;
2. select strongest takes;
3. remove dead air, repetitions, and failed attempts;
4. preserve human cadence rather than over-smoothing language;
5. map the final spoken sequence to `beat_id`s;
6. identify only missing or invalidated assets;
7. send one comprehensive semantic edit instruction rather than many micro-edits.

### `RENDER MISSING`

For each unresolved visual:

1. decide whether it should be real evidence, deterministic motion, or generated cinema;
2. route accordingly;
3. batch independent generation jobs;
4. keep accepted assets immutable unless the user or QA rejects them;
5. update the manifest status.

### `REVIEW`

Run these gates:

- signal / originality;
- factual support;
- voice authenticity;
- hook strength;
- pacing and visual-information density;
- evidence over decoration;
- design-contract compliance;
- audio / captions / safe area;
- provenance / rights;
- CTA coherence;
- attestation completeness.

Return only material defects. Do not create endless polish loops.

### `SHIP`

Render approved masters and variants, write platform copy, publish only through approved adapters, then persist attestation and learning metadata.

### `LEARN`

Attach outcomes to:

- hook;
- topic;
- format;
- length;
- visual treatment;
- CTA;
- distribution channel.

Promote a pattern only after repeat evidence. Do not confuse a single viral outlier with a reusable rule.

## Parallelism rule

Never serialize work that does not depend on the previous output.

Examples:

- generate visuals while the creator records;
- render deterministic assets while Drive uploads;
- draft thumbnail/copy variants while transcription runs;
- batch independent Higgsfield shots;
- fact-check claims while Descript builds the first cut.

## Descript discipline

Prefer a maximum of:

1. import/transcription;
2. one comprehensive first-edit instruction;
3. one consolidated revision after QA.

Use Descript as a semantic assembler, not as the visual design brain.

## Output contract

Every production pass should leave the system more legible than before. Update or emit:

- episode state;
- manifest;
- asset statuses and references;
- review decision;
- attestation steps;
- learning record after publication.

The desired creator experience is:

> **PACK → record → upload once → CUT LATEST → review → SHIP.**