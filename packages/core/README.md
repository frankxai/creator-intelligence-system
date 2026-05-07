# @cis/core

The Creator Intelligence Protocol (CIP) — TypeScript types, schemas, and adapter contracts.

## Install

```bash
pnpm add @cis/core
```

## What's in here

- `types.ts` — every artifact and adapter contract: `Capture`, `Brief`, `AssetBundle`, `Publication`, `LearnedPattern`, `Attestation`, plus `CaptureAdapter`, `StrategyAdapter`, `ProductionAdapter`, `DistributionAdapter`, `LearningAdapter`.
- `schemas/cip-v0.1.json` — the JSON Schema mirror of the TypeScript types. Use for runtime validation and cross-language interop.

## Usage

```ts
import type {
  Capture,
  Brief,
  AssetBundle,
  Publication,
  Attestation,
  CaptureAdapter,
  DistributionAdapter,
} from '@cis/core'
import { CIP_VERSION } from '@cis/core'

console.log('CIP version:', CIP_VERSION) // "0.1.0"
```

## Conformance

If you implement an adapter or a new CIS instance, conformance means:

1. Types validate against `cip-v0.1.json`.
2. Attestations sign and verify per the canonicalization rules in `SPEC.md`.
3. Layer interface methods are implemented fully (no `// TODO` shortcuts in production).

## License

MIT.
