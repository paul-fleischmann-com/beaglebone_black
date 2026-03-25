"""Tests für SARIF-Konverter (TOOL-SAR-001, TOOL-SAR-002)"""
import json
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import shellcheck_to_sarif as sc
import junit_to_sonar_generic as jts


# ── TOOL-SAR-002: shellcheck_to_sarif ───────────────────────────────────────

def test_shellcheck_to_sarif_empty():
    """Leere Findings → valides SARIF mit 0 Results."""
    sarif = sc.convert([])
    assert sarif["version"] == "2.1.0"
    assert sarif["runs"][0]["results"] == []


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
    assert len(results) == 1
    assert results[0]["ruleId"] == "SC2086"
    assert "Double quote" in results[0]["message"]["text"]


# ── TOOL-SAR-001: junit_to_sonar_generic ────────────────────────────────────

JUNIT_PASS = """<?xml version="1.0"?>
<testsuites>
  <testsuite name="pkg/hal" tests="1" failures="0">
    <testcase classname="pkg/hal" name="TestFoo" time="0.01"/>
  </testsuite>
</testsuites>
"""

JUNIT_FAIL = """<?xml version="1.0"?>
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
    import xml.etree.ElementTree as ET
    in_file  = tmp_path / "junit.xml"
    out_file = tmp_path / "sonar.xml"
    in_file.write_text(JUNIT_PASS)
    jts.convert(str(in_file), str(out_file))
    tree = ET.parse(str(out_file))
    root = tree.getroot()
    failures = root.findall(".//testCase[@status='ERROR']") + root.findall(".//testCase[@status='FAILED']")
    assert len(failures) == 0


def test_junit_to_sonar_with_failure(tmp_path):
    """Fehlgeschlagener Test erscheint als <failure> Child im Sonar Generic XML."""
    import xml.etree.ElementTree as ET
    in_file  = tmp_path / "junit.xml"
    out_file = tmp_path / "sonar.xml"
    in_file.write_text(JUNIT_FAIL)
    jts.convert(str(in_file), str(out_file))
    tree = ET.parse(str(out_file))
    root = tree.getroot()
    failures = root.findall(".//failure")
    assert len(failures) >= 1
    assert "assert failed" in (failures[0].get("message", "") or failures[0].text or "")
