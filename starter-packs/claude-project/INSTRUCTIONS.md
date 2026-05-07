# Claude Project starter pack

> Drop these files into a Claude Project knowledge base. Paste `system_prompt.md` into the Project Instructions field.

## How to install

1. **Create a new Claude Project** at https://claude.ai/projects/new.
2. **Set Project Instructions** — copy the contents of `system_prompt.md` from this folder and paste into the "Project Instructions" field.
3. **Upload these files to the knowledge base** (drag-and-drop):
   - `system_prompt.md` (also as a knowledge file for reference)
   - `cip-spec.md` (a flattened version of `SPEC.md`)
   - `voice-profile.json` (your voice config — the example one or your own)
   - `examples.md` (worked examples)
4. **Test the setup** — ask Claude: "What CIS layer would handle a voice memo capture?" The response should reference L2 with citations.

## File limits (April 2026 — verify if reading later)

- 30 MB per file
- 200K context window for active retrieval
- Beyond that, Claude switches to RAG mode

## What this gives you

After installation, your Claude Project understands:

- The CIP protocol shapes (Capture, Brief, AssetBundle, Publication, LearnedPattern, Attestation)
- The 6-layer stack and which adapter handles what
- The attestation contract — every output gets a provenance record
- Your voice profile — banned phrases, quarantined terms, reference brands

You can now dictate briefs, paste captures, draft posts, and the project assistant will respond in your voice with attestation-ready outputs.

## Limitations vs Claude Code

- No tool execution — the Project assistant cannot actually fetch URLs or call APIs unless you wire MCP. For real production runs, use the Claude Code starter pack.
- No file write — outputs are text only. Copy-paste workflow.

## Companion: ChatGPT Project

If you also use ChatGPT, see `../chatgpt-project/INSTRUCTIONS.md` for the parallel setup.
