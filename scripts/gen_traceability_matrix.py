#!/usr/bin/env python3
"""gen_traceability_matrix.py — Generiert docs/requirements/traceability_matrix.md.

Liest SDoc-Dateien (regex-basiert, kein strictdoc nötig) und sucht
SDOC_LINK-Kommentare im Quellcode um die vollständige Traceability-Kette
SYS → SWR → HW-DRV → Code zu dokumentieren.

Verwendung:
    python3 scripts/gen_traceability_matrix.py
    python3 scripts/gen_traceability_matrix.py --output docs/requirements/traceability_matrix.md
    python3 scripts/gen_traceability_matrix.py --check   # Exit 1 bei fehlenden Links
"""
import argparse
import os
import re
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
SDOC_DIR  = REPO_ROOT / "docs" / "requirements"
SOURCE_DIRS = [
    REPO_ROOT / "project" / "go-api",
    REPO_ROOT / "project" / "c",
    REPO_ROOT / "project" / "rust-lib",
    REPO_ROOT / "Makefile",
]
SOURCE_EXTS = {".go", ".c", ".h", ".rs"}


# ── SDoc Parser ───────────────────────────────────────────────────────────────

def parse_sdoc(path: Path) -> list[dict]:
    """Extrahiert Requirement-Blöcke aus einer SDoc-Datei (regex-basiert)."""
    text = path.read_text(encoding="utf-8")
    blocks = re.split(r'\n(?=\[)', text)
    reqs = []
    for block in blocks:
        node_match = re.match(r'\[(\w+)\]', block)
        if not node_match:
            continue
        node_type = node_match.group(1)
        if not node_type.endswith("REQUIREMENT"):
            continue

        uid_m   = re.search(r'^UID:\s*(.+)$', block, re.MULTILINE)
        title_m = re.search(r'^TITLE:\s*(.+)$', block, re.MULTILINE)
        if not uid_m:
            continue

        parents = re.findall(r'TYPE:\s*Parent\s*\n\s*VALUE:\s*(\S+)', block)
        reqs.append({
            "uid":      uid_m.group(1).strip(),
            "title":    title_m.group(1).strip() if title_m else "—",
            "type":     node_type,
            "parents":  parents,
            "doc":      path.name,
        })
    return reqs


def load_all_reqs() -> dict[str, dict]:
    """Liest alle SDoc-Dateien und gibt uid→req-Dict zurück."""
    reqs = {}
    for sdoc in sorted(SDOC_DIR.glob("*.sdoc")):
        for req in parse_sdoc(sdoc):
            reqs[req["uid"]] = req
    return reqs


# ── Quellcode Scanner ─────────────────────────────────────────────────────────

SDOC_LINK_PATTERN = re.compile(
    r'(?://|#)\s*\[?SDOC_LINK:\s*([A-Z][\w-]+)\]?'
)


def scan_source_links() -> dict[str, list[str]]:
    """Sucht SDOC_LINK-Kommentare im Quellcode. Gibt uid→[dateipfade] zurück."""
    links: dict[str, list[str]] = defaultdict(list)

    def scan_file(path: Path):
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            return
        for m in SDOC_LINK_PATTERN.finditer(text):
            uid = m.group(1).strip()
            rel = str(path.relative_to(REPO_ROOT))
            if rel not in links[uid]:
                links[uid].append(rel)

    for entry in SOURCE_DIRS:
        if entry.is_file():
            scan_file(entry)
        elif entry.is_dir():
            for ext in SOURCE_EXTS:
                for f in entry.rglob(f"*{ext}"):
                    scan_file(f)

    return dict(links)


# ── Matrix bauen ──────────────────────────────────────────────────────────────

def build_matrix(reqs: dict[str, dict], links: dict[str, list[str]]) -> dict:
    """Baut die SYS→SWR→HW-DRV→Code Hierarchie auf."""
    sys_reqs = {uid: r for uid, r in reqs.items() if uid.startswith("SYS-")}
    swr_reqs = {uid: r for uid, r in reqs.items() if uid.startswith("SWR-")}
    hwd_reqs = {uid: r for uid, r in reqs.items() if uid.startswith("HW-DRV-")}

    # SWR → parent SYS-*
    swr_by_sys: dict[str, list[str]] = defaultdict(list)
    swr_orphans: list[str] = []
    for uid, r in swr_reqs.items():
        sys_parents = [p for p in r["parents"] if p.startswith("SYS-")]
        if sys_parents:
            for p in sys_parents:
                swr_by_sys[p].append(uid)
        else:
            swr_orphans.append(uid)

    # HW-DRV → parent SWR-*
    hwd_by_swr: dict[str, list[str]] = defaultdict(list)
    hwd_orphans: list[str] = []
    for uid, r in hwd_reqs.items():
        swr_parents = [p for p in r["parents"] if p.startswith("SWR-")]
        if swr_parents:
            for p in swr_parents:
                hwd_by_swr[p].append(uid)
        else:
            hwd_orphans.append(uid)

    return {
        "sys_reqs": sys_reqs,
        "swr_reqs": swr_reqs,
        "hwd_reqs": hwd_reqs,
        "swr_by_sys": dict(swr_by_sys),
        "swr_orphans": swr_orphans,
        "hwd_by_swr": dict(hwd_by_swr),
        "hwd_orphans": hwd_orphans,
        "links": links,
    }


# ── Markdown Ausgabe ──────────────────────────────────────────────────────────

