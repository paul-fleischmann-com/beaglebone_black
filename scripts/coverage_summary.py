#!/usr/bin/env python3
import xml.etree.ElementTree as ET
import urllib.request
import json
import os
import sys

output_dir = os.environ.get("OUTPUT_DIR", "bin")
xml_path = os.path.join(output_dir, "coverage.xml")
summary_file = os.environ.get("GITHUB_STEP_SUMMARY", "")
github_token = os.environ.get("GITHUB_TOKEN", "")
github_repo = os.environ.get("GITHUB_REPOSITORY", "")
github_sha = os.environ.get("GITHUB_SHA", "")

print(f"[coverage_summary] xml_path={xml_path} exists={os.path.exists(xml_path)}")

if not os.path.exists(xml_path):
    print("[coverage_summary] coverage.xml not found — skipping")
    sys.exit(0)

tree = ET.parse(xml_path)
root = tree.getroot()
cov_el = root if root.tag == "coverage" else root.find("coverage")
if cov_el is None:
    print(f"[coverage_summary] unexpected root tag: {root.tag} — skipping")
    sys.exit(0)

line_rate   = float(cov_el.get("line-rate",   0)) * 100
branch_rate = float(cov_el.get("branch-rate", 0)) * 100
print(f"[coverage_summary] lines={line_rate:.1f}% branches={branch_rate:.1f}%")


def badge(pct):
    if pct >= 90: return "🟢"
    if pct >= 75: return "🟡"
    return "🔴"


rows = []
for pkg in cov_el.iter("package"):
    name = pkg.get("name", "")
    lr   = float(pkg.get("line-rate",   0)) * 100
    br   = float(pkg.get("branch-rate", 0)) * 100
    rows.append(f"| `{name}` | {badge(lr)} {lr:.1f}% | {badge(br)} {br:.1f}% |")

title = f"C Coverage: {badge(line_rate)} {line_rate:.1f}% lines  {badge(branch_rate)} {branch_rate:.1f}% branches"

md = f"""| | Lines | Branches |
|---|---|---|
| **Total** | {badge(line_rate)} **{line_rate:.1f}%** | {badge(branch_rate)} **{branch_rate:.1f}%** |

<details><summary>Per-package breakdown</summary>

| Package | Lines | Branches |
|---|---|---|
{chr(10).join(rows) if rows else "| — | — | — |"}
</details>

> Thresholds: 🟢 >=90%  🟡 >=75%  🔴 <75%
"""

# Write to Job Summary
if summary_file:
    with open(summary_file, "a") as f:
        f.write(f"## C Coverage Report\n{md}")
    print("[coverage_summary] written to GITHUB_STEP_SUMMARY")

# Publish as GitHub Check Run (visible in Checks tab like dorny/test-reporter)
if github_token and github_repo and github_sha:
    conclusion = "success" if line_rate >= 75 else "failure"
    payload = {
        "name": "C Coverage",
        "head_sha": github_sha,
        "status": "completed",
        "conclusion": conclusion,
        "output": {
            "title": title,
            "summary": md,
        },
    }
    url = f"https://api.github.com/repos/{github_repo}/check-runs"
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode(),
        headers={
            "Authorization": f"Bearer {github_token}",
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    try:
        with urllib.request.urlopen(req) as resp:
            print(f"[coverage_summary] check-run created: {json.loads(resp.read())['html_url']}")
    except urllib.error.HTTPError as e:
        print(f"[coverage_summary] check-run failed: {e.code} {e.read().decode()}")
else:
    print("[coverage_summary] GITHUB_TOKEN/REPOSITORY/SHA not set — skipping check-run")

print(md)
