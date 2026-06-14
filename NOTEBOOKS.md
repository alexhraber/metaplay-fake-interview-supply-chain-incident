---
layout: default
title: "Defensive Analysis Notebooks"
---

# Defensive Analysis Notebooks

These notebooks are static-analysis and reasoning exercises. Source notebooks
remain output-light and use fake fixtures or already-public indicators.

| Notebook | Kernel | Purpose |
|---|---|---|
| `00-python-lab-healthcheck` | Python | Verify the local analysis environment without reading secrets |
| `01-deno-js-runtime-healthcheck` | Deno | Verify safe JavaScript primitives using loopback-only data |
| `02-package-json-lifecycle-analysis` | Deno | Identify npm lifecycle execution from a fake manifest |
| `03-stage2-static-deobfuscation-notes` | Deno | Practice inert decoding and staged-loader reasoning |
| `04-ioc-extraction` | Python | Parse the already-public IOC fixture without contacting it |
| `05-behavior-map` | Python | Map capability, execution, transmission, and controls |

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

