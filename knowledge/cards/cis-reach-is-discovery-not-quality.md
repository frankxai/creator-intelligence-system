---
id: cis-reach-is-discovery-not-quality
type: definition
domain: creator
license: platform-docs-commentary
public_ok: true
hitl_status: pending_human_review
source:
  title: Understand your YouTube video reach (YouTube Help)
  url: https://support.google.com/youtube/answer/9314355?hl=en
  retrieved: "2026-08-21"
  quote: >-
    The Reach tab in YouTube Analytics is your key to understanding how
    viewers find your content. It provides a quick snapshot of key metrics
    like click-through-rate, watch time, views, and more.
failure_modes:
  - Optimizing CTR while watch time collapses (clickbait without payoff)
  - Treating Reach as a taste score
agent_directive: >-
  Hook tools may use CTR as a discovery diagnostic only. A ship decision
  requires a retention/watch-time companion metric. CTR-only “winners” fail.
---

# Reach measures how people found it

YouTube’s own Help page defines Reach as **discovery**: CTR, watch time,
views, traffic sources. It is not a quality rubric.

**Agent use:** CIS strategy layer should split L3 into (1) packaging /
impressions→click, (2) fulfillment / click→watch. Mixing them produces
false “viral” wins.
