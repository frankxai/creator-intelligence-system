# Contributing

> Thank you for considering a contribution. CIS is small but the surface is broad. Read this short guide before opening a PR.

---

## Ground rules

1. **Adapters first.** The fastest way to add value is to write a new adapter (a new capture mode, a new distribution channel, a new model provider). Open an issue describing the adapter, then submit.
2. **The protocol is sacred.** Changes to types in `@cis/core/src/types.ts` or `@cis/core/src/schemas/cip-*.json` go through an RFC.
3. **Attestation cannot be weakened.** No PR may make attestation optional, skippable, or partial without RFC consensus.
4. **Voice config stays single-source.** All voice rules live in `@cis/voice`. Do not duplicate banned-phrase or quarantine lists in adapters.
5. **No vendor lock.** Every adapter must implement the layer interface fully. Closed-source adapters are welcome elsewhere; this repo only ships open ones.

---

## How to add an adapter

```bash
# 1. Scaffold
cd packages/adapters/
cp -r _template my-adapter
cd my-adapter
# 2. Edit package.json, README, src/index.ts, tests/
# 3. Add to the registry
# packages/core/src/registry.ts → add { id: 'my-adapter', layer: 'distribute', ... }
# 4. Test
pnpm test
# 5. Open a PR
```

Each adapter must:

- Implement the layer interface (`CaptureAdapter`, `StrategyAdapter`, `ProductionAdapter`, `DistributionAdapter`, `LearningAdapter`).
- Include a README with: what it does, what credentials are needed, what it costs, what it logs, what failure modes to expect.
- Pass the contract tests in `packages/test-kit/`.
- Carry MIT or compatible permissive license. AGPL or copyleft adapters live elsewhere.

---

## How to file an RFC

RFCs live in `docs/rfcs/`. Format:

```
docs/rfcs/000N-short-title.md
```

Template at `docs/rfcs/_template.md`. Required sections: motivation, design, drawbacks, alternatives, prior art, unresolved questions.

Discussion in GitHub Issues with the label `rfc:`. Approval requires:

1. Two CODEOWNERS approvals.
2. No outstanding objections after a 2-week review window.
3. Implementation plan with at least one committed implementer.

---

## Code style

- TypeScript strict mode.
- ESLint + Prettier defaults from `tsconfig.base.json`.
- Tests via `vitest`.
- No commented-out code in committed files. Use git history.
- No `any` without an inline `// reason: ...` comment.

---

## Commit style

Conventional commits. Examples:

```
feat(adapter): add distribute-mastodon
fix(core): correct ULID encoding for capture IDs
docs(spec): clarify canonicalization rules for attestation signatures
chore(deps): bump @atproto/api to 0.13.0
```

---

## Reporting security issues

Do not file public issues for security vulnerabilities. Email the maintainer at the address listed in `SECURITY.md`. Disclosure within 90 days, coordinated.

---

## License

All contributions are licensed under MIT. By submitting a PR, you agree to release your contribution under MIT.

---

> *Build the substrate that outlives the platform.*
