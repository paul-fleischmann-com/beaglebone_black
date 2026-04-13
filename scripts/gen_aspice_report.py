#!/usr/bin/env python3
"""
ASPICE Capability Level Report Generator
Liest workflow-state.json und prüft vorhandene Work Products.
Gibt einen Markdown-Report aus.

Usage:
    python3 scripts/gen_aspice_report.py
    python3 scripts/gen_aspice_report.py --output docs/reports/aspice_report.md
"""

import json
import os
import sys
import argparse
import subprocess
from datetime import date
from pathlib import Path

def check_file(*paths):
    """True wenn mindestens eine der Dateien/Globs existiert."""
    for p in paths:
        if Path(p).exists():
            return True
        # Glob-Unterstützung
        parent = Path(p).parent
        name = Path(p).name
        if '*' in name and parent.exists():
            if list(parent.glob(name)):
                return True
    return False

def count_grep(pattern, *files):
    """Zählt Treffer von pattern in files."""
    count = 0
    for f in files:
        if Path(f).exists():
            try:
                result = subprocess.run(
                    ['grep', '-c', pattern, f],
                    capture_output=True, text=True
                )
                count += int(result.stdout.strip()) if result.returncode == 0 else 0
            except Exception:
                pass
    return count

def run_cmd(cmd):
    """Führt Shell-Befehl aus, gibt stdout zurück."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
        return result.stdout.strip()
    except Exception:
        return ""

def check_sdoc_links():
    """Prüft ob SDOC_LINK-Kommentare in Code vorhanden sind."""
    result = run_cmd("grep -r 'SDOC_LINK' project/ Makefile 2>/dev/null | wc -l")
    return int(result) if result.isdigit() else 0

def assess_level(bps_ok, bps_total, work_products_ok, work_products_total):
    """Bewertet Capability Level basierend auf BP- und WP-Erfüllung."""
    bp_rate = bps_ok / bps_total if bps_total > 0 else 0
    wp_rate = work_products_ok / work_products_total if work_products_total > 0 else 0

    if bp_rate >= 0.85 and wp_rate >= 0.85:
        return 2, "Managed — alle BPs erfüllt, Work Products vorhanden"
    elif bp_rate >= 0.5:
        return 1, "Performed — Prozess wird ausgeführt, aber nicht vollständig gemanagt"
    else:
        return 0, "Incomplete — Prozess nicht oder kaum ausgeführt"

def check_swe1():
    bps = [
        ("BP1", "SYS→SWR Traceability",
         count_grep("VALUE: SYS-", "docs/requirements/software_requirements.sdoc") > 0),
        ("BP2", "Requirements klassifiziert (REQUIREMENT_TYPE)",
         count_grep("REQUIREMENT_TYPE:", "docs/requirements/software_requirements.sdoc") > 0),
        ("BP3", "Traceability-Matrix vorhanden",
         check_file("docs/requirements/traceability_matrix.md")),
        ("BP4", "Review-Protokoll vorhanden",
         bool(list(Path("docs/requirements").glob("review_*.md"))) if Path("docs/requirements").exists() else False),
        ("BP5", "SDOC_LINK in Code",
         check_sdoc_links() > 0),
        ("BP6", "Requirements dokumentiert",
         check_file("docs/requirements/software_requirements.sdoc")),
        ("BP7", "Requirements versioniert",
         bool(run_cmd("git log --oneline docs/requirements/ 2>/dev/null | head -1"))),
    ]
    wps = [
        ("SRS", check_file("docs/requirements/software_requirements.sdoc")),
        ("SYS-RS", check_file("docs/requirements/system_requirements.sdoc")),
        ("Traceability-Matrix", check_file("docs/requirements/traceability_matrix.md")),
        ("Review-Protokoll", bool(list(Path("docs/requirements").glob("review_*.md"))) if Path("docs/requirements").exists() else False),
    ]
    return bps, wps

def check_swe2():
    bps = [
        ("BP1", "Architektur aus Requirements abgeleitet",
         check_file("project/go-api/pkg/hal/interface.go")),
        ("BP2", "Architektur-Elemente identifiziert",
         check_file("project/go-api/pkg/hal/interface.go")),
        ("BP3", "Schnittstellen definiert",
         check_file("project/c/include/gpio.h", "project/rust-lib/src/lib.rs")),
        ("BP4", "Backends vollständig",
         check_file("project/go-api/pkg/hal/c/driver.go") and
         check_file("project/go-api/pkg/hal/rust/driver.go") and
         check_file("project/go-api/pkg/hal/mock/driver.go")),
    ]
    wps = [
        ("HAL Interface", check_file("project/go-api/pkg/hal/interface.go")),
        ("C Headers", check_file("project/c/include/gpio.h")),
        ("Rust FFI", check_file("project/rust-lib/src/lib.rs")),
    ]
    return bps, wps

def check_swe3():
    bps = [
        ("BP1", "API-Dokumentation vorhanden",
         bool(list(Path("docs").rglob("*.adoc"))) if Path("docs").exists() else False),
        ("BP2", "Schnittstellen dokumentiert",
         check_file("project/go-api/cmd/main.go")),
    ]
    wps = [
        ("API-Dokumentation (.adoc)", bool(list(Path("docs").rglob("*.adoc"))) if Path("docs").exists() else False),
    ]
    return bps, wps

def check_swe4():
    test_count = count_grep("^func Test", "project/go-api/pkg/hal/hal_test.go")
    coverage_exists = check_file("reports/coverage/coverage_func.txt")
    bps = [
        ("BP1", "Code entspricht Design (SDOC_LINK)",
         check_sdoc_links() > 0),
        ("BP2", "Unit Tests vorhanden",
         check_file("project/go-api/pkg/hal/hal_test.go") and test_count >= 4),
        ("BP3", "Tests ausgeführt (CI)",
         check_file(".drone.yml")),
        ("BP4", "Coverage gemessen",
         coverage_exists),
        ("BP5", "Code-Reviews durchgeführt",
         bool(run_cmd("gh pr list --state closed --limit 5 --json reviews --jq '.[].reviews | length > 0' 2>/dev/null"))),
    ]
    wps = [
        ("Unit Tests", check_file("project/go-api/pkg/hal/hal_test.go")),
        ("Coverage Report", coverage_exists),
        ("CI-Pipeline", check_file(".drone.yml")),
    ]
    return bps, wps

def check_swe5():
    bps = [
        ("BP1", "Integration geplant (CI-Pipeline)",
         check_file(".drone.yml")),
        ("BP2", "Integrationstests vorhanden",
         check_file("tests/api")),
        ("BP3", "Integrationstests ausgeführt",
         check_file("tests/api")),
    ]
    wps = [
        ("Integrationstests", check_file("tests/api")),
        ("CI-Reports", check_file("reports")),
    ]
    return bps, wps

def check_swe6():
    bps = [
        ("BP1", "Qualifikationstests definiert",
         check_file("tests/hardware")),
        ("BP2", "Tests auf Hardware ausgeführt",
         check_file("reports/hardware")),
        ("BP3", "Testergebnisse dokumentiert",
         check_file("reports/hardware")),
    ]
    wps = [
        ("Hardware-Tests", check_file("tests/hardware")),
        ("Test-Protokoll", check_file("reports/hardware")),
    ]
    return bps, wps

def check_man3():
    has_milestone = bool(run_cmd("gh milestone list 2>/dev/null | head -1"))
    bps = [
        ("BP1", "Projektumfang definiert (GitHub Issues)",
         bool(run_cmd("gh issue list --state open --limit 1 2>/dev/null"))),
        ("BP2", "Aufgaben verfolgt",
         check_file(".claude/workflow-state.json")),
        ("BP3", "Sprint-Milestones vorhanden", has_milestone),
    ]
    wps = [
        ("Workflow-State", check_file(".claude/workflow-state.json")),
        ("GitHub Issues", True),
    ]
    return bps, wps

def check_sup1():
    bps = [
        ("BP1", "QA-Strategie (CI-Gates)",
         check_file(".drone.yml")),
        ("BP2", "Code-Qualität geprüft (SonarQube)",
         check_file("sonar-project.properties")),
        ("BP3", "Coverage-Gate vorhanden",
         count_grep("coverage", "scripts/test.sh") > 0),
    ]
    wps = [
        ("CI-Pipeline", check_file(".drone.yml")),
        ("SonarQube-Konfiguration", check_file("sonar-project.properties")),
    ]
    return bps, wps

def check_sup8():
    has_tags = bool(run_cmd("git tag 2>/dev/null | head -1"))
    bps = [
        ("BP1", "Git-Versionierung aktiv", True),
        ("BP2", "Branch-Strategie (main + feature branches)",
         bool(run_cmd("git branch -r 2>/dev/null | head -1"))),
        ("BP3", "Releases/Tags vorhanden", has_tags),
    ]
    wps = [
        ("Git-Repository", True),
        ("Tags/Releases", has_tags),
    ]
    return bps, wps

PROCESS_CHECKS = {
    "SWE.1": ("Software Requirements Analysis", check_swe1),
    "SWE.2": ("Software Architectural Design", check_swe2),
    "SWE.3": ("Software Detailed Design", check_swe3),
    "SWE.4": ("Unit Construction & Testing", check_swe4),
    "SWE.5": ("Integration & Integration Testing", check_swe5),
    "SWE.6": ("Qualification Testing", check_swe6),
    "MAN.3": ("Project Management", check_man3),
    "SUP.1": ("Quality Assurance", check_sup1),
    "SUP.8": ("Configuration Management", check_sup8),
}

def generate_report(target_level=2):
    today = date.today().isoformat()
    lines = [
        f"# ASPICE Capability Level Report — BeagleBone Black",
        f"",
        f"**Generiert:** {today}  ",
        f"**Target Level:** {target_level}  ",
        f"**Tool:** `scripts/gen_aspice_report.py`",
        f"",
        f"---",
        f"",
        f"## Übersicht",
        f"",
        f"| Prozess | Name | BPs ✅ | WPs ✅ | Level | Status |",
        f"|---------|------|--------|--------|-------|--------|",
    ]

    process_results = {}
    for proc_id, (proc_name, check_fn) in PROCESS_CHECKS.items():
        try:
            bps, wps = check_fn()
        except Exception as e:
            bps, wps = [], []

        bps_ok = sum(1 for _, _, ok in bps if ok)
        wps_ok = sum(1 for _, ok in wps if ok)
        level, reason = assess_level(bps_ok, len(bps), wps_ok, len(wps))
        icon = {2: "✅", 1: "⚠️", 0: "❌"}.get(level, "❓")
        target_icon = "✅" if level >= target_level else ("⚠️" if level == target_level - 1 else "❌")

        lines.append(f"| **{proc_id}** | {proc_name} | {bps_ok}/{len(bps)} | {wps_ok}/{len(wps)} | {icon} Level {level} | {target_icon} |")
        process_results[proc_id] = (proc_name, bps, wps, level, reason)

    # Gesamtbewertung
    levels = [r[3] for r in process_results.values()]
    min_level = min(levels) if levels else 0
    avg_level = sum(levels) / len(levels) if levels else 0

    lines += [
        f"",
        f"**Minimum Level:** {min_level}  ",
        f"**Durchschnitt:** {avg_level:.1f}  ",
        f"",
        f"---",
        f"",
    ]

    # Detailbewertung je Prozess
    for proc_id, (proc_name, bps, wps, level, reason) in process_results.items():
        icon = {2: "✅", 1: "⚠️", 0: "❌"}.get(level, "❓")
        lines += [
            f"## {proc_id} — {proc_name}",
            f"",
            f"**Capability Level: {icon} {level}** — {reason}",
            f"",
            f"### Base Practices",
            f"",
            f"| BP | Beschreibung | Status |",
            f"|-----|-------------|--------|",
        ]
        for bp_id, bp_desc, ok in bps:
            lines.append(f"| {bp_id} | {bp_desc} | {'✅' if ok else '❌'} |")

        lines += [
            f"",
            f"### Work Products",
            f"",
            f"| Work Product | Status |",
            f"|---|---|",
        ]
        for wp_name, ok in wps:
            lines.append(f"| {wp_name} | {'✅' if ok else '❌'} |")

        lines.append(f"")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="ASPICE Capability Level Report Generator")
    parser.add_argument("--output", "-o", help="Ausgabedatei (default: stdout)")
    parser.add_argument("--target-level", type=int, default=2, help="ASPICE Target Level (default: 2)")
    args = parser.parse_args()

    # Zum Projektroot wechseln
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    os.chdir(project_root)

    report = generate_report(args.target_level)

    if args.output:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        Path(args.output).write_text(report)
        print(f"ASPICE Report geschrieben: {args.output}")
    else:
        print(report)


if __name__ == "__main__":
    main()
