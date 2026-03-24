#!/usr/bin/env python3
import xml.etree.ElementTree as ET
import os
import sys

xml_path = os.path.join(os.environ.get("OUTPUT_DIR", "bin"), "coverage.xml")
if not os.path.exists(xml_path):
    print("coverage.xml not found, skipping summary")
    sys.exit(0)

tree = ET.parse(xml_path)
root = tree.getroot()
line_rate   = float(root.get("line-rate",   0)) * 100
branch_rate = float(root.get("branch-rate", 0)) * 100


def badge(pct):
    if pct >= 90: return "🟢"
    if pct >= 75: return "🟡"
    return "🔴"


rows = []
for pkg in root.iter("package"):
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
{chr(10).join(rows)}
</details>

> Thresholds: 🟢 >=90%  🟡 >=75%  🔴 <75%
"""

summary_file = os.environ.get("GITHUB_STEP_SUMMARY", "")
if summary_file:
    with open(summary_file, "a") as f:
        f.write(md)
print(md)
