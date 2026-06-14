---
layout: default
---

# Publishing

This repository is intended to be published with GitHub Pages as a project site.

## Expected URL

Assuming the GitHub username is `alexhraber` and the repository is named `metaplay-fake-interview-supply-chain-incident`, the expected project Pages URL is:

`https://alexhraber.github.io/metaplay-fake-interview-supply-chain-incident/`

## GitHub Settings

After pushing:

1. Open the repository on GitHub.
2. Go to **Settings -> Pages**.
3. Under **Build and deployment**, choose **Deploy from a branch**.
4. Select:
   - Branch: `main`
   - Folder: `/ (root)`
5. Save.
6. Wait for the Pages build to complete.
7. Visit the published site from the Pages settings panel.

## Safety Notes

Before publishing, verify:

- No live secrets are included.
- No raw environment captures are included.
- No executable attacker payloads are included.
- No credential audit reports are included.
- Attribution remains evidence-bound.
- The reconstructed `nohup.out` evidence is clearly labeled as reconstructed.

## Notebook Publication

Public notebook sources live in `notebooks/`. Before rendering:

```bash
uv sync
python scripts/build-public-notebooks.py
bash scripts/check-public-safety.sh
bash scripts/render-notebooks.sh
```

Rendered HTML is written to `docs/notebooks/`, which is linked from the existing
Pages article. GitHub Pages serves these as static HTML; it does not execute a
Jupyter kernel in the browser.

Once `uv.lock` has been generated during an intentional dependency sync, use
`uv sync --frozen` for publication rebuilds.

Only reviewed public notebooks are rendered. `notebooks/private/`, raw payloads,
raw environment captures, credential reports, and local scratch output are
excluded.