def render_markdown(m: dict) -> str:
    lines = [
        "# Traceability-Matrix — BeagleBone Black",
        "",
        f"**Generiert:** {date.today()}  ",
        f"**Tool:** `scripts/gen_traceability_matrix.py`  ",
        f"**ASPICE:** SWE.1 BP3/BP4/BP5 Work Product",
        "",
        "---",
        "",
        "## Legende",
        "",
        "| Symbol | Bedeutung |",
        "|--------|-----------|",
        "| ✅ | Traceability vollständig |",
        "| ⚠️ | Teilweise (kein SDOC_LINK im Code) |",
        "| ❌ | Keine Abdeckung |",
        "",
        "---",
        "",
        "## SYS → SWR → HW-DRV → Code",
        "",
    ]

    total_swr = len(m["swr_reqs"])
    linked_swr = sum(1 for uid in m["swr_reqs"] if uid in m["links"])

    for sys_uid in sorted(m["sys_reqs"]):
        sys_r = m["sys_reqs"][sys_uid]
        swr_children = sorted(m["swr_by_sys"].get(sys_uid, []))
        sys_icon = "✅" if swr_children else "❌"
        lines.append(f"### {sys_icon} `{sys_uid}` — {sys_r['title']}")
        lines.append("")

        if not swr_children:
            lines.append(f"> ❌ Keine SWR-Anforderung verweist auf `{sys_uid}`")
            lines.append("")
            continue

        lines.append("| SWR | Titel | HW-DRV | Code-Link |")
        lines.append("|-----|-------|--------|-----------|")

        for swr_uid in swr_children:
            swr_r = m["swr_reqs"].get(swr_uid, {"title": "—"})
            hwd_children = sorted(m["hwd_by_swr"].get(swr_uid, []))
            code_files = m["links"].get(swr_uid, [])

            hwd_str  = " ".join(f"`{h}`" for h in hwd_children) if hwd_children else "—"
            code_str = " ".join(f"`{f}`" for f in code_files)   if code_files   else "⚠️ kein SDOC_LINK"
            icon     = "✅" if code_files else "⚠️"

            lines.append(f"| {icon} `{swr_uid}` | {swr_r['title']} | {hwd_str} | {code_str} |")

        lines.append("")

    # Orphan SWRs (kein SYS-Parent)
    if m["swr_orphans"]:
        lines += [
            "---",
            "",
            "## SWR ohne SYS-Parent",
            "",
            "| SWR | Titel | Code-Link |",
            "|-----|-------|-----------|",
        ]
        for swr_uid in sorted(m["swr_orphans"]):
            swr_r = m["swr_reqs"].get(swr_uid, {"title": "—"})
            code_files = m["links"].get(swr_uid, [])
            code_str = " ".join(f"`{f}`" for f in code_files) if code_files else "⚠️ kein SDOC_LINK"
            lines.append(f"| `{swr_uid}` | {swr_r['title']} | {code_str} |")
        lines.append("")

    # Zusammenfassung
    missing_swr = [uid for uid in m["swr_reqs"] if uid not in m["links"]]
    lines += [
        "---",
        "",
        "## Zusammenfassung",
        "",
        "| Metrik | Wert |",
        "|--------|------|",
        f"| SYS-Anforderungen | {len(m['sys_reqs'])} |",
        f"| SWR-Anforderungen | {total_swr} |",
        f"| SWR mit SDOC_LINK im Code | {linked_swr} / {total_swr} |",
        f"| SWR ohne Code-Link | {len(missing_swr)} |",
        f"| HW-DRV-Anforderungen | {len(m['hwd_reqs'])} |",
        f"| SYS vollständig abgedeckt | {sum(1 for s in m['sys_reqs'] if m['swr_by_sys'].get(s))} / {len(m['sys_reqs'])} |",
        "",
    ]

    if missing_swr:
        lines.append("### SWR ohne SDOC_LINK im Code")
        lines.append("")
        for uid in sorted(missing_swr):
            lines.append(f"- `{uid}` — {m['swr_reqs'][uid]['title']}")
        lines.append("")

    return "\n".join(lines)


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output", "-o",
        default=str(REPO_ROOT / "docs" / "requirements" / "traceability_matrix.md"),
        help="Ausgabedatei (default: docs/requirements/traceability_matrix.md)"
    )
    parser.add_argument(
        "--check", action="store_true",
        help="Exit 1 wenn SWR ohne Code-Link oder SYS ohne SWR-Abdeckung"
    )
    parser.add_argument(
        "--stdout", action="store_true",
        help="Ausgabe auf stdout statt in Datei"
    )
    args = parser.parse_args()

    reqs  = load_all_reqs()
    links = scan_source_links()
    mat   = build_matrix(reqs, links)
    md    = render_markdown(mat)

    if args.stdout:
        print(md)
    else:
        out = Path(args.output)
        out.write_text(md, encoding="utf-8")
        print(f"✅ Traceability-Matrix geschrieben: {out}")

    if args.check:
        missing_swr = [uid for uid in mat["swr_reqs"] if uid not in mat["links"]]
        uncovered_sys = [s for s in mat["sys_reqs"] if not mat["swr_by_sys"].get(s)]
        issues = []
        if missing_swr:
            issues.append(f"{len(missing_swr)} SWR ohne SDOC_LINK: {', '.join(sorted(missing_swr))}")
        if uncovered_sys:
            issues.append(f"{len(uncovered_sys)} SYS ohne SWR: {', '.join(sorted(uncovered_sys))}")
        if issues:
            for i in issues:
                print(f"❌ {i}", file=sys.stderr)
            sys.exit(1)
        print("✅ Traceability vollständig")


if __name__ == "__main__":
    main()
