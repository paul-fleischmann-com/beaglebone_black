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

    for suite in suites:
        # Derive file path from classname of first test case
        for tc in suite.findall("testcase"):
            classname = tc.get("classname", "")
            name = tc.get("name", "unknown")
            duration_s = float(tc.get("time", "0") or "0")
            duration_ms = str(int(duration_s * 1000))

            # Convert Go package path to file path: github.com/.../pkg/hal → go-api/pkg/hal
            file_path = _classname_to_path(classname, source_root)

            # Find or create <file> element
            file_el = None
            for f in out.findall("file"):
                if f.get("path") == file_path:
                    file_el = f
                    break
            if file_el is None:
                file_el = ET.SubElement(out, "file", path=file_path)

            tc_el = ET.SubElement(file_el, "testCase", name=name, duration=duration_ms)

            failure = tc.find("failure")
            error = tc.find("error")
            skipped = tc.find("skipped")

            if failure is not None:
                msg = failure.get("message", "failure")
                body = (failure.text or "").strip()
                f_el = ET.SubElement(tc_el, "failure", message=msg[:200])
                if body:
                    f_el.text = body[:2000]
            elif error is not None:
                msg = error.get("message", "error")
                body = (error.text or "").strip()
                e_el = ET.SubElement(tc_el, "error", message=msg[:200])
                if body:
                    e_el.text = body[:2000]
            elif skipped is not None:
                msg = skipped.get("message", "skipped")
                ET.SubElement(tc_el, "skipped", message=msg[:200])

    tree_out = ET.ElementTree(out)
    ET.indent(tree_out, space="  ")
    tree_out.write(output_path, encoding="unicode", xml_declaration=True)
    print(f"Written: {output_path} ({len(out)} file entries)")


def _classname_to_path(classname: str, source_root: str) -> str:
    """Convert Go package classname to relative file path."""
    # e.g. github.com/paulefl/beaglebone_black/go-api/pkg/hal → go-api/pkg/hal/hal_test.go
    if not classname:
        return "go-api/pkg/hal/hal_test.go"

    # Strip module prefix (everything up to the repo name)
    parts = classname.replace(".", "/").split("/")
    # Find 'go-api' or similar segment
    for i, p in enumerate(parts):
        if p in ("go-api", "pkg", "cmd", "tools"):
            path = "/".join(parts[i:])
            return f"{path}/{parts[-1]}_test.go"

    # Fallback: use last segment
    return f"{parts[-1]}/{parts[-1]}_test.go"


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <junit.xml> <output.xml> [source-root]")
        sys.exit(1)
    convert(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "")
