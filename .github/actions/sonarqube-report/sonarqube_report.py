#!/usr/bin/env python3
"""Fetch open issues from SonarQube API and write a Markdown report."""

import argparse
import os
import sys
import urllib.request
import urllib.parse
import json
from datetime import datetime


def fetch_issues(host, token, project_key, severities, types):
    issues = []
    page = 1
    page_size = 500

    while True:
        params = urllib.parse.urlencode({
            "componentKeys": project_key,
            "severities": severities,
            "types": types,
            "resolved": "false",
            "ps": page_size,
            "p": page,
        })
        url = f"{host}/api/issues/search?{params}"
        req = urllib.request.Request(url)
        # Basic auth: token as username, empty password
        import base64
        creds = base64.b64encode(f"{token}:".encode()).decode()
        req.add_header("Authorization", f"Basic {creds}")

        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode())
        except Exception as e:
            print(f"⚠️  SonarQube API error: {e}", file=sys.stderr)
            return None

        issues.extend(data.get("issues", []))
        total = data.get("total", 0)
        if page * page_size >= total:
            break
        page += 1

    return issues


def severity_emoji(severity):
    return {
        "BLOCKER": "🔴",
        "CRITICAL": "🟠",
        "MAJOR": "🟡",
        "MINOR": "🔵",
        "INFO": "⚪",
    }.get(severity, "❓")


def type_label(issue_type):
    return {
        "BUG": "Bug",
        "VULNERABILITY": "Vulnerability",
        "CODE_SMELL": "Code Smell",
    }.get(issue_type, issue_type)


def build_markdown(issues, project_key, host, severities, types):
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        f"# SonarQube Issues Report",
        f"",
        f"**Project:** `{project_key}`  ",
        f"**Generated:** {now}  ",
        f"**Filter:** severities=`{severities}` types=`{types}`  ",
        f"**Total issues:** {len(issues)}",
        f"",
    ]

    if not issues:
        lines.append("✅ No open issues found matching the filter criteria.")
        return "\n".join(lines)

    # Group by severity
    by_severity = {}
    for issue in issues:
        sev = issue.get("severity", "UNKNOWN")
        by_severity.setdefault(sev, []).append(issue)

    severity_order = ["BLOCKER", "CRITICAL", "MAJOR", "MINOR", "INFO"]

    for sev in severity_order:
        group = by_severity.get(sev)
        if not group:
            continue
        emoji = severity_emoji(sev)
        lines.append(f"## {emoji} {sev} ({len(group)})")
        lines.append("")
        lines.append("| Type | Message | Component | Line |")
        lines.append("|------|---------|-----------|------|")
        for issue in group:
            component = issue.get("component", "").split(":")[-1]
            message = issue.get("message", "").replace("|", "\\|")
            line = issue.get("line", "")
            itype = type_label(issue.get("type", ""))
            issue_key = issue.get("key", "")
            url = f"{host}/project/issues?id={project_key}&open={issue_key}"
            lines.append(f"| {itype} | [{message}]({url}) | `{component}` | {line} |")
        lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", required=True)
    parser.add_argument("--token", required=True)
    parser.add_argument("--project-key", required=True)
    parser.add_argument("--severities", default="BLOCKER,CRITICAL,MAJOR")
    parser.add_argument("--types", default="BUG,VULNERABILITY,CODE_SMELL")
    parser.add_argument("--output-file", default="reports/sonarqube-report.md")
    parser.add_argument("--step-summary", action="store_true")
    args = parser.parse_args()

    issues = fetch_issues(
        args.host, args.token, args.project_key, args.severities, args.types
    )

    if issues is None:
        print("⚠️  Could not fetch issues — skipping report.", file=sys.stderr)
        sys.exit(0)

    report = build_markdown(issues, args.project_key, args.host, args.severities, args.types)

    with open(args.output_file, "w") as f:
        f.write(report)
    print(f"✅ Report written to {args.output_file} ({len(issues)} issues)")

    if args.step_summary:
        summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
        if summary_path:
            with open(summary_path, "a") as f:
                f.write(report)


if __name__ == "__main__":
    main()
