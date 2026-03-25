#!/usr/bin/env python3
"""Generate a StrictDoc traceability summary and write it to GITHUB_STEP_SUMMARY."""

import os
import re
import glob
import sys


def parse_sdoc_files(sdoc_glob="docs/requirements/**/*.sdoc"):
    reqs = []
    for sdoc_file in glob.glob(sdoc_glob, recursive=True):
        content = open(sdoc_file).read()
        blocks = re.split(r'\[REQUIREMENT\]', content)[1:]
        for block in blocks:
            end = re.search(r'\[(?:REQUIREMENT|DOCUMENT|/)', block)
            block = block[:end.start()] if end else block
            uid   = re.search(r'^UID:\s*(.+)$',   block, re.M)
            title = re.search(r'^TITLE:\s*(.+)$', block, re.M)
            rels  = re.findall(r'VALUE:\s*(.+)',   block)
            if uid:
                reqs.append({
                    "uid":       uid.group(1).strip(),
                    "title":     title.group(1).strip() if title else "—",
                    "relations": [r.strip() for r in rels],
                    "doc":       os.path.basename(sdoc_file),
                })
    return reqs


def build_summary(reqs, pages_url=None):
    total   = len(reqs)
    traced  = sum(1 for r in reqs if r["relations"])
    pct     = round(traced / total * 100) if total else 0
    gate_ok = pct >= 80

    lines = []
    lines.append("## 📋 StrictDoc Traceability Report\n")
    lines.append("| Metrik | Wert |")
    lines.append("|--------|------|")
    lines.append(f"| Anforderungen gesamt | **{total}** |")
    lines.append(f"| Mit Traceability     | **{traced}** |")
    lines.append(f"| Ohne Traceability    | **{total - traced}** |")
    lines.append(f"| Abdeckung            | **{pct}%** {'✅' if gate_ok else '❌'} |")
    lines.append(f"| Quality Gate (≥80%)  | {'✅ Bestanden' if gate_ok else '❌ Nicht bestanden'} |")
    lines.append("")
    lines.append("### Traceability Matrix\n")
    lines.append("| UID | Titel | Dokument | Verknüpfte Dateien |")
    lines.append("|-----|-------|----------|--------------------|")
    for r in sorted(reqs, key=lambda x: x["uid"]):
        files = " · ".join(f"`{f}`" for f in r["relations"]) if r["relations"] else "⚠️ keine"
        lines.append(f"| `{r['uid']}` | {r['title']} | `{r['doc']}` | {files} |")

    if pages_url:
        lines.append(f"\n🔗 [StrictDoc HTML-Dokumentation öffnen]({pages_url}) _(nur nach main-Deploy verfügbar)_")

    return "\n".join(lines)


if __name__ == "__main__":
    reqs = parse_sdoc_files()
    pages_url = "https://paulefl.github.io/beaglebone_black/strictdoc/"
    summary = build_summary(reqs, pages_url)

    print(summary)

    summary_file = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_file:
        with open(summary_file, "a") as f:
            f.write(summary + "\n")
    else:
        print("\n(GITHUB_STEP_SUMMARY nicht gesetzt — lokale Ausführung)", file=sys.stderr)
