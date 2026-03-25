#!/usr/bin/env python3
"""Convert JUnit XML to SARIF 2.1.0 for GitHub Code Scanning.

Only failed and errored test cases are emitted as SARIF results —
passing tests produce no findings (Code Scanning shows issues, not passes).

SARIF spec: https://docs.oasis-open.org/sarif/sarif/v2.1.0/sarif-v2.1.0.html

Usage:
    python3 junit_to_sarif.py <junit.xml> <output.sarif> [tool-name]
"""
import json
import sys
import xml.etree.ElementTree as ET


def _classname_to_uri(classname: str) -> str:
    """Best-effort conversion of a JUnit classname to a source file URI."""
    if not classname:
        return "."
    # Python: tests.api.test_foo → tests/api/test_foo.py
    # Go:     github.com/org/repo/go-api/pkg/hal → go-api/pkg/hal
    parts = classname.replace(".", "/").split("/")
    # Strip common Go module prefixes (github.com / gitlab.com / ...)
    if len(parts) > 2 and parts[0] in ("github.com", "gitlab.com", "bitbucket.org"):
        parts = parts[3:]  # drop host/org/repo
    path = "/".join(parts)
    # Add .py extension for Python-style names (no slashes originally)
    if "." in classname and "/" not in classname:
        return path + ".py"
    return path


def convert(junit_path: str, output_path: str, tool_name: str = "test-runner") -> None:
    tree = ET.parse(junit_path)
    root = tree.getroot()

    suites = root.findall("testsuite") if root.tag == "testsuites" else [root]

    rules: list[dict] = []
    results: list[dict] = []
    seen_rules: set[str] = set()

    for suite in suites:
        suite_name = suite.get("name", "unknown-suite")

        for tc in suite.findall("testcase"):
            name = tc.get("name", "unknown")
            classname = tc.get("classname", "")
            rule_id = f"{suite_name}/{name}".replace(" ", "-")[:128]

            failure = tc.find("failure")
            error = tc.find("error")
            node = failure if failure is not None else error
            if node is None:
                continue  # skip passing / skipped tests

            level = "error" if node is not None else "warning"
            msg = node.get("message", name)
            body = (node.text or "").strip()
            full_msg = f"{msg}\n\n{body}".strip() if body else msg

            if rule_id not in seen_rules:
                seen_rules.add(rule_id)
                rules.append({
                    "id": rule_id,
                    "name": name,
                    "shortDescription": {"text": f"Test failed: {name}"},
                    "fullDescription": {"text": f"Test case '{name}' in suite '{suite_name}' failed."},
                    "defaultConfiguration": {"level": level},
                    "properties": {"tags": ["test-failure"]},
                })

            uri = _classname_to_uri(classname)
            results.append({
                "ruleId": rule_id,
                "level": level,
                "message": {"text": full_msg[:2000]},
                "locations": [{
                    "physicalLocation": {
                        "artifactLocation": {"uri": uri, "uriBaseId": "%SRCROOT%"},
                        "region": {"startLine": 1},
                    }
                }],
            })

    sarif = {
        "$schema": "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json",
        "version": "2.1.0",
        "runs": [{
            "tool": {
                "driver": {
                    "name": tool_name,
                    "version": "1.0.0",
                    "informationUri": "https://github.com/paulefl/beaglebone-tooling",
                    "rules": rules,
                }
            },
            "results": results,
        }],
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(sarif, f, indent=2, ensure_ascii=False)

    print(f"Written: {output_path} ({len(results)} finding(s) from {len(suites)} suite(s))")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <junit.xml> <output.sarif> [tool-name]")
        sys.exit(1)
    convert(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "test-runner")
