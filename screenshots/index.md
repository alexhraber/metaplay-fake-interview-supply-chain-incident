---
layout: default
title: "Supporting Screenshots"
---

# Supporting Screenshots

These screenshots are supporting incident-context artifacts. They corroborate the recruiting wrapper, crypto-focused product pretext, repository presentation, prescribed install sequence, and malicious lifecycle trigger. They do not independently establish the operator's identity or implicate visible historical GitHub contributors.

## Review Status

All 15 PNG files were visually reviewed. Each is a 3840-by-2160 full-desktop capture made between approximately 02:13 and 02:21 on June 13, 2026, after the live interview execution. They document what was visible during later review; they are not packet captures, original process telemetry, or proof that every displayed identity participated knowingly.

The screenshots do **not** show the later deletion of the LinkedIn identity or calendar invitation. That remains victim-reported post-contact context rather than screenshot-corroborated evidence.

## Publication Safety

The current images require redaction review before public release:

- The invitation screenshot exposes personal account details, meeting and scheduling links, and browser-session context.
- Several images expose browser chrome, profile imagery, document URLs, local UI state, and other incidental identifiers.
- `2026-06-13_02-21-13.png` displays the captured obfuscated stage-two source. It should be withheld or replaced with a tightly cropped, non-executable behavioral excerpt so this repository does not redistribute the raw payload.

## Per-Image Review

| Screenshot | Evidentiary value | Publication recommendation |
|---|---|---|
| `02-13-20` | Unsolicited invitation, Gmail unknown-sender warning, lookalike recruiting domain, calendar/Meet/Calendly workflow, and crypto/AI role framing | **Heavy redaction or withhold.** Remove personal email, meeting and scheduling links, profile paths, account imagery, and browser/session details. |
| `02-14-05` | Polished Ritual-branded company overview used as recruiting collateral | Crop to document body; remove document URL, profile image, browser chrome, and local desktop state. |
| `02-14-10` | Presents MetaPlay as a key product with P2E, NFT, token, and real-crypto-reward claims | Crop to document body; same browser/account redactions. |
| `02-14-18` | Extends the product story to token utility, governance, staking, and cross-chain support | Crop to document body; same browser/account redactions. |
| `02-14-27` | First portion of a broad hiring matrix with unusually high salary and contractor-rate ranges | Crop to the table; avoid presenting compensation claims as verified job terms. |
| `02-14-33` | Additional blockchain, AI, game, DevOps, executive, operations, and design roles | Crop to the table; the breadth supports a scalable recruiting pretext, not proof that the roles existed. |
| `02-14-38` | Benefits language and possible exposure to pre-launch tokens | Crop to document body; treat all offered benefits as unverified collateral. |
| `02-16-25` | Public `Ritual-Products/MetaPlay` repository, substantial application tree, 315 commits, and minimal visible engagement | Crop to repository content; blur personal browser profile. Do not imply visible contributors were involved. |
| `02-16-32` | `.env`, `package.json`, `server.js`, multiple contributor avatars, and README branding visible together | Crop to repository content; contributor avatars are context, not attribution. |
| `02-16-40` | Repository README advertises multi-chain gaming, crypto rewards, NFTs, smart contracts, and staking | Safe after cropping browser/profile context. |
| `02-17-10` | README prescribes root install, client install, then start; directly supports the two-step interview sequence | High-value evidence. Crop tightly to the Quick Start block and surrounding repository context. |
| `02-17-28` | Ordinary-looking auth/configuration and contribution documentation | Useful as cover-quality evidence. The preserved code does not consistently implement these claims, so do not describe it as a functional security design. |
| `02-17-32` | PR rules and a proprietary-to-Ritual confidentiality claim | Useful as legitimacy theater; crop to the README content. |
| `02-18-11` | Public `package.json` showing the malicious root `prepare` lifecycle command | Highest-value static screenshot. Crop tightly to repository path and relevant script lines. |
| `02-21-13` | Full obfuscated captured stage-two source in a terminal | **Withhold.** It is excluded from Git tracking and retained only in the private evidence workspace. |

## Evidence Groups

### Recruiting and brand pretext

- [Invitation and scheduling workflow](./2026-06-13_02-13-20.png): unknown-sender warning, lookalike `@ritualhub.net` identity, and a professional calendar/meeting workflow.
- [Branded company overview](./2026-06-13_02-14-05.png): polished Ritual-branded collateral.
- [MetaPlay product framing](./2026-06-13_02-14-10.png): describes MetaPlay as a key product centered on P2E, NFTs, tokens, and crypto rewards.
- [Crypto roadmap](./2026-06-13_02-14-18.png): expands the pretext to token utility, governance, staking, and cross-chain support.
- [Open roles, part 1](./2026-06-13_02-14-27.png) and [part 2](./2026-06-13_02-14-33.png): broad hiring matrix with high salary and contractor-rate ranges.
- [Benefits and token compensation](./2026-06-13_02-14-38.png): includes possible exposure to pre-launch tokens.

### Repository presentation and execution path

- [Repository overview](./2026-06-13_02-16-25.png) and [file/contributor view](./2026-06-13_02-16-32.png): public repository, apparent history, contributor avatars, and an otherwise substantial application tree. The page simultaneously showed minimal engagement, no repository description/topics, and no releases or packages. Local Git analysis shows the 315-commit history began with 275 commits from the unrelated `tcpie` project.
- [Crypto-focused README](./2026-06-13_02-16-40.png): multi-chain gaming, real crypto rewards, NFT avatars, smart contracts, and staking.
- [Prescribed setup sequence](./2026-06-13_02-17-10.png): root `npm install`, followed by `cd client` and a second install. The victim completed only the root step.
- [Plausible application documentation](./2026-06-13_02-17-28.png) and [confidentiality claim](./2026-06-13_02-17-32.png): ordinary configuration, contribution, and proprietary-project language used as legitimacy cover.
- [Malicious lifecycle line](./2026-06-13_02-18-11.png): the root `prepare` script visible in the public repository.

### Withheld from publication

- `2026-06-13_02-21-13.png`: terminal view of the full captured stage-two response. Preserve privately as evidence; do not publish it as part of the defensive article.
