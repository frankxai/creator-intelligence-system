---
name: media-continuity
description: Use to find and reuse owned images, visual references, characters or media across accessible catalogs; audit DAM search coverage; resume a campaign, render or asset handoff across chats; explain missing connections and future-chat activation.
---

# Cross-chat Continuity and Handoff

Never treat the conversation transcript as the complete durable source of truth. Search relevant authorized GitHub, Notion, Drive, asset registry and deployment data; fetch exact artifacts and citations before claiming current status. Respect tenant, brand and audience boundaries.


## Find existing assets before production

1. Resolve the creator/workspace, brand, character and intended placement from the request. Discover the actual connected catalogs and their coverage. Load the current accepted storage policy when available; a connector's availability does not make it the asset authority.
2. Prefer a verified workspace-scoped VIS/GenCreator catalog tool when exposed. Use search_assets, get_asset and get_asset_preview only when their actual schemas are available. Otherwise use the authorized host file/provider tools. Recent chat-generated files may remain in ChatGPT Library; an R2 bucket, Cloudinary library, Supabase catalog and local VIS index cover different subsets. Do not invent a universal generation/export hook or assume access to another user's files.
3. Search identifiers and collection metadata first. Use caption/text search or visual similarity only when supported, and name which method ran. Preserve source, asset, version and character IDs. Show at most six useful candidates and retrieve previews only for selected candidates. A similar-looking character is not established canon.
4. Report each relevant source as searched, unavailable or not configured, with observed freshness when provided. Empty results from one source are not global absence. Distinguish catalog records, retrieved files, unique content hashes, rights, asset-level approval and exact-version approval. Do not inherit approval onto a changed version.
5. Return the selected references, original proportions, source links and known gaps. Preserve the user's requested composition/aspect ratio unless they request a change. Only report ingestion, upload or saved review decisions with observed receipts. Follow media-director for production and media-release-critic for release review.

### Acceptance examples

- Find our copper fox: retrieve its established identity and versions from accessible sources; inspect candidates rather than inventing a new fox.
- Cloudinary returned zero, Library has the reference: use the retrieved reference and report Cloudinary's coverage boundary.
- Another workspace's asset ID is supplied: use only authorized workspace tools; do not ask an operator connector to bypass the denial.
- A new account has no catalog: explain the empty/configuration state and use a selected supplied reference; never fall back to the founder's private collection.

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
