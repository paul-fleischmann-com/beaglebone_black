#!/usr/bin/env python3
"""Convert StrictDoc requirements coverage gaps to SARIF 2.1.0.

Requirements without any TYPE: File relations are reported as SARIF findings
so they appear as Code Smells in SonarQube / GitHub Code Scanning.

Usage:
    python3 strictdoc_to_sarif.py [--sdoc-glob GLOB] [--output FILE]

Defaults:
    --sdoc-glob  docs/requirements/**/*.sdoc
    --output     reports/requirements-coverage.sarif
"""
import argparse
import glob
import json
import os
import re
import sys
from pathlib import Path


RULE_ID = "REQ-UNCOVERED"
REQUIREMENT_TYPES = re.compile(
    r"^\[(?:REQUIREMENT|SW_REQUIREMENT|SYS_REQUIREMENT|GUI_REQUIREMENT"
    r"|HW_DRV_REQUIREMENT|HW_REQUIREMENT|SECTION|/SECTION|DOCUMENT|TEXT)\]",
    re.MULTILINE,
)


def parse_sdoc_file(sdoc_path: str) -> list[dict]:
    """Parse a .sdoc file and return list of requirement dicts with line numbers."""
    content = open(sdoc_path, encoding="utf-8").read()
    lines = content.splitlines()

    # Build a line-number index: char offset → line number
    offsets: list[int] = [0]
    for line in lines:
        offsets.append(offsets[-1] + len(line) + 1)

    def char_to_line(pos: int) -> int:
        lo, hi = 0, len(offsets) - 1
        while lo < hi:
            mid = (lo + hi) // 2
            if offsets[mid] <= pos < offsets[mid + 1]:
                return mid + 1
            elif pos < offsets[mid]:
                hi = mid
            else:
                lo = mid + 1
        return lo + 1

    # Split on any known block header
    req_types = re.compile(
        r"\[(?:REQUIREMENT|SW_REQUIREMENT|SYS_REQUIREMENT|GUI_REQUIREMENT"
        r"|HW_DRV_REQUIREMENT|HW_REQUIREMENT)\]"
    )

    reqs = []
    for m in req_types.finditer(content):
        start = m.start()
        # Find end: next block header or end of file
        next_block = REQUIREMENT_TYPES.search(content, m.end())
        block = content[m.end(): next_block.start() if next_block else len(content)]
        line_no = char_to_line(start)

        uid_m = re.search(r"^UID:\s*(.+)$", block, re.MULTILINE)
        title_m = re.search(r"^TITLE:\s*(.+)$", block, re.MULTILINE)
        status_m = re.search(r"^STATUS:\s*(.+)$", block, re.MULTILINE)

        if not uid_m:
            continue

        uid = uid_m.group(1).strip()
        title = title_m.group(1).strip() if title_m else uid
        status = status_m.group(1).strip() if status_m else "Active"

        # Collect all RELATIONS blocks: TYPE + VALUE pairs
        has_file_relation = bool(
            re.search(r"TYPE:\s*File", block, re.MULTILINE)
        )

        reqs.append({
            "uid": uid,
            "title": title,
            "status": status,
            "has_file": has_file_relation,
            "line": line_no,
            "file": sdoc_path,
        })

    return reqs


def to_sarif(gaps: list[dict], sdoc_glob: str) -> dict:
    """Convert a list of uncovered requirements to a SARIF document."""
    results = []
    for req in gaps:
        uri = req["file"].replace("\\", "/")
        # Make path relative to workspace root if possible
        try:
            uri = str(Path(uri).relative_to(Path.cwd())).replace("\\", "/")
        except ValueError:
            pass

        results.append({
            "ruleId": RULE_ID,
            "level": "warning",
            "message": {
                "text": (
                    f"Requirement {req['uid']} '{req['title']}' has no File relations. "
                    f"Link it to at least one implementation or test file via "
                    f"RELATIONS / TYPE: File."
                )
            },
            "locations": [{
                "physicalLocation": {
                    "artifactLocation": {
                        "uri": uri,
                        "uriBaseId": "%SRCROOT%",
                    },
                    "region": {"startLine": req["line"]},
                }
            }],
            "properties": {
                "uid": req["uid"],
                "status": req["status"],
            },
        })

    return {
        "$schema": "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json",
        "version": "2.1.0",
        "runs": [{
            "tool": {
                "driver": {
                    "name": "StrictDoc Requirements Coverage",
                    "version": "1.0.0",
                    "informationUri": "https://github.com/paulefl/beaglebone-tooling",
                    "rules": [{
                        "id": RULE_ID,
                        "name": "UncoveredRequirement",
                        "shortDescription": {"text": "Requirement without File relation"},
                        "fullDescription": {
                            "text": (
                                "A requirement has no TYPE: File relations. "
                                "Every requirement should be linked to at least one "
                                "implementation or test file to ensure traceability."
                            )
                        },
                        "defaultConfiguration": {"level": "warning"},
                        "properties": {"tags": ["requirements", "traceability"]},
                    }],
                }
            },
            "results": results,
        }],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--sdoc-glob",
        default="docs/requirements/**/*.sdoc",
        help="Glob pattern for .sdoc files (default: docs/requirements/**/*.sdoc)",
    )
    parser.add_argument(
        "--output",
        default="reports/requirements-coverage.sarif",
        help="Output SARIF file path (default: reports/requirements-coverage.sarif)",
    )
    args = parser.parse_args()

    sdoc_files = glob.glob(args.sdoc_glob, recursive=True)
    if not sdoc_files:
        print(f"No .sdoc files found matching: {args.sdoc_glob}", file=sys.stderr)
        # Write empty SARIF so downstream steps don't fail
        sarif = to_sarif([], args.sdoc_glob)
        os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(sarif, f, indent=2)
        print(f"Written: {args.output} (0 findings — no .sdoc files found)")
        return

    all_reqs: list[dict] = []
    for path in sorted(sdoc_files):
        all_reqs.extend(parse_sdoc_file(path))

    gaps = [r for r in all_reqs if not r["has_file"]]

    sarif = to_sarif(gaps, args.sdoc_glob)

    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(sarif, f, indent=2, ensure_ascii=False)

    total = len(all_reqs)
    print(
        f"Written: {args.output} "
        f"({len(gaps)} uncovered / {total} total requirements)"
    )


if __name__ == "__main__":
    main()
