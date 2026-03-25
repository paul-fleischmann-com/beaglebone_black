#!/usr/bin/env python3
"""Fetch SonarQube issues via API and generate a Markdown overview report.

Usage:
    python3 sonarqube_report.py \
        --host https://sonarcloud.io \
        --token <SONAR_TOKEN> \
        --project-key <project_key> \
        [--severities BLOCKER,CRITICAL,MAJOR] \
        [--types BUG,VULNERABILITY,CODE_SMELL] \
        [--output-file report.md] \
        [--step-summary]
"""
import argparse
import json
import sys
import urllib.request
import urllib.error
import urllib.parse
from base64 import b64encode
from collections import defaultdict

SEVERITY_EMOJI = {
    "BLOCKER": "🔴",
    "CRITICAL": "🟠",
    "MAJOR": "🟡",
    "MINOR": "🔵",
    "INFO": "⚪",
}

TYPE_LABEL = {
    "BUG": "Bug",
    "VULNERABILITY": "Vulnerability",
    "CODE_SMELL": "Code Smell",
    "SECURITY_HOTSPOT": "Hotspot",
}


def fetch_issues(host, token, project_key, severities, types, max_issues=500):
    """Fetch all matching issues from SonarQube API (paginated)."""
    issues = []
    page = 1
    page_size = 100

    auth = b64encode(f"{token}:".encode()).decode()
    headers = {"Authorization": f"Basic {auth}"}

    while len(issues) < max_issues:
        params = urllib.parse.urlencode({
            "componentKeys": project_key,
            "severities": severities,
            "types": types,
            "ps": page_size,
            "p": page,
            "s": "SEVERITY",
            "asc": "false",
        })
        url = f"{host.rstrip('/')}/api/issues/search?{params}"
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            print(f"⚠️  SonarQube API error: HTTP {e.code}", file=sys.stderr)
            return None, None
        except Exception as e:
            print(f"⚠️  SonarQube connection failed: {e}", file=sys.stderr)
            return None, None

        issues.extend(data.get("issues", []))
        total = data.get("total", 0)
        quality_gate = data.get("components", [{}])[0].get("qualityGate", {}) if data.get("components") else {}

        if len(data.get("issues", [])) < page_size or len(issues) >= total:
            break
        page += 1

    return issues, total


def fetch_quality_gate(host, token, project_key):
    """Fetch quality gate status for the project."""
    auth = b64encode(f"{token}:".encode()).decode()
    headers = {"Authorization": f"Basic {auth}"}
    url = f"{host.rstrip('/')}/api/qualitygates/project_status?projectKey={urllib.parse.quote(project_key)}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
            return data.get("projectStatus", {}).get("status", "UNKNOWN")
    except Exception:
        return "UNKNOWN"


def build_report(project_key, issues, total_count, quality_gate_status, severities_filter, types_filter):
    """Build Markdown report from issues list."""
    lines = []
    lines.append(f"## SonarQube Overview — `{project_key}`\n")

    # Quality gate status
    qg_icon = "✅" if quality_gate_status == "OK" else ("❌" if quality_gate_status == "ERROR" else "⚠️")
    lines.append(f"**Quality Gate:** {qg_icon} {quality_gate_status}\n")

    if issues is None:
        lines.append("> ⚠️ SonarQube nicht erreichbar oder Token fehlt — kein Report verfügbar.\n")
        return "\n".join(lines)

    lines.append(f"**Gefundene Issues:** {total_count} (angezeigt: {len(issues)})\n")
    lines.append(f"**Filter:** Severities: `{severities_filter}` | Typen: `{types_filter}`\n")

    # Summary table: Severity × Type
    counts = defaultdict(lambda: defaultdict(int))
    for issue in issues:
        sev = issue.get("severity", "UNKNOWN")
        typ = issue.get("type", "UNKNOWN")
        counts[sev][typ] += 1

    active_severities = [s for s in ["BLOCKER", "CRITICAL", "MAJOR", "MINOR", "INFO"] if s in severities_filter]
    active_types = [t for t in ["BUG", "VULNERABILITY", "CODE_SMELL"] if t in types_filter]

    if any(counts[s][t] > 0 for s in active_severities for t in active_types):
        lines.append("\n### Übersicht nach Severity\n")
        header = "| Severity | " + " | ".join(TYPE_LABEL.get(t, t) for t in active_types) + " | Gesamt |"
        sep = "|" + "---|" * (len(active_types) + 2)
        lines.append(header)
        lines.append(sep)
        for sev in active_severities:
            row_counts = [counts[sev][t] for t in active_types]
            total_row = sum(row_counts)
            if total_row == 0:
                continue
            emoji = SEVERITY_EMOJI.get(sev, "")
            cells = " | ".join(str(c) if c > 0 else "—" for c in row_counts)
            lines.append(f"| {emoji} {sev} | {cells} | **{total_row}** |")
        lines.append("")

    # Top issues table
    if issues:
        lines.append("\n### Top Issues\n")
        lines.append("| # | Typ | Severity | Regel | Datei | Zeile | Nachricht |")
        lines.append("|---|-----|----------|-------|-------|-------|-----------|")
        for i, issue in enumerate(issues[:50], 1):
            sev = issue.get("severity", "?")
            typ = issue.get("type", "?")
            rule = issue.get("rule", "?")
            component = issue.get("component", "?").split(":")[-1]  # strip project prefix
            line = issue.get("line", "?")
            msg = issue.get("message", "").replace("|", "\\|")[:80]
            emoji = SEVERITY_EMOJI.get(sev, "")
            lines.append(f"| {i} | {TYPE_LABEL.get(typ, typ)} | {emoji} {sev} | `{rule}` | `{component}` | {line} | {msg} |")

        if total_count > 50:
            lines.append(f"\n> ... und {total_count - 50} weitere Issues in SonarQube.")
    else:
        lines.append("\n> ✅ Keine Issues gefunden für die gewählten Filter.\n")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="SonarQube Issues → Markdown Report")
    parser.add_argument("--host", default="https://sonarcloud.io", help="SonarQube host URL")
    parser.add_argument("--token", required=True, help="SonarQube API token")
    parser.add_argument("--project-key", required=True, help="sonar.projectKey")
    parser.add_argument("--severities", default="BLOCKER,CRITICAL,MAJOR",
                        help="Comma-separated severities to include")
    parser.add_argument("--types", default="BUG,VULNERABILITY,CODE_SMELL",
                        help="Comma-separated issue types to include")
    parser.add_argument("--output-file", help="Write report to this file (in addition to stdout)")
    parser.add_argument("--step-summary", action="store_true",
                        help="Also write to $GITHUB_STEP_SUMMARY if set")
    args = parser.parse_args()

    issues, total = fetch_issues(
        args.host, args.token, args.project_key,
        args.severities, args.types,
    )
    qg_status = fetch_quality_gate(args.host, args.token, args.project_key)

    report = build_report(
        args.project_key, issues, total or 0,
        qg_status, args.severities, args.types,
    )

    print(report)

    if args.output_file:
        with open(args.output_file, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"Report written to {args.output_file}", file=sys.stderr)

    if args.step_summary:
        import os
        summary_file = os.environ.get("GITHUB_STEP_SUMMARY")
        if summary_file:
            with open(summary_file, "a", encoding="utf-8") as f:
                f.write(report + "\n")
            print(f"Report appended to GITHUB_STEP_SUMMARY", file=sys.stderr)


if __name__ == "__main__":
    main()
