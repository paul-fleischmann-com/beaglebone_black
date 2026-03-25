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


class TestBuildReport:
    def test_contains_project_key(self):
        report = build_report("my-project", SAMPLE_ISSUES, 3, "OK",
                              "BLOCKER,CRITICAL,MAJOR", "BUG,VULNERABILITY,CODE_SMELL")
        assert "my-project" in report

    def test_quality_gate_ok(self):
        report = build_report("p", SAMPLE_ISSUES, 3, "OK",
                              "BLOCKER,CRITICAL,MAJOR", "BUG,VULNERABILITY,CODE_SMELL")
        assert "✅" in report
        assert "OK" in report

    def test_quality_gate_error(self):
        report = build_report("p", SAMPLE_ISSUES, 3, "ERROR",
                              "BLOCKER,CRITICAL,MAJOR", "BUG,VULNERABILITY,CODE_SMELL")
        assert "❌" in report
        assert "ERROR" in report

    def test_severity_counts_in_table(self):
        report = build_report("p", SAMPLE_ISSUES, 3, "OK",
                              "BLOCKER,CRITICAL,MAJOR", "BUG,VULNERABILITY,CODE_SMELL")
        assert "BLOCKER" in report
        assert "CRITICAL" in report
        assert "MAJOR" in report

    def test_top_issues_listed(self):
        report = build_report("p", SAMPLE_ISSUES, 3, "OK",
                              "BLOCKER,CRITICAL,MAJOR", "BUG,VULNERABILITY,CODE_SMELL")
        assert "gpio.c" in report
        assert "Null pointer dereference" in report
        assert "c:S1035" in report

    def test_component_prefix_stripped(self):
        report = build_report("p", SAMPLE_ISSUES, 3, "OK",
                              "BLOCKER,CRITICAL,MAJOR", "BUG,VULNERABILITY,CODE_SMELL")
        # "myproject:" prefix should be stripped from component
        assert "myproject:" not in report
        assert "c-lib/src/gpio.c" in report

    def test_none_issues_graceful(self):
        report = build_report("p", None, 0, "UNKNOWN",
                              "BLOCKER,CRITICAL,MAJOR", "BUG,VULNERABILITY,CODE_SMELL")
        assert "nicht erreichbar" in report or "kein Report" in report

    def test_empty_issues(self):
        report = build_report("p", [], 0, "OK",
                              "BLOCKER,CRITICAL,MAJOR", "BUG,VULNERABILITY,CODE_SMELL")
        assert "Keine Issues" in report or "✅" in report

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
        assert "foo \\| bar" in report

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
        assert "50 weitere Issues" in report

    def test_output_file_written(self, tmp_path):
        outfile = tmp_path / "report.md"
        report = build_report("p", SAMPLE_ISSUES, 3, "OK",
                              "BLOCKER,CRITICAL,MAJOR", "BUG,VULNERABILITY,CODE_SMELL")
        outfile.write_text(report, encoding="utf-8")
        content = outfile.read_text(encoding="utf-8")
        assert "SonarQube Overview" in content


class TestSeverityEmoji:
    def test_all_severities_have_emoji(self):
        for sev in ["BLOCKER", "CRITICAL", "MAJOR", "MINOR", "INFO"]:
            assert sev in SEVERITY_EMOJI
            assert SEVERITY_EMOJI[sev]


class TestTypeLabel:
    def test_all_types_have_label(self):
        for t in ["BUG", "VULNERABILITY", "CODE_SMELL"]:
            assert t in TYPE_LABEL
            assert TYPE_LABEL[t]
