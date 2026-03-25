"""Tests für collect_results.py (TOOL-COL-001, TOOL-COL-002, TOOL-COL-003)"""
import json
import os
import sys
import tempfile

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import collect_results as cr


# ── TOOL-COL-001: Go-Ergebnisse einlesen ────────────────────────────────────

def test_collect_go_results():
    """pass/fail/skip korrekt auf BESTANDEN/FEHLGESCHLAGEN/ÜBERSPRUNGEN gemappt."""
    with tempfile.TemporaryDirectory() as tmp:
        lines = (
            '{"Action":"pass","Test":"TestFoo","Elapsed":0.01}\n'
            '{"Action":"fail","Test":"TestBar","Elapsed":0.02}\n'
            '{"Action":"skip","Test":"TestBaz","Elapsed":0.0}\n'
            '{"Action":"pass","Package":"pkg/hal"}\n'  # kein Test-Feld → ignoriert
        )
        with open(os.path.join(tmp, "go-tests.json"), "w") as f:
            f.write(lines)
        results = cr.load_go_results(tmp)

    assert results["TestFoo"]["status"] == "BESTANDEN"
    assert results["TestBar"]["status"] == "FEHLGESCHLAGEN"
    assert results["TestBaz"]["status"] == "ÜBERSPRUNGEN"
    assert len(results) == 3


def test_collect_go_results_missing_file():
    """Fehlende go-tests.json liefert leeres Dict."""
    with tempfile.TemporaryDirectory() as tmp:
        results = cr.load_go_results(tmp)
    assert results == {}


# ── TOOL-COL-002: pytest-Ergebnisse einlesen ────────────────────────────────

def test_collect_pytest_results():
    """passed/failed/skipped korrekt gemappt."""
    with tempfile.TemporaryDirectory() as tmp:
        report = {
            "tests": [
                {"nodeid": "tests/test_api.py::test_health",  "outcome": "passed",  "call": {"duration": 0.05}},
                {"nodeid": "tests/test_api.py::test_broken",  "outcome": "failed",  "call": {"duration": 0.10}},
                {"nodeid": "tests/test_api.py::test_skip",    "outcome": "skipped", "call": {"duration": 0.0}},
            ]
        }
        with open(os.path.join(tmp, "pytest-api.json"), "w") as f:
            json.dump(report, f)
        results = cr.load_pytest_results(tmp)

    assert results["test_health"]["status"] == "BESTANDEN"
    assert results["test_broken"]["status"] == "FEHLGESCHLAGEN"
    assert results["test_skip"]["status"]   == "ÜBERSPRUNGEN"


# ── TOOL-COL-003: Ausgabe-Format ────────────────────────────────────────────

def test_collect_output_format():
    """collect() schreibt {test_ergebnisse: [...]} in output_path."""
    with tempfile.TemporaryDirectory() as tmp:
        # go-tests.json schreiben
        with open(os.path.join(tmp, "go-tests.json"), "w") as f:
            f.write('{"Action":"pass","Test":"TestFoo","Elapsed":0.01}\n')
        # minimale requirements.json
        req = {
            "kategorien": [{
                "id": "TEST",
                "requirements": [{"id": "T-001", "tests": ["TestFoo"]}]
            }]
        }
        req_path = os.path.join(tmp, "requirements.json")
        out_path = os.path.join(tmp, "test_results.json")
        with open(req_path, "w") as f:
            json.dump(req, f)

        cr.collect(workspace=tmp, requirements_path=req_path, output_path=out_path)

        with open(out_path) as f:
            data = json.load(f)

    assert "test_ergebnisse" in data
    assert isinstance(data["test_ergebnisse"], list)
    assert any(e["name"] == "TestFoo" for e in data["test_ergebnisse"])
