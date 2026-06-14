#!/usr/bin/env python3
"""Build the eight reviewed public forensic notebooks without executing cells."""

from __future__ import annotations

import json
from pathlib import Path

try:
    import nbformat
except ImportError as exc:
    raise SystemExit("nbformat is required. Run `uv sync` first.") from exc

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "notebooks"

SAFETY = (
    "> **Safety boundary:** This workbook performs static analysis of sanitized "
    "excerpts, fake fixtures, and derived public metadata. It does not execute "
    "attacker code, inspect the analyst's environment, or contact any network."
)


def md(text: str):
    return nbformat.v4.new_markdown_cell(text.strip())


def py(text: str):
    return nbformat.v4.new_code_cell(text.strip())


def deno(text: str):
    return nbformat.v4.new_code_cell(text.strip())


def notebook(title: str, kernel: str, cells: list):
    if kernel == "deno":
        kernelspec = {"display_name": "Deno", "language": "typescript", "name": "deno"}
        language_info = {"name": "typescript", "file_extension": ".ts"}
    else:
        kernelspec = {"display_name": "Python 3", "language": "python", "name": "python3"}
        language_info = {"name": "python", "file_extension": ".py", "version": "3.12"}

    result = nbformat.v4.new_notebook()
    result.metadata = {
        "kernelspec": kernelspec,
        "language_info": language_info,
        "metaplay_publication": {
            "safe_static_analysis": True,
            "attacker_code_executed": False,
            "network_access_required": False,
            "raw_payload_published": False,
        },
    }
    result.cells = [
        md(f"# {title}\n\n{SAFETY}"),
        *cells,
    ]
    return result


