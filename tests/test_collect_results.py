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

    if results["TestFoo"]["status"] != "BESTANDEN":
        pytest.fail(f"TestFoo: expected BESTANDEN, got {results['TestFoo']['status']!r}")
    if results["TestBar"]["status"] != "FEHLGESCHLAGEN":
        pytest.fail(f"TestBar: expected FEHLGESCHLAGEN, got {results['TestBar']['status']!r}")
    if results["TestBaz"]["status"] != "ÜBERSPRUNGEN":
        pytest.fail(f"TestBaz: expected ÜBERSPRUNGEN, got {results['TestBaz']['status']!r}")
    if len(results) != 3:
        pytest.fail(f"Expected 3 results, got {len(results)}")


def test_collect_go_results_missing_file():
    """Fehlende go-tests.json liefert leeres Dict."""
    with tempfile.TemporaryDirectory() as tmp:
        results = cr.load_go_results(tmp)
    if results != {}:
        pytest.fail(f"Expected empty dict for missing file, got {results!r}")


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

    if results["test_health"]["status"] != "BESTANDEN":
        pytest.fail(f"test_health: expected BESTANDEN, got {results['test_health']['status']!r}")
    if results["test_broken"]["status"] != "FEHLGESCHLAGEN":
        pytest.fail(f"test_broken: expected FEHLGESCHLAGEN, got {results['test_broken']['status']!r}")
    if results["test_skip"]["status"] != "ÜBERSPRUNGEN":
        pytest.fail(f"test_skip: expected ÜBERSPRUNGEN, got {results['test_skip']['status']!r}")


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

    if "test_ergebnisse" not in data:
        pytest.fail("Key 'test_ergebnisse' missing from output")
    if not isinstance(data["test_ergebnisse"], list):
        pytest.fail(f"Expected list for 'test_ergebnisse', got {type(data['test_ergebnisse']).__name__}")
    if not any(e["name"] == "TestFoo" for e in data["test_ergebnisse"]):
        pytest.fail("Expected entry with name='TestFoo' in test_ergebnisse")
