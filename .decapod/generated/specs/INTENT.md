# Intent


<!-- decapod:declared-capabilities:start -->

## Declared Capability Surfaces

- `authentication`
- `background-processing`
- `event-driven`
- `external-integrations`
- `infrastructure-management`
- `persistent-state`
- `public-api`
- `scheduled-jobs`

<!-- decapod:declared-capabilities:end -->
## Product Outcome
- > **Defensive disclosure note:** This write-up is published for defensive awareness and incident-response education. It documents a malicious fake-interview repository, npm lifecycle execution path, staged JavaScript behavior, observed IOCs, containment actions, and evidence boundaries. It intentionally avoids publishing live secrets or executable attacker payloads. Attribution is not asserted beyond the evidence described.

## What This Project Is
metaplay-fake-interview-supply-chain-incident is a service_or_library project built using JavaScript.
> **Defensive disclosure note:** This write-up is published for defensive awareness and incident-response education. It documents a malicious fake-interview repository, npm lifecycle execution path, staged JavaScript behavior, observed IOCs, containment actions, and evidence boundaries. It intentionally avoids publishing live secrets or executable attacker payloads. Attribution is not asserted beyond the evidence described.

Key operating facts:
- **Primary languages**: JavaScript
- **Detected surfaces**: javascript, python, shell

## Product View
```mermaid
flowchart LR
  U[Primary User] --> P[metaplay-fake-interview-supply-chain-incident]
  P --> O[User-visible Outcome]
  P --> G[Proof Gates]
  G --> E[Evidence Artifacts]
```

## Inferred Baseline
- Repository: metaplay-fake-interview-supply-chain-incident
- Product type: service_or_library
- Primary languages: JavaScript
- Detected surfaces: javascript, python, shell

## Scope
| Area | In Scope | Proof Surface |
|---|---|---|
| Core workflow | Define a concrete user-visible workflow | Acceptance criteria + tests |
| Data contracts | Document canonical inputs/outputs | [INTERFACES.md](./INTERFACES.md) and schema checks |
| Delivery quality | Block promotion on broken proof surfaces | [VALIDATION.md](./VALIDATION.md) blocking gates |

## Non-Goals (Falsifiable)
| Non-goal | How to falsify |
|---|---|
| Feature creep beyond the primary outcome | Any PR adds capability not tied to outcome criteria |
| Shipping without evidence | Missing validation artifacts for promoted changes |
| Ambiguous ownership boundaries | Missing owner/system-of-record in interfaces |

## Constraints
- Technical: runtime, dependency, and topology boundaries are explicit.
- Operational: deployment, rollback, and incident ownership are defined.
- Security/compliance: sensitive data handling and authz are mandatory.

## Acceptance Criteria (must be objectively testable)
- [ ] Decapod validate passes, required tests pass, and promotion-relevant artifacts are present.
- [ ] Non-functional targets are met (latency, reliability, cost, etc.).
- [ ] Validation gates pass and artifacts are attached.
- [ ] `npm test` (or `pnpm test`) passes for unit/integration suites
- [ ] `npm run lint` passes
- [ ] `npm run typecheck` passes for strict TS projects

## Epistemic Custody Fields

### Active Assumptions
- [ ] List any assumptions made to proceed.
- [ ] Flag assumptions that require future verification.

### Confidence & Risk Level
- **Confidence**: Low/Medium/High (Rationale: )
- **Risk**: Low/Medium/High (Impact of wrong assumptions: )

### Measured vs Inferred Facts
| Fact | Source (Provenance) | Type (Measured/Inferred) |
|---|---|---|
| | | |

### Unresolved Contradictions
- [ ] List any evidence that conflicts with current assumptions or intent.

### Deferred Questions
- [ ] Questions to be answered later.

### Stop Conditions
- [ ] Explicit conditions under which the agent should stop and ask for help.

### Proof Required Before Completion
- [ ] Specific evidence needed to prove the outcome is met.

## Tradeoffs Register
| Decision | Benefit | Cost | Review Trigger |
|---|---|---|---|
| Simplicity vs extensibility | Faster iteration | Potential rework | Feature set expands |
| Strict gates vs dev speed | Higher confidence | More upfront discipline | Lead time regressions |

## First Implementation Slice
- [ ] Define the smallest user-visible workflow to ship first.
- [ ] Define required data/contracts for that workflow.
- [ ] Define what is intentionally postponed until v2.

## Open Questions (with decision deadlines)
| Question | Owner | Deadline | Decision |
|---|---|---|---|
| Which interfaces are versioned at launch? | TBD | YYYY-MM-DD | |
| Which non-functional target is hardest to hit? | TBD | YYYY-MM-DD | |
