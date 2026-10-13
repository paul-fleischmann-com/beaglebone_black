#!/usr/bin/env python3
"""Convert JUnit XML to SonarQube Generic Test Execution format.

SonarQube Generic Test Execution format:
https://docs.sonarsource.com/sonarcloud/enriching/generic-test-data/#generic-test-execution

Usage:
    python3 scripts/junit_to_sonar_generic.py <junit.xml> <output.xml> [source-root]
"""
import sys
import xml.etree.ElementTree as ET


def convert(junit_path: str, output_path: str, source_root: str = "") -> None:
    tree = ET.parse(junit_path)
    root = tree.getroot()

    # Handle both <testsuites> and <testsuite> as root
    suites = root.findall("testsuite") if root.tag == "testsuites" else [root]

    out = ET.Element("testExecutions", version="1")

    # Aggregate by (file_path, test_name) to handle -count=N producing duplicates.
    # SonarQube rejects duplicate testCase names within the same file.
    # Strategy: keep worst outcome (failure > error > skipped > ok), sum durations.
    aggregated: dict[str, dict[str, dict]] = {}  # file_path -> name -> {duration_ms, outcome, msg, body}

    for suite in suites:
        for tc in suite.findall("testcase"):
            classname = tc.get("classname", "")
            name = tc.get("name", "unknown")
            duration_s = float(tc.get("time", "0") or "0")
            duration_ms = int(duration_s * 1000)

            file_path = _classname_to_path(classname, source_root)

            failure = tc.find("failure")
            error = tc.find("error")
            skipped = tc.find("skipped")

            if failure is not None:
                outcome = "failure"
                msg = failure.get("message", "failure")
                body = (failure.text or "").strip()
            elif error is not None:
                outcome = "error"
                msg = error.get("message", "error")
                body = (error.text or "").strip()
            elif skipped is not None:
                outcome = "skipped"
                msg = skipped.get("message", "skipped")
                body = ""
            else:
                outcome = "ok"
                msg = ""
                body = ""

            fp = aggregated.setdefault(file_path, {})
            if name not in fp:
                fp[name] = {"duration_ms": duration_ms, "outcome": outcome, "msg": msg, "body": body}
            else:
                existing = fp[name]
                existing["duration_ms"] += duration_ms
                # Escalate outcome: failure > error > skipped > ok
                rank = {"failure": 3, "error": 2, "skipped": 1, "ok": 0}
                if rank[outcome] > rank[existing["outcome"]]:
                    existing["outcome"] = outcome
                    existing["msg"] = msg
                    existing["body"] = body

    for file_path, tests in aggregated.items():
        file_el = ET.SubElement(out, "file", path=file_path)
        for name, data in tests.items():
            tc_el = ET.SubElement(file_el, "testCase", name=name, duration=str(data["duration_ms"]))
            if data["outcome"] == "failure":
                f_el = ET.SubElement(tc_el, "failure", message=data["msg"][:200])
                if data["body"]:
                    f_el.text = data["body"][:2000]
            elif data["outcome"] == "error":
                e_el = ET.SubElement(tc_el, "error", message=data["msg"][:200])
                if data["body"]:
                    e_el.text = data["body"][:2000]
            elif data["outcome"] == "skipped":
                ET.SubElement(tc_el, "skipped", message=data["msg"][:200])

    tree_out = ET.ElementTree(out)
    ET.indent(tree_out, space="  ")
    tree_out.write(output_path, encoding="unicode", xml_declaration=True)
    print(f"Written: {output_path} ({len(out)} file entries)")


def _classname_to_path(classname: str, source_root: str) -> str:
    """Convert Go package classname to relative file path."""
    if not classname:
        return "go-api/pkg/hal/hal_test.go"

    parts = classname.replace(".", "/").split("/")
    for i, p in enumerate(parts):
        if p in ("go-api", "pkg", "cmd", "tools"):
            path = "/".join(parts[i:])
            return f"{path}/{parts[-1]}_test.go"

    return f"{parts[-1]}/{parts[-1]}_test.go"


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <junit.xml> <output.xml> [source-root]")
        sys.exit(1)
    convert(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "")
