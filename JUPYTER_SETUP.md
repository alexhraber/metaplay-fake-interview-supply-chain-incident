---
layout: default
title: "Jupyter Setup"
---

# Reproducible Jupyter Setup

This repository supports controlled static analysis only. The notebooks do not
execute attacker-provided code, read raw environment captures, or contact
incident infrastructure.

## NixOS and Nushell

```nu
cd ~/src/metaplay-fake-interview-supply-chain-incident
nix develop
uv sync
source .venv/bin/activate.nu
deno jupyter --install
jupyter lab
```

`deno jupyter --install` is a one-time user-level kernel registration. It is
explicit rather than part of shell activation because it writes outside the
repository.

The flake exports the compiler runtime library through `LD_LIBRARY_PATH`, which
is the NixOS equivalent of:

```nu
let gcclib = (nix eval --raw nixpkgs#stdenv.cc.cc.lib)
$env.LD_LIBRARY_PATH = $"($gcclib)/lib"
```

The Python environment is managed by uv from `pyproject.toml`. The first
intentional `uv sync` creates `uv.lock`; commit that lock after review. Do not
use the attacker project as a Python or JavaScript dependency.

## Daily Use

```nu
nix develop
uv sync
source .venv/bin/activate.nu
jupyter lab
```

After `uv.lock` exists, use `uv sync --frozen` for repeatable daily setup.

Inspect kernels:

```nu
jupyter kernelspec list
```

Rebuild and render reviewed notebooks:

```nu
make notebooks
make check
make render
```

## Safety Boundary

- Never import or run files from the hostile MetaPlay project.
- Never paste the captured second-stage payload into a notebook.
- Never read the real process environment.
- Never replace fake fixture paths with raw private evidence.
- Never turn an IOC into a request target.
- Rendered HTML is static and does not execute notebook kernels in the browser.
