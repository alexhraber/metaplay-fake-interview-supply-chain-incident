#!/usr/bin/env python3
"""Write the static notebook learning hub used by GitHub Pages."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs/notebooks/index.html"

NOTEBOOKS = [
    (
        "00-python-lab-healthcheck.html",
        "Python Lab Healthcheck",
        "Verifies the local analysis environment and Python/Jupyter assumptions.",
    ),
    (
        "01-deno-js-runtime-healthcheck.html",
        "Deno JavaScript Runtime Healthcheck",
        "Verifies the JavaScript/TypeScript runtime path used for safe notebook exploration.",
    ),
    (
        "02-package-json-lifecycle-analysis.html",
        "package.json Lifecycle Analysis",
        "Examines npm lifecycle execution risk and why dependency installation is code execution.",
    ),
    (
        "03-stage2-static-deobfuscation-notes.html",
        "Stage-Two Static Deobfuscation Notes",
        "Documents static reasoning about the staged payload without executing attacker code.",
    ),
    (
        "04-ioc-extraction.html",
        "Public IOC Extraction",
        "Extracts and organizes already-public indicators of compromise from the evidence set.",
    ),
    (
        "05-behavior-map.html",
        "Behavior and Evidence Map",
        "Maps observed and inferred behavior while preserving capability, execution, and transmission boundaries.",
    ),
]


def main() -> int:
    missing = [
        filename
        for filename, _, _ in NOTEBOOKS
        if not (ROOT / "docs/notebooks" / filename).exists()
    ]
    if missing:
        raise SystemExit(f"Missing rendered notebooks: {', '.join(missing)}")

    items = "\n".join(
        (
            f'<li><a href="{filename}">{title}</a>'
            f"<p>{description}</p></li>"
        )
        for filename, title, description in NOTEBOOKS
    )
    OUTPUT.write_text(
        f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Defensive Analysis Notebooks</title>
  <link rel="stylesheet" href="../../assets/css/style.css">
</head>
<body>
  <main class="page">
    <article class="article">
      <h1>Rendered Analysis Notebooks</h1>
      <p>These notebooks are static HTML exports from the defensive MetaPlay
      incident analysis lab. They document controlled inspection steps, parsing
      logic, hashes, IOC extraction, behavior mapping, and evidence-bound
      reasoning.</p>
      <p>They are not live notebooks. They do not execute attacker-provided code
      in the browser. They are provided so readers can dig deeper into the
      technical nuance behind the incident report.</p>
      <nav class="top-nav">
        <a href="../../">Article</a>
        <a href="../../NOTEBOOKS.html">Notebook Guide</a>
      </nav>
      <h2>Suggested Reading Order</h2>
      <p>Start with the two runtime healthchecks, continue through lifecycle and
      staged-loader analysis, then finish with IOC extraction and the behavior
      map.</p>
      <ol>
        {items}
      </ol>
      <h2>Safety Boundary</h2>
      <p>The collection uses fake fixtures or indicators already published in
      the report. Raw executable payloads, raw environment captures, and private
      credential findings are intentionally withheld.</p>
    </article>
  </main>
</body>
</html>
""",
        encoding="utf-8",
    )
    print(f"Wrote {OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
