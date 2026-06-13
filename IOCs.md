# Indicators of Compromise

These indicators are provided for defensive detection and incident-response correlation.

| Type | Indicator | Context |
|---|---|---|
| URL | `https://gamboracle.vercel.app/api` | Hardcoded first-stage environment POST and stage-two delivery endpoint |
| URL | `https://ipcheck-six.vercel.app/api` | Alternate endpoint encoded in the repository `.env` |
| URL | `http://136.243.22.62:1224/api/checkStatus` | Second-stage beacon and command endpoint |
| IP | `136.243.22.62` | Direct-IP C2; blackholed during containment |
| IP | `216.198.79.131` | Vercel response IP recorded during controlled analyst retrieval |
| SHA256 | `bdc6b8a1c098ce32683d496e10c769cffe52ecd3a0c47b563b36849ca37bed7d` | Captured second-stage payload; executable payload is not published here |
| npm script | `start /b node server \|\| nohup node server &` | Malicious root `prepare` lifecycle command |
| HTTP header | `x-app-request: ip-check` | Marker used on the first-stage POST |
| Code pattern | `new Function("require", response.data)` | Downloaded JavaScript execution with CommonJS access |
| Code pattern | `status === "error"` followed by `eval(message)` | Remote command gate in captured stage two |
| VS Code | `.vscode/tasks.json` with `runOn: "folderOpen"` | Quiet npm-install trigger on trusted folder open |
| VS Code | `.vscode/settings.json` excluding `**/.vscode` | Conceals the task configuration in the Explorer |
| Repository | `Ritual-Products/MetaPlay` | Repository identity preserved in local evidence |

Some infrastructure indicators may belong to shared or ephemeral hosting infrastructure. Use context before blocking broad provider ranges.

The reported `@ritualhub.net` identity, deleted LinkedIn profile, and removed Gmail invitation are social-engineering indicators rather than network IOCs. They are victim-reported context and do not independently prove attribution.
