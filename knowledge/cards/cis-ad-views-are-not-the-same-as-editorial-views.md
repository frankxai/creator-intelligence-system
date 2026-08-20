---
id: cis-ad-views-are-not-the-same-as-editorial-views
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
    If your video is used as an ad on YouTube, you’ll see “YouTube
    advertising” as a traffic source. Views from skippable ads longer than
    10 seconds are counted if they're watched for 30 seconds or until
    they're finished. Non-skippable ads never qualify as views in YouTube
    Analytics.
failure_modes:
  - Celebrating view spikes that are paid inventory
  - Comparing ad-driven CTR to organic Search CTR
agent_directive: >-
  Analytics summaries must split YouTube advertising traffic from organic
  sources before any “it took off” claim.
---

# Paid inventory ≠ earned attention

The Help page states counting rules for ads vs Analytics views.
Non-skippable ads never qualify as views in Analytics.

**Agent use:** CIS learn-loop (L6) must not train on mixed paid+organic
view totals as if they were one skill signal.
