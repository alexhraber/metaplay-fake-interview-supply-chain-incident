#!/usr/bin/env python3
"""Generate the reviewed public notebook set without executing cells."""

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
    "> **Safety:** This notebook uses fake fixtures or already-public indicators. "
    "It does not execute attacker code, read the process environment, or contact "
    "network infrastructure."
)


def markdown(text: str):
    return nbformat.v4.new_markdown_cell(text.strip())


def code(text: str):
    return nbformat.v4.new_code_cell(text.strip())


def make_notebook(title: str, kernel: str, cells: list):
    if kernel == "python3":
        kernelspec = {"display_name": "Python 3", "language": "python", "name": "python3"}
        language_info = {"name": "python", "file_extension": ".py", "version": "3.12"}
    else:
        kernelspec = {"display_name": "Deno", "language": "typescript", "name": "deno"}
        language_info = {"name": "typescript", "file_extension": ".ts"}
    notebook = nbformat.v4.new_notebook()
    notebook.metadata = {
        "kernelspec": kernelspec,
        "language_info": language_info,
        "metaplay_publication": {
            "safe_static_analysis": True,
            "attacker_code_executed": False,
        },
    }
    notebook.cells = [
        markdown(f"# {title}\n\n{SAFETY}"),
        *cells,
        markdown(
            "## Evidence Gate\n\n"
            "State the strongest supported claim, strongest unsupported claim, "
            "missing proof, one preventive control, and one detective control."
        ),
    ]
    return notebook


