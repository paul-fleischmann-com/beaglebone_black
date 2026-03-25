"""Tests for sonarqube_report.py."""
import sys
import os
import json
import tempfile
from unittest.mock import patch, MagicMock
from io import BytesIO

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sonarqube_report import build_report, SEVERITY_EMOJI, TYPE_LABEL


SAMPLE_ISSUES = [
    {
        "severity": "BLOCKER",
        "type": "BUG",
        "rule": "c:S1035",
        "component": "myproject:c-lib/src/gpio.c",
        "line": 42,
        "message": "Null pointer dereference",
    },
    {
        "severity": "CRITICAL",
        "type": "VULNERABILITY",
        "rule": "python:S1313",
        "component": "myproject:go-api/main.go",
        "line": 7,
        "message": "Hard-coded IP address",
    },
    {
        "severity": "MAJOR",
        "type": "CODE_SMELL",
        "rule": "go:S1234",
        "component": "myproject:go-api/pkg/handler.go",
        "line": 99,
        "message": "Unused variable",
    },
]


def _require(condition, msg):
    """Raise AssertionError with a message if condition is False."""
    if not condition:
        raise AssertionError(msg)


class TestBuildReport:
    def test_contains_project_key(self):
        report = build_report("my-project", SAMPLE_ISSUES, 3, "OK",
                              "BLOCKER,CRITICAL,MAJOR", "BUG,VULNERABILITY,CODE_SMELL")
        _require("my-project" in report, "Project key missing from report")

    def test_quality_gate_ok(self):
        report = build_report("p", SAMPLE_ISSUES, 3, "OK",
                              "BLOCKER,CRITICAL,MAJOR", "BUG,VULNERABILITY,CODE_SMELL")
        _require("✅" in report, "OK gate should show ✅")
        _require("OK" in report, "'OK' missing from report")

    def test_quality_gate_error(self):
        report = build_report("p", SAMPLE_ISSUES, 3, "ERROR",
                              "BLOCKER,CRITICAL,MAJOR", "BUG,VULNERABILITY,CODE_SMELL")
        _require("❌" in report, "ERROR gate should show ❌")
        _require("ERROR" in report, "'ERROR' missing from report")

    def test_severity_counts_in_table(self):
        report = build_report("p", SAMPLE_ISSUES, 3, "OK",
                              "BLOCKER,CRITICAL,MAJOR", "BUG,VULNERABILITY,CODE_SMELL")
        _require("BLOCKER" in report, "'BLOCKER' missing from report")
        _require("CRITICAL" in report, "'CRITICAL' missing from report")
        _require("MAJOR" in report, "'MAJOR' missing from report")

    def test_top_issues_listed(self):
        report = build_report("p", SAMPLE_ISSUES, 3, "OK",
                              "BLOCKER,CRITICAL,MAJOR", "BUG,VULNERABILITY,CODE_SMELL")
        _require("gpio.c" in report, "'gpio.c' missing from report")
        _require("Null pointer dereference" in report, "Issue message missing from report")
        _require("c:S1035" in report, "Rule ID missing from report")

    def test_component_prefix_stripped(self):
        report = build_report("p", SAMPLE_ISSUES, 3, "OK",
                              "BLOCKER,CRITICAL,MAJOR", "BUG,VULNERABILITY,CODE_SMELL")
        # "myproject:" prefix should be stripped from component
        _require("myproject:" not in report, "'myproject:' prefix should be stripped")
        _require("c-lib/src/gpio.c" in report, "Stripped component path missing from report")

    def test_none_issues_graceful(self):
        report = build_report("p", None, 0, "UNKNOWN",
                              "BLOCKER,CRITICAL,MAJOR", "BUG,VULNERABILITY,CODE_SMELL")
        _require("nicht erreichbar" in report or "kein Report" in report,
                 "Expected fallback message for None issues")

    def test_empty_issues(self):
        report = build_report("p", [], 0, "OK",
                              "BLOCKER,CRITICAL,MAJOR", "BUG,VULNERABILITY,CODE_SMELL")
        _require("Keine Issues" in report or "✅" in report,
                 "Expected empty-issues indicator in report")

    def test_pipe_in_message_escaped(self):
        issues = [{
            "severity": "MAJOR",
            "type": "BUG",
            "rule": "r:1",
            "component": "p:file.c",
            "line": 1,
            "message": "foo | bar",
        }]
        report = build_report("p", issues, 1, "OK",
                              "MAJOR", "BUG")
        # Pipe in message must be escaped so Markdown table is valid
        _require("foo \\| bar" in report, "Pipe in message must be escaped as '\\|'")

    def test_top_50_limit(self):
        many_issues = [
            {
                "severity": "MAJOR",
                "type": "BUG",
                "rule": f"r:{i}",
                "component": f"p:file{i}.c",
                "line": i,
                "message": f"issue {i}",
            }
            for i in range(100)
        ]
        report = build_report("p", many_issues, 100, "OK",
                              "MAJOR", "BUG")
        _require("50 weitere Issues" in report, "Expected truncation notice for >50 issues")

    def test_output_file_written(self, tmp_path):
        outfile = tmp_path / "report.md"
        report = build_report("p", SAMPLE_ISSUES, 3, "OK",
                              "BLOCKER,CRITICAL,MAJOR", "BUG,VULNERABILITY,CODE_SMELL")
        outfile.write_text(report, encoding="utf-8")
        content = outfile.read_text(encoding="utf-8")
        _require("SonarQube Overview" in content, "Report file missing 'SonarQube Overview' header")


class TestSeverityEmoji:
    def test_all_severities_have_emoji(self):
        for sev in ["BLOCKER", "CRITICAL", "MAJOR", "MINOR", "INFO"]:
            if sev not in SEVERITY_EMOJI:
                raise KeyError(f"SEVERITY_EMOJI missing key: {sev!r}")
            if not SEVERITY_EMOJI[sev]:
                raise ValueError(f"SEVERITY_EMOJI[{sev!r}] is empty or falsy")


class TestTypeLabel:
    def test_all_types_have_label(self):
        for t in ["BUG", "VULNERABILITY", "CODE_SMELL"]:
            if t not in TYPE_LABEL:
                raise KeyError(f"TYPE_LABEL missing key: {t!r}")
            if not TYPE_LABEL[t]:
                raise ValueError(f"TYPE_LABEL[{t!r}] is empty or falsy")
