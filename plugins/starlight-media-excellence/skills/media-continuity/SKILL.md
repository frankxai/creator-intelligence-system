---
name: media-continuity
description: Use to resume or hand off an existing media campaign, content production project, render run, DAM ingestion, GitHub skill/plugin implementation or cross-chat creative task, including requests for automatic hooks or making future agents follow a playbook.
---

# Cross-chat Continuity and Handoff

Never treat the conversation transcript as the complete durable source of truth. Search relevant authorized GitHub, Notion, Drive, asset registry and deployment data; fetch exact artifacts and citations before claiming current status. Respect tenant, brand and audience boundaries.

## On every relevant new production task

1. Identify work/campaign ID and owning repository; find the most recent accepted manifest and latest complete source/output receipt. Do not infer from same-titled docs alone.
2. Classify each work item as `PROPOSED`, `SOURCE_READY`, `RENDERED`, `QA_PASS`, `FOUNDER_APPROVED`, `PUBLISHED`, `PERFORMANCE_OBSERVED`, `BLOCKED` or `UNKNOWN`. Report exact revision and evidence.
3. Pull the relevant brand rules, approved examples, rejected examples and canonical CIS Video Production OS; do not paste a bloated profile into every tool call.
4. Dispatch specific jobs to actually available tool adapters (GitHub, Browser/Capture, HyperFrames, Descript, Higgsfield, DAM, publisher). No fictitious subagents or backend automations.
5. Produce or verify work; write a small handoff for other sessions: source revision, work ID, approved assets, unresolved defects, owner, rights, QA receipt, exact next action, cost if observed, and canonical links.
6. Update the connected authoritative record only through authorized, observed write tools. A local markdown plan is not a Notion sync or runtime registration.

## Auto-hook reality

- ChatGPT: installed plugin skills may be selected for matching intents; implicit invocation does **not** guarantee selection in every chat or execute unattended work.
- Codex/repository agents: scoped `AGENTS.md` and SKILL.md guide agents **when they operate in that repository**; they do not inject into unrelated sessions.
- Runtime hooks: event webhooks, job schedulers or GitHub Actions require an actual deployed runner, credentialed adapters, role-scoped permissions, deduplication, budgets, monitoring and release receipt; no implied background agent.
- Memory: useful hints, not a canonical artifact ledger or substitute for source retrieval.

## Handoff format

```yaml
work_id: REQUIRED
brand: REQUIRED
owner_repo: REQUIRED
source_commit: EXACT_OR_UNKNOWN
source_artifact_uri: EXACT_OR_UNKNOWN
accepted_asset_hashes: []
status: PROPOSED
qa_receipt_uri: null
founder_approval_ref: null
publication_receipt_ref: null
cost_observed: null
known_blockers: []
next_owner: NAMED_ROLE
next_action: ONE_CONCRETE_ACTION
```

## Privacy and guardrails

No secret copying into exports. No cross-brand confidential assets without permission. Do not silently publish, merge, charge credits, launch automated jobs, or claim a release gate complete. When task is authorized and tools exist, execute reversible steps and report receipts; avoid performative status updates.
