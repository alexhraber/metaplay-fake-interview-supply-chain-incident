#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

secret_pattern='sk-''ant-|nv''api-|gh''o_|gh''p_|github_''pat_|BEGIN OPENSSH PRIVATE ''KEY|BEGIN PGP PRIVATE ''KEY|refresh''Token|access''Token|SECRET_ACCESS_''KEY|PRIVATE ''KEY|seed ''phrase|mnemo''nic|xox''b-|xox''p-|aws_secret_access_''key'
secret_hits="$(
  grep -RInE "$secret_pattern" . \
    --exclude-dir=.git \
    --exclude-dir=_site \
    --exclude-dir=.venv \
    --exclude='check-public-safety.sh' \
    --exclude='build-public-notebooks.py' \
    --exclude='sanitize-notebooks.py' \
    --exclude='*.ipynb' \
    || true
)"
unexpected_secret_hits="$(
  printf '%s\n' "$secret_hits" |
    grep -vE '\.(md|html):' |
    grep -v 'fixtures/fake-process-env.redacted.json.*redacted-demo-value' |
    sed '/^$/d' || true
)"
if [[ -n "$unexpected_secret_hits" ]]; then
  echo "Unexpected secret-pattern hits:"
  printf '%s\n' "$unexpected_secret_hits"
  exit 1
fi
documentation_hits="$(printf '%s\n' "$secret_hits" | grep -E '\.(md|html):' || true)"
if [[ -n "$documentation_hits" ]]; then
  echo "Documentation-only warning-pattern hits reviewed:"
  printf '%s\n' "$documentation_hits"
fi

danger_pattern='e''val\(|new Func''tion|child_''process|ex''ec\(|sp''awn\(|/home/''arx'
danger_hits="$(
  grep -RInE "$danger_pattern" scripts tools analysis fixtures \
    --exclude='*.md' \
    --exclude='*.html' \
    --exclude='check-public-safety.sh' \
    --exclude='build-public-notebooks.py' \
    || true
)"
if [[ -n "$danger_hits" ]]; then
  echo "Unexpected executable-code safety hits:"
  printf '%s\n' "$danger_hits"
  exit 1
fi

python scripts/sanitize-notebooks.py notebooks
echo "Public safety checks passed."
