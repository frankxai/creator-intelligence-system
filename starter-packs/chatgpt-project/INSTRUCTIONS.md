# ChatGPT Custom GPT starter pack

> Build a CIS-aware Custom GPT in 10 minutes.

## How to install

1. **Open GPT Builder** at https://chat.openai.com/gpts/editor.
2. **Configure tab** — paste the contents of `system_prompt.txt` from this folder into the "Instructions" field. (Max ~8,000 characters; the prompt fits.)
3. **Knowledge files** — upload (max 10 files, 512 MB each):
   - `cip-spec.pdf` (flattened protocol doc — PDFs index reliably in GPT search)
   - `voice-profile.json` (your voice config)
   - `examples.md`
4. **Actions** (optional) — paste the contents of `actions.yaml` (OpenAPI 3.1) into the GPT Actions panel to wire your CIS instance's HTTP endpoints. The schema documents:
   - `POST /api/cis/capture`
   - `POST /api/cis/brief`
   - `POST /api/cis/produce`
   - `POST /api/cis/distribute`
   - `GET /.well-known/cis/attestations/{id}`
5. **Test** — ask the GPT: "What's the difference between an L4 production adapter and an L5 distribution adapter?" Expected: clear answer with citations to the CIP spec.

## File-format reminder

ChatGPT does NOT unzip uploaded files. Upload individual documents.

## Limitations

- 10 file ceiling per GPT lifetime. Keep uploads consolidated.
- Actions require a publicly-reachable HTTPS endpoint with OpenAPI 3.1 schema. If you self-host CIS, expose only the CIS endpoints — never the substrate.
- No real-time MCP — Actions are HTTP only.

## What this gives you

A Custom GPT that can:

- Discuss CIS architecture with full protocol awareness.
- Draft briefs in your voice profile.
- Produce drafts that pass the voice audit.
- Render attestation footers.

For full production execution (capture → publish), wire the Actions YAML or use a Claude Code or Vercel-template instance instead.
