#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

python scripts/sanitize-notebooks.py --write notebooks
mkdir -p docs/notebooks
find docs/notebooks -maxdepth 1 -type f -name '*.html' -delete
jupyter nbconvert \
  --to html \
  --output-dir docs/notebooks \
  notebooks/*.ipynb

python scripts/write-notebook-index.py
echo "Rendered reviewed notebooks to docs/notebooks/"
