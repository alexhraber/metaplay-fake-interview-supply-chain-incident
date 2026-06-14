---
layout: default
title: "Defensive Analysis Notebooks"
---

# Technical Analysis Notebooks

These public notebooks are the technical appendix to the incident report. They
focus on exploit mechanics, static code analysis, data flow, network semantics,
IOC derivation, and evidence-bound reporting. Source notebooks are sanitized,
output-light, and rendered as static HTML.

| Notebook | Kernel | Purpose |
|---|---|---|
| `00-analysis-map-and-safety-boundary` | Python | Map the incident architecture and public evidence boundary |
| `01-npm-lifecycle-entrypoint-analysis` | Python | Parse the lifecycle entrypoint, shell fallback, and process ancestry |
| `02-node-import-chain-and-side-effects` | Python | Reconstruct CommonJS imports, top-level calls, and authority transfer |
| `03-first-stage-env-exfil-dataflow` | Python | Model bulk environment capture and first-stage request construction |
| `04-stage-two-static-feature-analysis` | Python | Analyze derived stage-two features without publishing the payload |
| `05-beacon-and-network-path-analysis` | Deno | Build a fake loopback beacon and reason about `ENETUNREACH` |
| `06-ioc-and-artifact-derivation` | Python | Normalize public IOCs and generate defender-friendly output |
| `07-evidence-boundary-and-claim-classification` | Python | Classify claims as proven, observed, likely, or unsupported |

[Open the rendered notebook index](./docs/notebooks/index.html).

> These notebooks are static rendered analysis artifacts. They document
> controlled inspection steps, parsing logic, hashes, and defensive reasoning.
> They are not live notebooks and do not execute attacker-provided code in the
> browser.

## Publication Rules

- Outputs are cleared before rendering.
- Raw payloads and raw environment captures are withheld.
- Public IOCs are data for correlation, never request targets.
- Absolute local paths are excluded from public notebook content.
- Evidence claims distinguish capability, observed execution, likely
  transmission, proven transmission, and not-evidenced behavior.

## Public and Private Scope

The public notebooks teach code-path reconstruction and evidence reasoning from
sanitized material. The separate private learning lab retains the broader
curriculum and loopback-only simulators. Raw hostile payloads, raw environment
captures, and private credential findings are not public notebook inputs.

## Rebuild and Render

From the repository development environment:

```bash
python scripts/build-public-notebooks.py
python scripts/sanitize-notebooks.py --write notebooks
bash scripts/check-public-safety.sh
bash scripts/render-notebooks.sh
```

The builder does not execute notebook cells. The sanitizer clears outputs and
rejects dangerous constructs in executable cells. The render step writes only
the reviewed public set to `docs/notebooks/`.
