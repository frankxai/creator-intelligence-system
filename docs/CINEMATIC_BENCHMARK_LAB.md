# Cinematic production benchmark lab

Status: reference experiment; not a replacement production platform. Extends [Video Production OS](VIDEO_PRODUCTION_OS.md) and [Media Excellence Playbook](MEDIA_EXCELLENCE_PLAYBOOK.md). Runtime implementation belongs to Starlight Creator Command; GenCreator Studio is a consumer surface. Keep CIS's accepted HyperFrames default until a representative benchmark supports changing it. Remotion remains the requested experimental React route.

One source-backed 45-second brief is the control variable. Compare image + lightweight animation; agent-authored Remotion; research-to-video; generated cinematic footage; and cinematic footage + deterministic technical graphics. Hold narration, claims, delivery ratio, duration and review conditions constant. A common finishing stage is permitted and must be declared.

## Evidence contract

The production view links a CIP Brief to AssetBundle references without changing CIP v0.1 types. Retain work ID, source URL/date/retrieval hash, source-to-claim links, angle, route, exact asset/version hashes, duration, provider requests/job IDs, retries, costs and review receipts. Unknown billed cost and human intervention time remain null. Never coerce plan credits to USD or treat rate-card estimates as invoices.

Store protocol and production doctrine here, executable runtime and provider handoffs in Creator Command, canonical binary media in the accepted media fabric, and human-readable review pointers in the existing cockpit. A private runtime manifest is authoritative for its work; copied briefing documents are projections.

## Responsibility boundaries

| Responsibility | Owner |
|---|---|
| Discovery and durable episode execution | Existing Creator Command Cloudflare runtime; one scheduler and workflow instance per work |
| Optional connector ingress | Existing n8n flow, stateless forwarding only |
| Episode state and command admission | Existing BrandDesk transaction boundary |
| Audit | Hash-linked command trail and version-addressed media-store snapshots |
| Media generation | Credentialed provider adapter, or an explicitly manual connected-tool handoff |
| Deterministic render | Pinned local/hosted renderer with source and output receipts |
| Human approval | Existing signed approval contract, bound to exact manifest/media hashes |
| Publication preparation | Export package; publication is a separately authorized action |
| Feedback and reuse | Measurement records tied to original source, asset and rendition IDs |

Do not run independent n8n, Activepieces and Cloudflare schedulers for the same episode. Select a connector shell on integration fit, but retain one durable execution and state owner. A deployed binding is not proof its target workflow was registered or invoked.

## Unified episode progression

`SOURCE_READY → PRODUCING → REVIEW → APPROVED → PREPARED`

BLOCKED and CANCELLED are explicit dispositions. Materially changed input creates a new revision/work ID. Duplicate idempotency keys with changed payloads fail; stale sequence numbers fail. Checkpoints must not re-submit an ambiguous paid provider operation. Wake events signal a state recheck; they cannot approve media. PREPARED does not imply published.

## Comparison protocol

Record actual credits/currency, nullable billed compute, human intervention minutes, provider latency, assembly time and total elapsed time separately. Report polling-based completion latency as an upper bound. Attribute shared image, footage, narration and setup costs once, then report marginal reuse cost explicitly.

Evaluate character consistency against an approved exact-version reference; claim accuracy; cinematic quality; audio intelligibility and taste; reproducibility; automation readiness; and audience usefulness. Empty character use is N/A, not perfect consistency. Codec and acoustic checks do not establish aesthetic or audience quality. Use independent reviewers and viewer tasks before changing a default.

Tools without a supported accessible generation interface receive a handoff packet. In particular, source/audio APIs for NotebookLM Enterprise do not establish access to a video-generation API. Retain native video output and any manual 45-second conforming edit separately. A renderer source file is not a rendered video.

## First bounded experiment

The pilot uses Anthropic's [Sonnet 4.5 announcement dated 29 September 2025](https://www.anthropic.com/news/claude-sonnet-4-5) as an explicitly historical fixture. The original treatment separates sourced launch facts from an architectural interpretation about control and evidence. No current-model ranking is inferred.

The first run generated one image and three 15-second clips through connected Higgsfield tools. Account balance moved by 57.75 Higgsfield credits, consistent with quoted inputs; this is balance evidence, not a per-job invoice. No claim of unattended provider transport follows from successful conversational generation. No character reference was promoted from a registry status alone. Runtime audit, file hashes and measured exports belong with that private experiment's receipts.

Acceptance requires an actual request, durable episode record, inspectable output, honest QA disposition and publication-preparation handoff. A document, placeholder workflow, mock provider result or successful unit test alone does not satisfy it.
