# Creator Command mapping — CIP artifacts to content-graph nodes

Author: frankxai/starlight-creator-command (2026-11-07) · Draft for CIP v0.2 discussion

Starlight Creator Command (frankxai/starlight-creator-command) implements its
content graph as a direct extension of the CIP v0.1 artifact types. No new
protocol version is proposed yet; this mapping is the input for a future
CIP v0.2 RFC. Mapping:

| CIP artifact | Creator Command graph node | Notes |
|---|---|---|
| Capture | `source` | kind/capturedVia/SHA-256 preserved; CIP attestation becomes graph edges |
| Brief | `idea` + `story` | storyboard options are a structured refinement of the agent chain |
| AssetBundle | `asset` (+`variant`) | provenance.origin + rights (license, ISRC/ISWC/UPC, splits) extend the bundle |
| Publication | `publication` | export-handoff only (TikTok AutoCut/CapCut/manual); no posting by design |
| LearnedPattern | `measurement` | platform-reported or human-entered metrics; honest rollups |
| Attestation | `approval` | HMAC-signed, human principal, exact content SHA-256, 48h TTL (starlight-social pattern) |

Two additions beyond v0.1 that a v0.2 RFC should consider:
1. **Signed approval as a first-class artifact** (principal, content hash, expiry) — currently CIP has no approval artifact.
2. **Cost admission receipts** — model calls carry budget-ledger reservations (fail-closed when actual cost is unknown).

References: CIP SPEC.md; starlight-social `starlight.publishApprovals.v1`; creator-command docs/ADR-001.
