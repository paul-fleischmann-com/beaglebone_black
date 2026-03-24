#!/usr/bin/env python3
import xml.etree.ElementTree as ET
import urllib.request
import urllib.error
import json
import os
import sys

output_dir    = os.environ.get("OUTPUT_DIR", "bin")
xml_path      = os.path.join(output_dir, "coverage.xml")
sarif_path    = os.path.join(output_dir, "coverage.sarif")
summary_file  = os.environ.get("GITHUB_STEP_SUMMARY", "")
github_token  = os.environ.get("GITHUB_TOKEN", "")
github_repo   = os.environ.get("GITHUB_REPOSITORY", "")
github_sha    = os.environ.get("GITHUB_SHA", "")
source_prefix = os.environ.get("COVERAGE_SOURCE_PREFIX", "project/c")

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


# --- Per-package summary rows ---
rows = []
for pkg in cov_el.iter("package"):
    name = pkg.get("name", "")
    lr   = float(pkg.get("line-rate",   0)) * 100
    br   = float(pkg.get("branch-rate", 0)) * 100
    rows.append(f"| `{name}` | {badge(lr)} {lr:.1f}% | {badge(br)} {br:.1f}% |")

# --- Build SARIF for uncovered lines ---
sarif_results = []
for cls in cov_el.iter("class"):
    filename  = cls.get("filename", "")
    repo_path = f"{source_prefix}/{filename}".replace("//", "/")
    for line in cls.iter("line"):
        if int(line.get("hits", 1)) == 0:
            lineno    = int(line.get("number", 0))
            is_branch = line.get("branch", "false") == "true"
            rule_id   = "uncovered-branch" if is_branch else "uncovered-line"
            msg       = "Branch not covered by tests" if is_branch else "Line not covered by tests"
            sarif_results.append({
                "ruleId": rule_id,
                "message": {"text": msg},
                "locations": [{
                    "physicalLocation": {
                        "artifactLocation": {
                            "uri": repo_path,
                            "uriBaseId": "%SRCROOT%",
                        },
                        "region": {"startLine": lineno},
                    }
                }],
            })

sarif = {
    "$schema": "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json",
    "version": "2.1.0",
    "runs": [{
        "tool": {
            "driver": {
                "name": "C Coverage (gcovr)",
                "version": "1.0.0",
                "informationUri": "https://gcovr.com",
                "rules": [
                    {
                        "id": "uncovered-line",
                        "name": "UncoveredLine",
                        "shortDescription": {"text": "Line not covered by tests"},
                        "defaultConfiguration": {"level": "warning"},
                    },
                    {
                        "id": "uncovered-branch",
                        "name": "UncoveredBranch",
                        "shortDescription": {"text": "Branch not covered by tests"},
                        "defaultConfiguration": {"level": "note"},
                    },
                ],
            }
        },
        "results": sarif_results,
    }],
}

with open(sarif_path, "w") as f:
    json.dump(sarif, f, indent=2)
print(f"[coverage_summary] SARIF written: {sarif_path} ({len(sarif_results)} results)")

# --- Job Summary ---
title = f"C Coverage: {badge(line_rate)} {line_rate:.1f}% lines  {badge(branch_rate)} {branch_rate:.1f}% branches"
md = f"""## C Coverage Report
| | Lines | Branches |
|---|---|---|
| **Total** | {badge(line_rate)} **{line_rate:.1f}%** | {badge(branch_rate)} **{branch_rate:.1f}%** |

<details><summary>Per-package breakdown</summary>

| Package | Lines | Branches |
|---|---|---|
{chr(10).join(rows) if rows else "| — | — | — |"}
</details>

> Thresholds: 🟢 >=90%  🟡 >=75%  🔴 <75%
> {len(sarif_results)} uncovered lines — see Code Scanning tab for details.
"""

if summary_file:
    with open(summary_file, "a") as f:
        f.write(md)
    print("[coverage_summary] written to GITHUB_STEP_SUMMARY")

# --- GitHub Check Run (summary only, no annotations — SARIF handles line detail) ---
def gh_request(method, url, payload):
    req = urllib.request.Request(
        url, data=json.dumps(payload).encode(), method=method,
        headers={
            "Authorization": f"Bearer {github_token}",
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())


if github_token and github_repo and github_sha:
    conclusion = "success" if line_rate >= 75 else "failure"
    try:
        result = gh_request("POST", f"https://api.github.com/repos/{github_repo}/check-runs", {
            "name": "C Coverage",
            "head_sha": github_sha,
            "status": "completed",
            "conclusion": conclusion,
            "output": {"title": title, "summary": md},
        })
        print(f"[coverage_summary] check-run: {result['html_url']}")
    except urllib.error.HTTPError as e:
        print(f"[coverage_summary] check-run error: {e.code} {e.read().decode()}")

print(md)
