#!/usr/bin/env python3
"""Generate a StrictDoc traceability summary and write it to GITHUB_STEP_SUMMARY.

Uses 'strictdoc export --formats json' as the data source — no fragile sdoc
regex parsing. If a pre-generated JSON file is provided via --json, that is
used directly; otherwise strictdoc is invoked automatically.
"""

import argparse
import json
import os
import subprocess
import sys
import tempfile


def export_json(input_path=".", output_dir=None):
    """Run strictdoc export --formats json and return path to index.json."""
    if output_dir is None:
        output_dir = tempfile.mkdtemp(prefix="strictdoc_json_")
    result = subprocess.run(
        ["strictdoc", "export", input_path, "--formats", "json",
         "--output-dir", output_dir, "--no-parallelization"],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        print(result.stderr, file=sys.stderr)
        sys.exit(result.returncode)
    return os.path.join(output_dir, "json", "index.json")


def parse_json(json_path):
    """Extract requirements with File relations from strictdoc JSON export."""
    with open(json_path) as f:
        data = json.load(f)

    reqs = []
    for doc in data.get("DOCUMENTS", []):
        doc_title = doc.get("TITLE", "—")
        for node in doc.get("NODES", []):
            node_type = node.get("_NODE_TYPE", "")
            if not node_type.endswith("REQUIREMENT"):
                continue
            uid = node.get("UID")
            if not uid:
                continue
            file_rels = [
                r["VALUE"] for r in node.get("RELATIONS", [])
                if r.get("TYPE") == "File" and r.get("VALUE")
            ]
            reqs.append({
                "uid":       uid,
                "title":     node.get("TITLE") or "—",
                "doc":       doc_title,
                "relations": file_rels,
            })
    return reqs


def build_summary(reqs, pages_url=None):
    total  = len(reqs)
    traced = sum(1 for r in reqs if r["relations"])
    pct    = round(traced / total * 100) if total else 0
    gate   = pct >= 80

    lines = [
        "## 📋 StrictDoc Traceability Report\n",
        "| Metrik | Wert |",
        "|--------|------|",
        f"| Anforderungen gesamt | **{total}** |",
        f"| Mit Traceability     | **{traced}** |",
        f"| Ohne Traceability    | **{total - traced}** |",
        f"| Abdeckung            | **{pct}%** {'✅' if gate else '❌'} |",
        f"| Quality Gate (≥80%)  | {'✅ Bestanden' if gate else '❌ Nicht bestanden'} |",
        "",
        "### Traceability Matrix\n",
        "| UID | Titel | Dokument | Verknüpfte Dateien |",
        "|-----|-------|----------|--------------------|",
    ]
    for r in sorted(reqs, key=lambda x: x["uid"]):
        files = " · ".join(f"`{f}`" for f in r["relations"]) if r["relations"] else "⚠️ keine"
        lines.append(f"| `{r['uid']}` | {r['title']} | {r['doc']} | {files} |")

    if pages_url:
        lines.append(f"\n🔗 [StrictDoc HTML-Dokumentation öffnen]({pages_url}) _(nur nach main-Deploy verfügbar)_")

    return "\n".join(lines)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json",        help="Pfad zu einer vorhandenen strictdoc JSON index.json")
    parser.add_argument("--input",       default=".", help="Eingabepfad für strictdoc (default: .)")
    parser.add_argument("--pages-url",   default="https://paulefl.github.io/beaglebone_black/strictdoc/")
    args = parser.parse_args()

    json_path = args.json or export_json(args.input)
    reqs      = parse_json(json_path)
    summary   = build_summary(reqs, args.pages_url)

    print(summary)

    summary_file = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_file:
        with open(summary_file, "a") as f:
            f.write(summary + "\n")
    else:
        print("\n(GITHUB_STEP_SUMMARY nicht gesetzt — lokale Ausführung)", file=sys.stderr)
