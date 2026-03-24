#!/usr/bin/env python3
import xml.etree.ElementTree as ET
import os
import sys

output_dir = os.environ.get("OUTPUT_DIR", "bin")
xml_path = os.path.join(output_dir, "coverage.xml")
summary_file = os.environ.get("GITHUB_STEP_SUMMARY", "")

print(f"[coverage_summary] OUTPUT_DIR={output_dir}")
print(f"[coverage_summary] xml_path={xml_path} exists={os.path.exists(xml_path)}")
print(f"[coverage_summary] GITHUB_STEP_SUMMARY={summary_file!r}")

if not os.path.exists(xml_path):
    print("[coverage_summary] coverage.xml not found — skipping summary")
    sys.exit(0)

tree = ET.parse(xml_path)
root = tree.getroot()

# gcovr Cobertura: root tag may be 'coverage' or wrapped in 'coverages'
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
"""

if summary_file:
    with open(summary_file, "a") as f:
        f.write(md)
    print("[coverage_summary] written to GITHUB_STEP_SUMMARY")
else:
    print("[coverage_summary] GITHUB_STEP_SUMMARY not set — printing only")

print(md)
