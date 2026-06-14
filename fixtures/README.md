# Public Fixtures

Fixtures are fake, sanitized, derived, or already public:

- `fake-package-json.json`: inert lifecycle strings used for shell parsing;
- `fake-process-env.redacted.json`: fake key names and redacted demo values;
- `fake-stage2-response-summary.json`: behavior summary, not payload code;
- `fake-nohup-runtime-evidence.json`: reconstructed runtime structure;
- `stage2-feature-summary.public.json`: reviewed hash, size, and feature presence;
- `public-artifact-catalog.json`: normalized public IOCs and evidence references;
- `iocs.public.json`: indicators already published in `IOCs.md`.

The feature and artifact catalogs are publication derivatives. They deliberately
exclude the raw stage-two body, real environment values, credentials, cookies,
auth headers, and private capture data.

Do not replace these files with raw evidence captures.