def specs():
    return {
        "00-analysis-map-and-safety-boundary.ipynb": notebook(
            "Analysis Map and Safety Boundary",
            "python3",
            [
                md(
                    """
## Question and Method

This technical appendix reconstructs how a root dependency install crossed
several trust boundaries:

```text
root npm install
  -> prepare lifecycle script
  -> backgrounded Node server
  -> CommonJS import-time side effect
  -> bulk environment POST
  -> returned JavaScript executed with CommonJS access
  -> host-profile beacon attempt
  -> direct-IP connect failure
```

The notebooks analyze that chain without replaying it. Their governing rule is:

> **capability != observed execution != proven transmission**

Static code can establish capability. Runtime traces can establish execution.
Network or server-side evidence is needed to establish completed transmission.
"""
                ),
                md(
                    """
## Artifact and Publication Map

| Layer | Artifact | Public treatment | Reason |
|---|---|---|---|
| npm lifecycle | preserved package manifest / sanitized excerpt | analyzed directly | automatic entrypoint |
| Node import chain | `server.js`, `socket/index.js`, `controllers/auth.js` | call graph and reviewed excerpts | import-time side effects |
| environment exfiltration | auth controller / redacted schema | data-flow model | sensitive primitive |
| stage two | hash plus derived feature summary | feature extraction only | raw payload withheld |
| C2 path | public IOC plus reconstructed runtime error | network-path reasoning | no live contact |

The private evidence set also contains hostile source and raw captures. Those
are not notebook dependencies and are intentionally not published.
"""
                ),
                py(
                    """
layers = [
    {"step": 1, "boundary": "package manager -> shell", "question": "What can install execute?"},
    {"step": 2, "boundary": "entrypoint -> import graph", "question": "What runs before a request?"},
    {"step": 3, "boundary": "process -> environment", "question": "What data is reachable?"},
    {"step": 4, "boundary": "host -> remote response", "question": "What authority does returned data receive?"},
    {"step": 5, "boundary": "stage two -> C2", "question": "Did the connection complete?"},
]
layers
"""
                ),
                md(
                    """
## What Is Withheld

- the raw executable stage-two body;
- raw process-environment captures;
- credential, token, browser, shell-history, or wallet reports;
- private filesystem inventories;
- live endpoint interaction and tasking logic.

This is not loss of analytical rigor. The public substitutes are hashes,
lengths, line references, sanitized excerpts, feature presence, and bounded
runtime observations. Those are sufficient to teach the reasoning path without
redistributing executable hostile content.
"""
                ),
                py(
                    """
claim_levels = {
    "capability": "The code can perform an action.",
    "observed": "A local artifact shows that the path ran.",
    "likely": "Multiple artifacts support the inference, but one proof source is absent.",
    "proven transmission": "Network or receiver evidence shows data completed the path.",
    "not evidenced": "The available artifacts do not show the behavior.",
}
claim_levels
"""
                ),
                md(
                    """
## Analytical Questions Used Throughout

Every workbook asks:

1. What code path is under analysis?
2. Which artifact supports it?
3. What did the code do, and what authority did it enable?
4. What was actually observed?
5. What was not proven?
6. Which control could prevent or detect it?
7. Which additional telemetry would raise confidence?

**Strongest supported claim:** the install path reached downloaded stage-two
execution and a direct-IP connection attempt.

**Strongest unsupported claim:** that direct-IP tasking completed or that
credential or wallet files were stolen.
"""
                ),
            ],
        ),
        "01-npm-lifecycle-entrypoint-analysis.ipynb": notebook(
            "npm Lifecycle Entrypoint Analysis",
            "python3",
            [
                md(
                    """
## Code Path

```text
root npm install
  -> npm lifecycle scheduler
  -> prepare
  -> start /b node server || nohup node server &
  -> node server
```

`prepare` is lifecycle code, not metadata. During a normal install npm may hand
that string to a platform shell. The user therefore crossed a code-execution
boundary by installing the root project, before explicitly starting the app.
"""
                ),
                py(
                    """
import json
from pathlib import Path

manifest = json.loads(Path("../fixtures/fake-package-json.json").read_text())
lifecycle_names = {"preinstall", "install", "postinstall", "prepare"}
lifecycle = [
    {"hook": name, "command": command}
    for name, command in manifest.get("scripts", {}).items()
    if name in lifecycle_names
]
lifecycle
"""
                ),
                md(
                    """
## Shell Semantics, Parsed as Data

The preserved command was:

```text
start /b node server || nohup node server &
```

On Windows, `start /b` attempts a background launch. On Linux/NixOS, that
Windows-oriented command fails, so `||` selects the Unix-like fallback.
`nohup` reduces coupling to the terminal and `&` backgrounds the child.
Nothing below executes the command; it is tokenized from an inert fixture.
"""
                ),
                py(
                    """
command = manifest["scripts"]["prepare"]
segments = [
    {
        "segment": "start /b node server",
        "meaning": "Windows background launch attempt",
        "risk": "hidden runtime",
        "classification": ["installer-triggered", "backgrounding", "server launch"],
    },
    {
        "segment": "||",
        "meaning": "run fallback if the first branch fails",
        "risk": "cross-platform resilience",
        "classification": ["cross-platform fallback", "suspicious"],
    },
    {
        "segment": "nohup node server &",
        "meaning": "Unix-like background launch",
        "risk": "detached process",
        "classification": ["backgrounding", "server launch", "suspicious"],
    },
]
{"command_matches_fixture": command == "start /b node server || nohup node server &",
 "segments": segments}
"""
                ),
                md(
                    """
| Segment | Meaning | Risk |
|---|---|---|
| `start /b node server` | Windows background launch attempt | hidden runtime |
| `||` | fallback if the prior command fails | cross-platform resilience |
| `nohup node server &` | Linux/NixOS background launch | detached process |
| `node server` | server entrypoint | imports the malicious chain |
"""
                ),
                py(
                    """
process_ancestry = [
    {"depth": 0, "process": "npm", "cause": "user ran root install"},
    {"depth": 1, "process": "platform shell", "cause": "npm invoked prepare"},
    {"depth": 2, "process": "nohup", "cause": "fallback branch on Linux/NixOS"},
    {"depth": 3, "process": "node server", "cause": "background server entrypoint"},
]
process_ancestry
"""
                ),
                md(
                    """
## Why This Is Useful to an Attacker

The command gains three properties with one manifest line: automatic execution,
cross-platform fallback, and a backgrounded process likely to outlive the
terminal session. The application does not need to serve a legitimate request.
Node only needs to evaluate `server.js` and its imports.

**Evidence:** preserved pre-containment manifest, victim account of the root
install, and reconstructed `nohup` runtime evidence.

**Strongest supported claim:** the manifest supplied an automatic install-time
path to a backgrounded `node server`; runtime evidence corroborates that this
path reached the downloaded stage.

**Not proven by the manifest alone:** the exact process lifetime or every child
PID. Process accounting, audit logs, or full shell history would strengthen it.

**Prevention:** review manifests and use an isolated, secret-free host with
scripts disabled during first inspection.

**Detection:** alert when npm is parent or ancestor of `nohup`, a shell
background operator, or an unexpected long-lived Node process.
"""
                ),
            ],
        ),
        "02-node-import-chain-and-side-effects.ipynb": notebook(
            "Node Import Chain and Side Effects",
            "python3",
            [
                md(
                    """
## Static Call Chain

```text
server.js
  -> require("./config")
  -> require("./socket/index")
       -> require("../controllers/auth")
       -> validateApiKey() at module top level
            -> setApiKey(...)
            -> verify(...)
            -> compile response as code with CommonJS access
            -> invoke compiled code with require
```

CommonJS evaluates a module's top-level statements the first time it is
required. A server import can therefore trigger network and execution behavior
before any route, socket event, or user interaction.
"""
                ),
                md(
                    """
## Sanitized Source Map

The following records preserve relationships and line-level meaning without
embedding executable source:

| File | Static relationship | Side effect |
|---|---|---|
| `server.js` | imports config, then socket module | causes imported modules to evaluate |
| `config.js` | initializes dotenv-style configuration | populates process environment |
| `socket/index.js` | imports auth controller | invokes validation at module top level |
| `controllers/auth.js` | exports validation helpers | posts environment and grants returned text Node authority |
"""
                ),
                py(
                    """
files = {
    "server.js": [
        {"kind": "require", "target": "./config"},
        {"kind": "require", "target": "./socket/index"},
    ],
    "socket/index.js": [
        {"kind": "require", "target": "../controllers/auth"},
        {"kind": "top_level_call", "target": "validateApiKey"},
    ],
    "controllers/auth.js": [
        {"kind": "function_call", "target": "setApiKey"},
        {"kind": "function_call", "target": "verify"},
        {"kind": "authority_transfer", "target": "response text receives CommonJS module access"},
    ],
}

edges = [
    {"source": source, "target": item["target"], "kind": item["kind"]}
    for source, items in files.items()
    for item in items
]
edges
"""
                ),
                py(
                    """
top_level_effects = [
    {
        "module": "config.js",
        "trigger": "first import",
        "effect": "configuration loader mutates process environment",
        "requires_user_request": False,
    },
    {
        "module": "socket/index.js",
        "trigger": "first import",
        "effect": "validation routine begins",
        "requires_user_request": False,
    },
]
top_level_effects
"""
                ),
                md(
                    """
## Dangerous Primitive Table

| Primitive | Role in the path | Security consequence |
|---|---|---|
| top-level `validateApiKey()` | begins behavior during import | startup becomes detonation |
| bulk environment copy | creates request body | broad secret exposure |
| response text compiled as code | turns data into instructions | remote stage delivery |
| `require` passed to downloaded code | grants Node module authority | filesystem, OS, and network capability |

The exact hostile syntax is documented in the public report as
`new Function("require", response.data)` followed by invocation with `require`.
It is shown here only as inert Markdown and is never run.
"""
                ),
                py(
                    """
review_questions = [
    {"primitive": "module import", "question": "Does top-level evaluation call a function?"},
    {"primitive": "HTTP response", "question": "Is response content treated as data or instructions?"},
    {"primitive": "module capability", "question": "Is a loader handed require or equivalent authority?"},
    {"primitive": "async validation", "question": "Is the caller actually awaiting the result?"},
]
review_questions
"""
                ),
                md(
                    """
## Review Lesson

A filename such as `socket/index.js` suggests infrastructure glue, but the
review unit is the import graph plus top-level statements. The trust boundary
collapsed because loading a module also began validation, transmission, stage
retrieval, and dynamic execution.

**Observed:** runtime evidence places the downloaded stage under the executor
originating from `socket/index.js`.

**Not proven by static imports:** which request bytes reached the server or
which later tasking ran.

**Detection:** grep for top-level calls near imports; build AST rules for
response-to-code flows; flag a function constructor receiving response data;
review imports whose initialization performs network I/O.

**Confidence upgrade:** Node module-load tracing, process telemetry, proxy logs,
or a preserved server-side request record.
"""
                ),
            ],
        ),
        "03-first-stage-env-exfil-dataflow.ipynb": notebook(
            "First-Stage Environment Exfiltration Dataflow",
            "python3",
            [
                md(
                    """
## Data Flow

```text
project configuration
  -> dotenv-style loader
  -> process environment
  -> bulk object copy
  -> POST request body
  -> serverless endpoint
  -> JavaScript response
```

The dangerous primitive is not one particular API key. It is bulk capture of a
developer process environment, where cloud credentials, package tokens,
service URLs, and shell context commonly coexist.

The published first-stage helper spread `process.env` into the POST body and
used the request marker `x-app-request: ip-check`. The exact source remains in
the incident report; executable cells below use only fake values.
"""
                ),
                py(
                    """
import json
from pathlib import Path

fake_env = json.loads(Path("../fixtures/fake-process-env.redacted.json").read_text())

def category(key):
    if key.startswith("AWS_"):
        return "cloud"
    if "ALCHEMY" in key:
        return "blockchain/API"
    if "AUTH" in key:
        return "auth/session"
    if key.startswith("npm_"):
        return "npm lifecycle"
    if key in {"HOME", "PATH"}:
        return "path/home"
    return "local runtime"

rows = [
    {
        "env_key": key,
        "category": category(key),
        "why_it_matters": {
            "cloud": "may authorize cloud API operations",
            "blockchain/API": "may identify or authorize a service account",
            "auth/session": "may expose service authentication configuration",
            "npm lifecycle": "reveals execution context and triggering hook",
            "path/home": "reveals host layout and command search path",
            "local runtime": "describes application mode",
        }[category(key)],
        "real_value_published": False,
    }
    for key in fake_env
]
rows
"""
                ),
                md(
                    """
| Env key | Category | Why it matters | Real value published? |
|---|---|---|---|
| `AWS_ACCESS_KEY_ID` | cloud | may identify cloud principal | no |
| `AWS_SECRET_ACCESS_KEY` | cloud | may authorize cloud API operations | no |
| `ALCHEMY_API_KEY` | blockchain/API | may authorize or identify a service account | no |
| `AUTH_API` | auth/session | identifies authentication configuration | no |
| `npm_lifecycle_event` | npm lifecycle | confirms execution context | no real capture |
| `HOME`, `PATH` | path/home | describes host layout | fake examples only |
"""
                ),
                py(
                    """
fake_request = {
    "method": "POST",
    "path": "/api",
    "headers": {
        "content-type": "application/json",
        "x-app-request": "ip-check",
    },
    "body": {
        "env": {key: "[redacted fake value]" for key in fake_env},
    },
}
fake_request
"""
                ),
                md(
                    """
## Evidence Boundary

The strongest inference is that the first-stage POST likely succeeded because
the loader received and executed a stage-two response. That is stronger than
mere capability but weaker than a complete server-side record of every field
received.

The public repository does not disclose the raw captured body. It does not
assert that every variable present in the victim shell was transmitted, and it
does not turn potential credential exposure into a claim of credential use.
"""
                ),
                py(
                    """
controls = [
    {"control": "clean-room review user", "breaks": "credential reachability"},
    {"control": "empty inherited environment", "breaks": "bulk secret capture"},
    {"control": "container or disposable VM", "breaks": "host-data reachability"},
    {"control": "egress deny by default", "breaks": "POST completion"},
    {"control": "install scripts disabled for inspection", "breaks": "automatic entrypoint"},
]
controls
"""
                ),
                md(
                    """
**Observed:** the stage-two execution path was reached.

**Likely:** the environment POST completed sufficiently for the serverless
endpoint to return the captured stage.

**Not proven publicly:** the exact request body received by the remote service.

**Detection:** alert on Node processes posting a broad environment-shaped JSON
object, especially under npm ancestry and with unusual custom headers.

**Confidence upgrade:** endpoint logs, a packet capture with payload visibility,
or a cryptographically preserved request body.
"""
                ),
            ],
        ),
        "04-stage-two-static-feature-analysis.ipynb": notebook(
            "Stage-Two Static Feature Analysis",
            "python3",
            [
                md(
                    """
> **Hostile-evidence warning:** This notebook derives features from a reviewed
> summary of hostile evidence. It does not execute the payload and does not
> publish the raw body.

## Publication-Safe Method

The private capture was inspected statically. The public derivative records
only its SHA-256, byte length, feature presence, and bounded behavior summary.
That supports reproducible claims without making the hostile body available as
an executable artifact.
"""
                ),
                py(
                    """
import json
from pathlib import Path

summary = json.loads(
    Path("../fixtures/stage2-feature-summary.public.json").read_text()
)
{
    "artifact": summary["artifact"],
    "sha256": summary["sha256"],
    "byte_length": summary["byte_length"],
    "raw_body_in_fixture": False,
}
"""
                ),
                py(
                    """
feature_rows = [
    {
        "feature": item["feature"],
        "present": "yes" if item["present"] else "not shown",
        "evidence_type": item["evidence_type"],
        "publication_form": item["publication_form"],
    }
    for item in summary["features"]
]
feature_rows
"""
                ),
                md(
                    """
## Feature Interpretation

| Feature | Present | Evidence type | Publication form |
|---|---|---|---|
| host profiling | yes | static feature | summary only |
| OS, hostname, network interface | yes | static feature | summary only |
| process environment copy | yes | static feature | summary only |
| query-string beacon | yes | static feature | field names only |
| fixed polling interval | yes | static feature | 5000 ms |
| direct-IP C2 | yes | public IOC | published |
| response JSON parsing | yes | static feature | summary only |
| conditional remote task evaluation | yes | static feature | described, not implemented |
| wallet-file reads | not shown | not evidenced in captured stage | not claimed |
| credential-file enumeration | not shown | not evidenced in captured stage | not claimed |
"""
                ),
                py(
                    """
counts = {
    "present_features": sum(item["present"] for item in summary["features"]),
    "not_shown_features": sum(not item["present"] for item in summary["features"]),
    "network_features": sum(
        any(term in item["feature"] for term in ("query", "polling", "C2", "HTTP"))
        for item in summary["features"]
    ),
}
counts
"""
                ),
                md(
                    """
## Capability Versus Captured Behavior

Conditional task evaluation makes arbitrary follow-on behavior possible if an
operator response is received. It does not prove that such a response arrived.
Likewise, the architecture could support later credential or wallet theft, but
those actions are not present in the captured stage and are not claimed.

**Observed:** downloaded stage-two JavaScript began executing and attempted the
published direct-IP connection.

**Static capability:** host profiling, environment copying, periodic beaconing,
and conditional operator task execution.

**Not proven:** successful direct-IP tasking or later file theft.

**Detection:** scan JavaScript for clusters of host profiling, environment
copying, query serialization, polling timers, direct-IP URLs, and response
content crossing into an execution primitive.

**Confidence upgrade:** a complete PCAP, proxy transcript, remote server logs,
or local telemetry showing a task response and its effects.
"""
                ),
            ],
        ),
        "05-beacon-and-network-path-analysis.ipynb": notebook(
            "Beacon and Network Path Analysis",
            "deno",
            [
                md(
                    """
## Beacon Model

The captured stage serialized host and process information into query
parameters named `sysInfo`, `processInfo`, `tid`, and `sysId`, then polled a
direct-IP endpoint. Query strings are especially visible in proxy, gateway, and
server logs and may leak data beyond the destination application.

The real stage also described conditional task evaluation when a response
reported an error state. That creates arbitrary follow-on capability, but is
not reproduced here.
"""
                ),
                deno(
                    """
const base = new URL("http://127.0.0.1:9001/api/checkStatus");
const fakeSysInfo = { hostname: "training-host", platform: "linux", mac: "00:00:00:00:00:00" };
const fakeProcessInfo = { NODE_ENV: "development", npm_lifecycle_event: "prepare" };
base.search = new URLSearchParams({
  sysInfo: JSON.stringify(fakeSysInfo),
  processInfo: JSON.stringify(fakeProcessInfo),
  tid: "fake-token",
  sysId: "fake-system-id",
}).toString();
base.toString();
"""
                ),
                md(
                    """
The cell constructs a loopback URL object only; it does not fetch it.

| Beacon field | Meaning | Risk |
|---|---|---|
| `sysInfo` | host and network profile | fingerprinting and victim selection |
| `processInfo` | process environment snapshot | secret and configuration exposure |
| `tid` | task or victim token | tracking and task correlation |
| `sysId` | stable system identifier | repeat-host correlation |
"""
                ),
                md(
                    """
## Observed Network Failure

The reconstructed runtime trace included:

```text
TypeError: fetch failed
cause: connect ENETUNREACH 136.243.22.62:1224
```

Node's `fetch` implementation uses undici. For a direct IP, no DNS lookup is
needed. The stack attempts a TCP connection, consults the route table, and fails
before connection establishment when the destination is blackholed or otherwise
unreachable.

```text
stage-two fetch
  -> undici request machinery
  -> TCP connect(136.243.22.62, 1224)
  -> route lookup
  -> local blackhole / unreachable route
  -> ENETUNREACH
```
"""
                ),
                deno(
                    """
const observation = {
  runtimeError: "TypeError: fetch failed",
  causeCode: "ENETUNREACH",
  syscall: "connect",
  transport: "TCP",
  connectionEstablished: false,
  applicationResponseReceived: false,
};

const interpretation = observation.causeCode === "ENETUNREACH"
  ? "route selection failed before the observed TCP connection completed"
  : "requires separate analysis";

({ observation, interpretation });
"""
                ),
                md(
                    """
| Network observation | Interpretation | Confidence |
|---|---|---|
| direct IP and port embedded in stage | intended command endpoint | high, static |
| `connect ENETUNREACH` | observed TCP connection did not complete | high, runtime |
| no application response in trace | no observed tasking on that attempt | high for captured run |
| absence of full PCAP | other attempts cannot be excluded | bounded uncertainty |

The failure weighs strongly against completed direct-IP C2 transmission during
the observed attempt. It does not retroactively disprove the earlier serverless
POST, which used a different destination and produced a stage-two response.

**Packet capture would prove:** SYN attempts, replies, completed handshakes, and
visible payload bytes.

**Proxy logs would prove:** URL, timing, status, and potentially query data for
proxied HTTP requests.

**Process telemetry would prove:** which PID initiated each socket and its npm
ancestry.

**Control:** egress policy plus a blackhole route blocked the direct-IP path.
**Detection:** alert on Node under npm ancestry connecting directly to rare
Internet IPs and nonstandard ports.
"""
                ),
            ],
        ),
        "06-ioc-and-artifact-derivation.ipynb": notebook(
            "IOC and Artifact Derivation",
            "python3",
            [
                md(
                    """
## Derivation Goal

An IOC list should be reproducible from public evidence without exposing raw
private captures. This workbook normalizes a reviewed catalog containing only
already-public indicators and sanitized artifact references.

Indicators are not verdicts. Shared hosting addresses, repository names, and
generic command fragments need context, time bounds, and corroboration.
"""
                ),
                py(
                    """
import csv
import io
import json
from pathlib import Path

catalog = json.loads(
    Path("../fixtures/public-artifact-catalog.json").read_text()
)
records = catalog["records"]

normalized = []
seen = set()
for record in records:
    key = (record["type"].lower(), str(record["value"]).strip())
    if key in seen:
        continue
    seen.add(key)
    normalized.append({
        "type": key[0],
        "value": key[1],
        "context": record["context"],
    })

normalized
"""
                ),
                py(
                    """
grouped = {}
for record in normalized:
    grouped.setdefault(record["type"], []).append(record)

{ioc_type: len(items) for ioc_type, items in sorted(grouped.items())}
"""
                ),
                md(
                    """
## Public Indicator Classes

| Class | Defensive use | Caution |
|---|---|---|
| domains and URLs | proxy/DNS review, repository scanning | serverless infrastructure may be shared or ephemeral |
| direct IP and port | firewall, flow, process-network correlation | time-bound ownership and reuse matter |
| SHA-256 | exact artifact matching | hash covers only the captured byte sequence |
| lifecycle command | manifest and endpoint review | fragments can have benign uses |
| custom header | proxy or application log hunting | requires HTTP visibility |
| artifact reference | evidence navigation | not itself an IOC |
"""
                ),
                py(
                    """
buffer = io.StringIO()
writer = csv.DictWriter(buffer, fieldnames=["type", "value", "context"])
writer.writeheader()
writer.writerows(normalized)
csv_preview = buffer.getvalue()

json_preview = json.dumps(normalized, indent=2)
{"csv": csv_preview, "json": json_preview}
"""
                ),
                md(
                    """
## Evidence Hygiene

The catalog includes the public stage hash, public endpoints, direct-IP IOC,
port, lifecycle command, request marker, repository identity, and references
to public evidence documents. It excludes environment values, credentials,
cookies, auth headers, and the raw stage body.

**Strongest supported claim:** these indicators occur in the preserved evidence
and public report.

**Not proven by an IOC match alone:** malicious intent for every appearance or
successful compromise of another host.

**Detection:** combine at least two dimensions, such as npm ancestry plus a
custom header, or direct-IP egress plus the stage hash.

**Confidence upgrade:** timestamped DNS/proxy/flow telemetry, file provenance,
and process ancestry tied to the matching indicator.
"""
                ),
            ],
        ),
        "07-evidence-boundary-and-claim-classification.ipynb": notebook(
            "Evidence Boundary and Claim Classification",
            "python3",
            [
                md(
                    """
## Why This Notebook Matters

Incident reports fail when possibility is rewritten as fact. This case has a
clear ladder:

```text
code capability
  != observed local execution
  != likely transmission
  != proven completed transmission
```

The matrix below turns each material claim into a classification, supporting
artifact, missing proof source, publication-safe wording, and defensive control.
"""
                ),
                py(
                    """
claims = [
    {
        "claim": "root npm install was executed",
        "classification": "observed",
        "artifact": "victim account plus preserved install/runtime context",
        "missing_evidence": "complete shell audit trail",
        "public_wording": "The user ran the root install.",
        "control": "review before install; isolated host",
    },
    {
        "claim": "prepare supplied automatic execution capability",
        "classification": "proven",
        "artifact": "preserved pre-containment package manifest",
        "missing_evidence": "none for capability",
        "public_wording": "The prepare lifecycle created an automatic execution path.",
        "control": "disable lifecycle scripts during first review",
    },
    {
        "claim": "node server launched through the fallback path",
        "classification": "observed",
        "artifact": "manifest command plus reconstructed nohup runtime evidence",
        "missing_evidence": "full process accounting",
        "public_wording": "Runtime evidence is consistent with the Linux fallback launch.",
        "control": "alert on npm -> shell -> nohup -> node ancestry",
    },
    {
        "claim": "server import chain reached socket/auth logic",
        "classification": "observed",
        "artifact": "static import chain plus executor origin in runtime trace",
        "missing_evidence": "module-load telemetry",
        "public_wording": "The import chain reached the first-stage loader path.",
        "control": "review top-level module calls",
    },
    {
        "claim": "environment POST path occurred",
        "classification": "likely",
        "artifact": "first-stage code plus returned stage-two execution",
        "missing_evidence": "receiver log or preserved request body",
        "public_wording": "The first-stage environment POST likely succeeded.",
        "control": "empty environment and egress deny",
    },
    {
        "claim": "serverless endpoint returned stage-two JavaScript",
        "classification": "proven",
        "artifact": "captured response hash plus runtime executor trace",
        "missing_evidence": "none for returned captured bytes",
        "public_wording": "The endpoint returned the captured stage, which the loader executed.",
        "control": "never grant response text execution authority",
    },
    {
        "claim": "stage two attempted direct-IP C2",
        "classification": "observed",
        "artifact": "public IOC plus connect ENETUNREACH runtime error",
        "missing_evidence": "full packet capture",
        "public_wording": "The stage attempted a direct-IP connection that failed in the observed run.",
        "control": "direct-IP egress block and process-network monitoring",
    },
    {
        "claim": "direct-IP C2 completed",
        "classification": "not proven",
        "artifact": "observed error weighs against completion",
        "missing_evidence": "successful handshake, response, or server log",
        "public_wording": "Direct-IP C2 completion was not demonstrated.",
        "control": "retain flow and packet telemetry",
    },
    {
        "claim": "remote tasking executed",
        "classification": "not proven",
        "artifact": "capability exists in static stage features",
        "missing_evidence": "task response and resulting local effect",
        "public_wording": "Remote tasking was possible but not observed.",
        "control": "block egress and detect response-to-code flows",
    },
    {
        "claim": "credential files were stolen",
        "classification": "not evidenced",
        "artifact": "not shown in captured stage",
        "missing_evidence": "file access plus transmission evidence",
        "public_wording": "Credential-file theft was not evidenced.",
        "control": "secret isolation and file-access telemetry",
    },
    {
        "claim": "wallet files were stolen",
        "classification": "not evidenced",
        "artifact": "not shown in captured stage",
        "missing_evidence": "wallet-file access plus transmission evidence",
        "public_wording": "Wallet-file theft was not evidenced.",
        "control": "separate wallets from review hosts",
    },
]
claims
"""
                ),
                py(
                    """
from collections import Counter

Counter(row["classification"] for row in claims)
"""
                ),
                md(
                    """
## Reading the Matrix

- **Proven** answers a narrow proposition directly from preserved evidence.
- **Observed** means runtime or user evidence shows the path occurred.
- **Likely** is a strong inference with a named missing proof source.
- **Plausible** should be reserved for architecturally possible follow-on action.
- **Not proven** means evidence does not close the claim.
- **Not evidenced** means the reviewed artifacts do not show the behavior.

Absence of proof is not always proof of absence. But public wording must remain
inside the available evidence, especially for high-impact claims such as
credential or wallet theft.
"""
                ),
                py(
                    """
publication_test = [
    {
        "question": "Does the wording name the supporting artifact?",
        "required": True,
    },
    {
        "question": "Does it separate capability from execution?",
        "required": True,
    },
    {
        "question": "Does it identify missing network or receiver evidence?",
        "required": True,
    },
    {
        "question": "Would a reasonable reader mistake possibility for fact?",
        "required_answer": "no",
    },
]
publication_test
"""
                ),
                md(
                    """
## Final Evidence-Bound Conclusion

The strongest public conclusion is that the root install activated the
lifecycle path, the import chain reached the loader, returned stage-two code
executed, and that stage attempted a direct-IP connection. The observed
connection failed with `ENETUNREACH`.

The first-stage environment POST likely completed because a stage was returned,
but the exact received body is withheld and not fully asserted. Direct-IP C2
completion, remote task execution, credential-file theft, and wallet-file theft
remain unproven or not evidenced.

The operational lesson is broader than this repository: treat package install,
module import, remote response handling, environment reachability, and network
egress as explicit trust boundaries. Preserve enough telemetry to distinguish
what code could do from what it actually did.
"""
                ),
            ],
        ),
    }


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    generated = specs()
    for path in OUT.glob("*.ipynb"):
        path.unlink()
    for filename, value in generated.items():
        value.metadata["metaplay_publication"]["source_builder"] = Path(__file__).name
        nbformat.validate(value)
        nbformat.write(value, OUT / filename)
    print(f"Wrote {len(generated)} reviewed notebooks to {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
