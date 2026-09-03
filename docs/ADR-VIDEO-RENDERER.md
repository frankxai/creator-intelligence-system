# ADR — Default deterministic video renderer

**Date:** 2026-09-03  
**Status:** Accepted for new CIS video work

## Context

CIS needs a programmatic rendering layer for diagrams, captions, UI composites, typography, charts, motion systems, and repeatable video templates. The stack previously listed Remotion and HeyGen HyperFrames as peer options.

The requirement has changed from "programmatic video exists" to **"agents can reliably author, inspect, test, and render branded video with minimal human timeline work."**

## Decision

Use **HyperFrames as the default deterministic renderer for new CIS / GenCreator video production**.

Keep **Remotion as a supported specialist and compatibility adapter**.

Do not delete or mechanically port existing Remotion projects.

## Why HyperFrames wins the default slot

1. **Agent-native authoring.** HTML/CSS/JS is a native strength of coding agents, and HyperFrames ships dedicated agent skills and routing workflows.
2. **Deterministic seeking.** Renderers seek exact frames rather than relying on wall-clock playback, which is better suited to CI, regression testing, and automated production.
3. **Open composition format.** Source remains ordinary web technology with timing metadata instead of a proprietary timeline artifact.
4. **Broad motion surface.** GSAP, CSS, Lottie, Three.js, Anime.js, WAAPI, video/audio elements, captions, charts, overlays, and ordinary DOM components can live in one composition.
5. **Low-friction preview.** HTML compositions can be inspected in-browser without making the creator operate a conventional NLE.
6. **License posture.** HyperFrames is Apache-2.0 and fits CIS's open, redistributable reference-stack philosophy.
7. **Skill ecosystem.** The upstream skills include core composition, CLI/dev loop, media preprocessing, registry/components, website-to-video, and Remotion-to-HyperFrames migration paths.

## Where Remotion still wins

Use Remotion when:

- the team already has a mature Remotion composition that works;
- the video is fundamentally a React application or tightly coupled to a React component system;
- a specific Remotion package/integration is materially better for the job;
- migration cost exceeds the maintenance or licensing benefit;
- a downstream user explicitly chooses Remotion.

## Where neither renderer should be used

- **Talking-head semantic edit:** Descript.
- **Cinematic generated B-roll / synthetic scenes:** Higgsfield or a model-specific generator.
- **Remote interview capture:** Riverside.
- **Fully synthetic storyboard-first fast lane:** Hypernatural can be an optional adapter.

The renderer should not become a universal hammer.

## Operating consequence

For new video formats:

1. define the visual grammar in a `frame.md` / project design contract;
2. install/update the HyperFrames core skills;
3. generate a reusable composition family;
4. lint and render deterministically;
5. expose the renderer through the CIS production adapter boundary;
6. keep every asset reference and model/tool invocation inside normal CIP attestation.

Recommended agent bootstrap:

```bash
npx hyperframes skills update
```

## Revisit trigger

Re-evaluate this ADR only when one of the following changes materially:

- HyperFrames maintenance or license posture;
- deterministic render reliability;
- CIS requires a feature only another renderer provides;
- measured production cost or failure rate is worse than the alternative across a representative batch.

Vendor novelty alone is not a reason to change the default.