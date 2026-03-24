#!/usr/bin/env python3
import xml.etree.ElementTree as ET
import urllib.request
import urllib.error
import json
import os
import sys

output_dir   = os.environ.get("OUTPUT_DIR", "bin")
xml_path     = os.path.join(output_dir, "coverage.xml")
summary_file = os.environ.get("GITHUB_STEP_SUMMARY", "")
github_token = os.environ.get("GITHUB_TOKEN", "")
github_repo  = os.environ.get("GITHUB_REPOSITORY", "")
github_sha   = os.environ.get("GITHUB_SHA", "")
# Maps the gcovr --root path (inside container) to the repo-relative path
# e.g. gcovr root was /src/c → files appear as "src/bme280.c" → repo path is "project/c/src/bme280.c"
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

# --- Annotations: uncovered lines per file ---
annotations = []
for cls in cov_el.iter("class"):
    filename = cls.get("filename", "")
    # Map container path to repo-relative path
    repo_path = f"{source_prefix}/{filename}".replace("//", "/")
    for line in cls.iter("line"):
        hits = int(line.get("hits", 1))
        if hits == 0:
            lineno = int(line.get("number", 0))
            is_branch = line.get("branch", "false") == "true"
            msg = "Branch not covered" if is_branch else "Line not covered"
            annotations.append({
                "path": repo_path,
                "start_line": lineno,
                "end_line": lineno,
                "annotation_level": "warning",
                "message": msg,
            })

print(f"[coverage_summary] {len(annotations)} uncovered lines found")

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
> {len(annotations)} uncovered lines annotated in the diff view.
"""

# Write to Job Summary
if summary_file:
    with open(summary_file, "a") as f:
        f.write(f"## C Coverage Report\n{md}")
    print("[coverage_summary] written to GITHUB_STEP_SUMMARY")


def gh_request(method, url, payload):
    data = json.dumps(payload).encode()
    req = urllib.request.Request(
        url, data=data, method=method,
        headers={
            "Authorization": f"Bearer {github_token}",
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())


if not (github_token and github_repo and github_sha):
    print("[coverage_summary] GITHUB_TOKEN/REPOSITORY/SHA not set — skipping check-run")
    print(md)
    sys.exit(0)

conclusion = "success" if line_rate >= 75 else "failure"
base_url = f"https://api.github.com/repos/{github_repo}/check-runs"

# Batch annotations (max 50 per request)
BATCH = 50
first_batch  = annotations[:BATCH]
rest_batches = [annotations[i:i+BATCH] for i in range(BATCH, len(annotations), BATCH)]

try:
    # POST: create check run (in_progress if more annotation batches follow)
    status = "in_progress" if rest_batches else "completed"
    payload = {
        "name": "C Coverage",
        "head_sha": github_sha,
        "status": status,
        "output": {
            "title": title,
            "summary": md,
            "annotations": first_batch,
        },
    }
    if status == "completed":
        payload["conclusion"] = conclusion

    result = gh_request("POST", base_url, payload)
    check_run_id = result["id"]
    print(f"[coverage_summary] check-run created: {result['html_url']}")

    # PATCH: send remaining annotation batches
    patch_url = f"{base_url}/{check_run_id}"
    for i, batch in enumerate(rest_batches):
        is_last = (i == len(rest_batches) - 1)
        patch_payload = {
            "output": {
                "title": title,
                "summary": md,
                "annotations": batch,
            },
        }
        if is_last:
            patch_payload["status"] = "completed"
            patch_payload["conclusion"] = conclusion
        gh_request("PATCH", patch_url, patch_payload)
        print(f"[coverage_summary] patch batch {i+1}/{len(rest_batches)} sent")

except urllib.error.HTTPError as e:
    print(f"[coverage_summary] API error: {e.code} {e.read().decode()}")

print(md)
