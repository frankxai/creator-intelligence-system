# Cross-format edition and asset manifest

Store the durable protocol in the owning repository and actual DAM. The example here is not a claim that the DAM has been deployed. Prefer existing CIS Content Intelligence Protocol types; add fields by migration rather than creating a competing schema.

```json
{
  "work_id":"example-starlight-mission-001",
  "brand":"starlight",
  "campaign_id":"example-campaign-001",
  "source":{"kind":"verified-product","repo":"frankxai/example","commit":"EXAMPLE_SHA","deployment":"UNVERIFIED","fixture":"fixtures/demo.json"},
  "claim_provenance":[{"claim_id":"c01","statement":"Exact verified statement","source_url":"https://example.org/source","verification":"pending"}],
  "creative_direction":{"story_shape":"state-change","takeaway":"A truthful example","beats":[{"id":"b01","reader_question":"What actually changed?","visual":"before-to-after","proof":"c01"}]},
  "assets":[{"asset_id":"a01","kind":"editable-svg","uri":"asset://example.svg","sha256":"PENDING","rights":"owned-or-verified","approved":false}],
  "renditions":[{"rendition_id":"r01","format":"linkedin-carousel","size":"1080x1350","source_asset_ids":["a01"],"uri":"UNRENDERED","qa":"pending"}],
  "quality_report":{"verdict":"HOLD","checked_asset_hashes":[],"frame_samples":[],"reviewer":"unassigned","timestamp":null},
  "publication_authority":{"approved_revision":null,"approved_by":null},
  "status_receipts":{"stage":"PROPOSED","published_provider_id":null,"published_url":null,"performance_snapshot":null}
}
```

## Integrity invariants

- `work_id` is stable; `edition_id`/`rendition_id` and source revision change when material content changes.
- SHA-256 binds actual bytes; URLs and filenames alone do not. Reuse approved assets by hash.
- `raw`, `approved_master` and `published` are different roles. Native editables stay with the master; flattened derivatives never replace them.
- No duplicate publishing: idempotency key includes destination account, exact approved edition hash and scheduled intent. Unknown provider response must be reconciled before retry.
- Publication requires checked source revision, rights, QA PASS, exact founder approval, account binding and provider receipt. Scheduling does not imply publication.
- R2/Supabase is a proposed machine-serving DAM target; Google Drive is existing working ingest. No claim of deployed bridge until measured.
- ChatGPT plugin, GitHub skill and Notion card cannot grant authority. Permission decisions live in service code and user approval paths.
