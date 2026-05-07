# Creator Intelligence System (CIS)

> **The sovereign content substrate for AI-first creators.**
> Open-source, MIT, bootable. Sibling to [Starlight Intelligence System (SIS)](https://github.com/frankxai/Starlight-Intelligence-System), [Investment Intelligence System (IIS)](https://github.com/frankxai/iis), and [Library OS](https://github.com/frankxai/library-os).

---

## Why this exists

In 2026, every major content platform has AI bolted on. None has an agent-orchestrated, cross-modal, self-learning content substrate built from first principles for individual creators. Adobe's GenStudio (April 2026) is the closest equivalent — and it is closed, AEM-coupled, and priced for Fortune 500 marketing departments.

CIS is the open equivalent for sovereign creators. The thesis:

1. **The integration layer is disposable.** APIs change yearly, models commoditize, platforms die. A creator tool tied to any specific provider is a 2-year asset, not a career asset.
2. **The intelligence layer is the 100-year asset.** Your content history. Your agent memory. Your distribution logic. Your voice. Your performance data. These compound across decades — but only if you own them.
3. **Attestation is the moat.** Every published piece carries a cryptographic record of human idea → models used → agent chain → human reviewer → signed timestamp. This is what nobody else does, and it is what audiences will demand by 2028.

You do not need to be a creator to use CIS. You need to be someone who would rather own their thinking than rent it from a platform.

---

## What it is

CIS is six composable layers on a sovereign substrate. Each layer has a typed interface, a default open-source adapter, and a clear extension point.

```
┌──────────────────────────────────────────────────────────────────┐
│  L6  LEARN       │ AgentDB · ReasoningBank pattern · perf loop   │
│  L5  DISTRIBUTE  │ Bluesky · LinkedIn · Beehiiv · Farcaster · …  │
│  L4  PRODUCE     │ Anthropic SDK · AI SDK · NB · Suno · Remotion │
│  L3  STRATEGY    │ Calendar · Format Library · Voice · ICP       │
│  L2  CAPTURE     │ Voice · Web clip · File drop · Notion bridge  │
│  L1  SUBSTRATE   │ Identity · Memory · MCP · Governance (SIS)    │
└──────────────────────────────────────────────────────────────────┘
                                  │
                          CIP v0.1 protocol
                                  │
                  ┌───────────────┴───────────────┐
                  ▼                               ▼
         GenCreator Studio                   Your custom UI
         (Vercel template)                   (Tauri, CLI, MCP)
```

Read [`ARCHITECTURE.md`](./ARCHITECTURE.md) for the layer-by-layer detail.
Read [`SPEC.md`](./SPEC.md) for the Content Intelligence Protocol (CIP) v0.1.
Read [`ATTESTATION.md`](./ATTESTATION.md) for the transparency moat.

---

## Quick start

CIS is distributed in four modes. Pick the one that fits your stack.

### Mode 1 — Vercel template (web-first creators)

The flagship experience. Deploy [GenCreator Studio](https://github.com/frankxai/GenCreator-Studio) — a Next.js + Tailwind template that uses `@cis/core` as its brain.

```bash
gh repo create my-studio --template frankxai/GenCreator-Studio --public
cd my-studio
pnpm install
pnpm dev
```

One-click deploy: see [GenCreator-Studio/DEPLOY.md](https://github.com/frankxai/GenCreator-Studio/blob/main/DEPLOY.md).

### Mode 2 — Claude Code plugin (terminal-first creators)

Drop the starter pack into your Claude Code project. Skills, commands, and agents become available as `/cis-*`.

```bash
npx skills add frankxai/creator-intelligence-system/starter-packs/claude-code -g
```

See [`starter-packs/claude-code/`](./starter-packs/claude-code/) for the bundle.

### Mode 3 — Claude Project (chat-first creators)

Drop the markdown bundle into your Claude Project knowledge base. Paste the system prompt into Project Instructions.

See [`starter-packs/claude-project/INSTRUCTIONS.md`](./starter-packs/claude-project/INSTRUCTIONS.md).

### Mode 4 — ChatGPT Custom GPT

Drop the bundle into your Custom GPT knowledge files. Paste the system prompt into the Instructions field. Wire the OpenAPI spec for actions if you want web fetches.

See [`starter-packs/chatgpt-project/INSTRUCTIONS.md`](./starter-packs/chatgpt-project/INSTRUCTIONS.md).

---

## What's in this repo

```
creator-intelligence-system/
├── README.md                       ← you are here
├── ARCHITECTURE.md                 ← the 6-layer stack, layer-by-layer
├── SPEC.md                         ← CIP v0.1 protocol
├── ATTESTATION.md                  ← the transparency moat
├── ROADMAP.md                      ← milestones from MV1 to year 2
├── CONTRIBUTING.md                 ← how to add an adapter, file an RFC
├── LICENSE                         ← MIT
├── package.json                    ← root (pnpm workspaces)
├── pnpm-workspace.yaml
├── packages/
│   ├── core/                       ← @cis/core — types, schemas, validators
│   │   └── src/types.ts            ← Capture, Brief, AssetBundle, Publication, LearnedPattern, Attestation
│   ├── voice/                      ← @cis/voice — brand-voice abstraction + audit
│   ├── adapters/                   ← reference adapters for each layer (W20+)
│   └── mcp-server/                 ← MCP server: any AI assistant can call CIS (W20+)
├── starter-packs/
│   ├── claude-code/                ← .claude/ skill + commands + agents
│   ├── claude-project/             ← Claude Project starter
│   └── chatgpt-project/            ← Custom GPT starter
└── docs/                           ← (W20+)
```

---

## OSS strategy

| Strategy | When | Examples |
|---|---|---|
| **Use as dependency** | OSS is MIT/Apache, well-maintained, commodity | Vercel AI SDK, BlockNote, Bluesky SDK, Farcaster SDK, Anthropic SDK, Remotion (peerDep), HeyGen Hyperframes |
| **Absorb the pattern, build clean** | The pattern is moat-critical OR upstream license is restrictive | ReasoningBank (pattern from ruflo), reflection-agent (pattern from open-canvas), agent canvas (replacing tldraw with react-flow) |
| **Avoid** | License blocks commercial use without paid key | tldraw ($6k/yr SDK), Activepieces EE (`packages/ee/` only) |

The core principle: **own the moat, rent the commodity.** Voice config, attestation protocol, learning loop, format library, brand-gate — these are clean-room. Editors, video frameworks, MCP transport, calendar UIs — these are dependencies.

---

## What CIS is not

- **Not a SaaS.** Self-host or deploy on Vercel. We do not run the substrate for you. (We will run a hosted GenCreator Studio reference instance, but the substrate itself is yours.)
- **Not a CMS.** Use Notion, Sanity, or your filesystem as the storage layer if you want. CIS is the brain, not the database.
- **Not opinionated about distribution.** Bluesky, LinkedIn, Beehiiv, Farcaster Frames, your own RSS — all adapters. Pick what fits.
- **Not a replacement for Buffer/Hootsuite.** Those are scheduling UIs. CIS is the agent-orchestrated production layer that decides what to schedule.
- **Not free of API costs.** Server-deployed CIS instances need their own Anthropic / OpenAI / Vercel AI Gateway keys. Budget API spend separately. Claude Pro/Max subscriptions cannot bill server-side calls (per Anthropic April 2026 policy).

---

## Status

**v0.1.0-alpha** · 2026-05-07 · pre-release

This is the foundation commit. The protocol is drafted; the types are written; the adapters are scaffolded. Working code lands across MV1 (this week), MV2 (May), MV3 (June). See [ROADMAP.md](./ROADMAP.md).

Bookmark the repo. Watch for the v0.1.0 tag.

---

## License

MIT. See [LICENSE](./LICENSE).

Use this freely. Build whatever you want on top. Sell what you build. The only thing you cannot do is claim you wrote it.

---

## Sibling projects

- [Starlight Intelligence System](https://github.com/frankxai/Starlight-Intelligence-System) — L1 substrate (memory palace, MCP, governance)
- [Investment Intelligence System](https://github.com/frankxai/iis) — L6 application (decision-support for wealth)
- [Library OS](https://github.com/frankxai/library-os) — sibling content substrate for books
- [GenCreator Studio](https://github.com/frankxai/GenCreator-Studio) — the Vercel template that runs on CIS

---

## Acknowledgments

CIS borrows ideas (not code) from: Adobe GenStudio's agentic content supply chain framing, ruflo's ReasoningBank pattern, LangChain's open-canvas reflection agent, and the SIS substrate-extraction pattern proven across IIS and Library OS.

The attestation moat is original work. So is the layer stack. So is the protocol.

Built with care by [Frank Riemer](https://frankx.ai) — AI Architect at Oracle EMEA, sovereign creator, runs the prototype on his own palace.

---

> *"CIS is the open substrate that captures what you say, makes what you mean, and ships it everywhere — so creators stop renting their thinking from platforms."*
