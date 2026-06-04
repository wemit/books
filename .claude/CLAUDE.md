# Books — project instructions

## Formatting (Prettier)

CI run `prettier --check .` in lint step, fail on any unformatted file. After edit or create **any** file (`.ts`, `.vue`, `.json`, `.md`, etc.), run Prettier before commit:

```bash
npx prettier --write <files-you-changed>
npx prettier --check .   # verify clean before commit/push
```

ESLint pass not enough — Prettier separate check. Editor auto-format not run on tool-written files, so format them explicit.

## Lint / typecheck

- Lint: `yarn lint` (`eslint . --ext ts,vue`)
- Typecheck: `npx tsc --noEmit -p tsconfig.json`
- Tests: `yarn test <spec-path>` (tape); run relevant specs after changes.

## Estonian (EE) compliance & addons

Fork add Estonian compliance via two-layer system (see README.md "Architecture"):

- **Layer 1 — native regional data**: models (`models/regionalModels/<cc>/`,
  `getRegionalModels()`), schemas (`schemas/regional/<cc>/`), setup records
  (`src/regional/<cc>/`, `createRegionalRecords()`), COA (`fixtures/`). Keyed
  by country code / name.
- **Layer 2 — addon system**: app-level contributions (reports, routes,
  sidebar, list actions) live in `src/custom/<addon>/index.ts` as `AppAddon`;
  main-process IPC in `main/addons/`.

Rules:

- Add regional data or addon feature must touch **zero core files**. When core file genuinely must change, mark spread/branch with `// EE` (or relevant country code) / `// CUSTOM:`, keep one line.
- No comments that merely describe code. Comments only at crucial decisions, there prefer cite governing law (e.g. KMS §41/§42, §43) or non-obvious reason.
- VAT codes / KMD line mapping compliance-sensitive: verify against EMTA / official sources before change line buckets or rates.