def specs():
    return {
        "00-python-lab-healthcheck.ipynb": make_notebook(
            "Python Lab Healthcheck",
            "python3",
            [
                markdown(
                    "Verify the local Python notebook runtime without inspecting "
                    "environment variables, home directories, or private evidence."
                ),
                code(
                    """import platform
import sys

{
    "python": platform.python_version(),
    "implementation": platform.python_implementation(),
    "major_minor": sys.version_info[:2],
    "safe_checks_only": True,
}"""
                ),
                code(
                    """required = {"json", "pathlib", "hashlib"}
sorted(required)"""
                ),
                markdown(
                    "This proves the notebook kernel can run ordinary local Python. "
                    "It does not prove that private evidence is safe to load."
                ),
            ],
        ),
        "01-deno-js-runtime-healthcheck.ipynb": make_notebook(
            "Deno JavaScript Runtime Healthcheck",
            "deno",
            [
                markdown(
                    "Verify Deno and safe JavaScript data primitives. No permissions "
                    "or network operations are requested."
                ),
                code(
                    """({
  deno: Deno.version.deno,
  typescript: Deno.version.typescript,
  safeChecksOnly: true
});"""
                ),
                code(
                    """const loopback = new URL("http://127.0.0.1:9001/api/checkStatus");
loopback.search = new URLSearchParams({
  tid: "fake-token",
  sysId: "fake-system-id"
}).toString();
({ origin: loopback.origin, pathname: loopback.pathname, query: loopback.search });"""
                ),
                markdown(
                    "Constructing a URL object does not send a request. This cell "
                    "models serialization only."
                ),
            ],
        ),
        "02-package-json-lifecycle-analysis.ipynb": make_notebook(
            "package.json Lifecycle Analysis",
            "deno",
            [
                markdown(
                    "Parse an inert fake manifest and identify npm lifecycle hooks. "
                    "The strings are never passed to a shell or package manager."
                ),
                code(
                    """const text = await Deno.readTextFile("../fixtures/fake-package-json.json");
const packageJson = JSON.parse(text);
const lifecycle = new Set(["preinstall", "install", "postinstall", "prepare"]);
Object.entries(packageJson.scripts ?? {})
  .filter(([name]) => lifecycle.has(name))
  .map(([name, command]) => ({ name, command }));"""
                ),
                code(
                    """const reviewSignals = ["nohup", "start /b", "node server", "&"];
Object.entries(packageJson.scripts ?? {}).flatMap(([name, command]) =>
  reviewSignals
    .filter(signal => String(command).includes(signal))
    .map(signal => ({ name, signal }))
);"""
                ),
                markdown(
                    "A lifecycle string establishes automatic-execution capability. "
                    "Runtime evidence is still required to show it actually ran."
                ),
            ],
        ),
        "03-stage2-static-deobfuscation-notes.ipynb": make_notebook(
            "Stage-Two Static Deobfuscation Notes",
            "deno",
            [
                markdown(
                    "Practice safe decoding and behavior classification on invented "
                    "training strings. The captured payload is intentionally withheld."
                ),
                code(
                    """const fakeEncoded = "aHR0cDovLzEyNy4wLjAuMTo5MDAxL2FwaS9jaGVja1N0YXR1cw==";
const decoded = atob(fakeEncoded);
({ decoded, loopbackOnly: decoded.startsWith("http://127.0.0.1:") });"""
                ),
                code(
                    """const fakeStringTable = ["system profile", "poll interval", "task response"];
const rotation = 1;
const normalized = fakeStringTable
  .slice(rotation)
  .concat(fakeStringTable.slice(0, rotation));
normalized;"""
                ),
                code(
                    """const summary = JSON.parse(
  await Deno.readTextFile("../fixtures/fake-stage2-response-summary.json")
);
summary;"""
                ),
                markdown(
                    "Static decoding can reveal architecture and indicators. It does "
                    "not prove delivery, execution, or successful transmission."
                ),
            ],
        ),
        "04-ioc-extraction.ipynb": make_notebook(
            "Public IOC Extraction",
            "python3",
            [
                markdown(
                    "Parse indicators already published in `IOCs.md`. Treat every "
                    "URL and address as inert text; never request it."
                ),
                code(
                    """import json
from pathlib import Path

ioc_path = Path("../fixtures/iocs.public.json")
iocs = json.loads(ioc_path.read_text(encoding="utf-8"))
[(item["type"], item["context"]) for item in iocs["indicators"]]"""
                ),
                code(
                    """from collections import Counter

Counter(item["type"] for item in iocs["indicators"])"""
                ),
                code(
                    """def publication_record(item):
    return {
        "type": item["type"],
        "value": item["value"],
        "context": item["context"],
        "action": "correlate; do not contact",
    }

[publication_record(item) for item in iocs["indicators"]]"""
                ),
                markdown(
                    "An IOC supports correlation. Shared hosting indicators do not "
                    "independently establish attribution."
                ),
            ],
        ),
        "05-behavior-map.ipynb": make_notebook(
            "Behavior and Evidence Map",
            "python3",
            [
                markdown(
                    "Map claims to evidence classes. The governing rule is: "
                    "`capability != observed execution != proven transmission`."
                ),
                code(
                    """claims = [
    {
        "claim": "Install lifecycle could start the server",
        "class": "capability",
        "control": "review manifests and disable scripts",
    },
    {
        "claim": "Downloaded stage path produced a connect error",
        "class": "observed execution",
        "control": "egress isolation and process telemetry",
    },
    {
        "claim": "Direct-IP command service received the beacon",
        "class": "not proven",
        "control": "packet capture or proxy logging",
    },
    {
        "claim": "Credential files were stolen",
        "class": "not evidenced",
        "control": "file-access telemetry and credential isolation",
    },
]
claims"""
                ),
                code(
                    """from collections import defaultdict

by_class = defaultdict(list)
for item in claims:
    by_class[item["class"]].append(item["claim"])
dict(by_class)"""
                ),
                markdown(
                    "Filesystem reachability is not a theft claim. Attempted network "
                    "access is not completed transmission. State the missing evidence."
                ),
            ],
        ),
    }


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    for filename, notebook in specs().items():
        nbformat.write(notebook, OUT / filename)
    print(f"Wrote {len(specs())} reviewed notebooks to {OUT}")
    print("No cells were executed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

