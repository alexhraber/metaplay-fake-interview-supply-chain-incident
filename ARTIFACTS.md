---
layout: default
---

# Artifact Publication Policy

This is a defensive disclosure repository, not a malware-sample distribution repository.

The following evidence exists in the private local incident workspace but is intentionally not published here:

- `stage2-response.js` was captured and hashed, but is not published as executable JavaScript.
- A terminal screenshot showing the full obfuscated stage-two source is retained locally but excluded from Git publication for the same reason.
- `headers.txt`, `fetch-meta.txt`, `SHA256SUMS.txt`, and `IOCs.txt` were preserved locally.
- `metaplay-vercel-process-env-20260612-234329.json` was preserved locally but is not published because it may contain environment and session metadata.
- Secret-scrub and follow-up reports were preserved locally but are not published because they identify credential surfaces and sensitive local paths.
- Raw attacker project files are not published in this repository.
- Raw npm logs, shell histories, and host-triage captures remain private because they may disclose local user, path, session, or operational details.

The public materials retain behavioral analysis, hashes, IOCs, remediation actions, evidence boundaries, and a clearly labeled runtime reconstruction without redistributing executable malware or sensitive host data.
