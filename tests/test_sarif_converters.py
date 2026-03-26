"""Tests für SARIF-Konverter (TOOL-SAR-001, TOOL-SAR-002)"""
import json
import os
import sys

import defusedxml.ElementTree as ET
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import shellcheck_to_sarif as sc
import junit_to_sonar_generic as jts


# ── TOOL-SAR-002: shellcheck_to_sarif ───────────────────────────────────────

def test_shellcheck_to_sarif_empty():
    """Leere Findings → valides SARIF mit 0 Results."""
    sarif = sc.convert([])
    if sarif["version"] != "2.1.0":
        pytest.fail(f"Expected SARIF version '2.1.0', got {sarif['version']!r}")
    if sarif["runs"][0]["results"] != []:
        pytest.fail("Expected empty results list for empty input")


def test_shellcheck_to_sarif_finding():
    """Ein Finding wird korrekt als SARIF Result serialisiert."""
    findings = [{
        "file": "scripts/test.sh",
        "line": 5,
        "endLine": 5,
        "column": 3,
        "endColumn": 10,
        "level": "warning",
        "code": 2086,
        "message": "Double quote to prevent globbing."
    }]
    sarif = sc.convert(findings)
    results = sarif["runs"][0]["results"]
    if len(results) != 1:
        pytest.fail(f"Expected 1 result, got {len(results)}")
    if results[0]["ruleId"] != "SC2086":
        pytest.fail(f"Expected ruleId 'SC2086', got {results[0]['ruleId']!r}")
    if "Double quote" not in results[0]["message"]["text"]:
        pytest.fail("Expected 'Double quote' in result message text")


# ── TOOL-SAR-001: junit_to_sonar_generic ────────────────────────────────────

JUNIT_ALL_GREEN = """<?xml version="1.0"?>
<testsuites>
  <testsuite name="pkg/hal" tests="1" failures="0">
    <testcase classname="pkg/hal" name="TestFoo" time="0.01"/>
  </testsuite>
</testsuites>
"""

JUNIT_WITH_FAILURE = """<?xml version="1.0"?>
<testsuites>
  <testsuite name="pkg/hal" tests="1" failures="1">
    <testcase classname="pkg/hal" name="TestBar" time="0.02">
      <failure message="assert failed">stacktrace here</failure>
    </testcase>
  </testsuite>
</testsuites>
"""


def test_junit_to_sonar_empty(tmp_path):
    """Alle Tests bestanden → 0 Failures in Sonar Generic XML."""

    in_file  = tmp_path / "junit.xml"
    out_file = tmp_path / "sonar.xml"
    in_file.write_text(JUNIT_ALL_GREEN)
    jts.convert(str(in_file), str(out_file))
    tree = ET.parse(str(out_file))
    root = tree.getroot()
    failures = root.findall(".//testCase[@status='ERROR']") + root.findall(".//testCase[@status='FAILED']")
    if len(failures) != 0:
        pytest.fail(f"Expected 0 failures for passing tests, got {len(failures)}")


def test_junit_to_sonar_with_failure(tmp_path):
    """Fehlgeschlagener Test erscheint als <failure> Child im Sonar Generic XML."""

    in_file  = tmp_path / "junit.xml"
    out_file = tmp_path / "sonar.xml"
    in_file.write_text(JUNIT_WITH_FAILURE)
    jts.convert(str(in_file), str(out_file))
    tree = ET.parse(str(out_file))
    root = tree.getroot()
    failures = root.findall(".//failure")
    if len(failures) < 1:
        pytest.fail("Expected at least one <failure> element in Sonar Generic XML")
    msg = failures[0].get("message", "") or failures[0].text or ""
    if "assert failed" not in msg:
        pytest.fail(f"Expected 'assert failed' in failure message, got {msg!r}")
