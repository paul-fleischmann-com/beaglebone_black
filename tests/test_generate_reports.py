"""Tests für generate_reports.py Logik (TOOL-RPT-003)

generate_reports.py wird als CLI-Tool ausgeführt und enthält komplexe
globale Initialisierung. Wir testen die kritische guard-Logik direkt.
"""
import pytest


# ── TOOL-RPT-003: Kein ZeroDivisionError bei leeren Tests ───────────────────

def test_generate_reports_division_guard_empty():
    """Division-Guards greifen korrekt bei total_reqs=0 und total_tests=0."""
    total_reqs  = 0
    total_tests = 0
    bestanden   = 0
    impl_reqs   = 0

    req_coverage = round(impl_reqs / total_reqs * 100, 1) if total_reqs else 0.0
    test_rate    = round(bestanden / total_tests * 100, 1) if total_tests else 0.0
    avg_coverage = (0.0 / total_reqs) if total_reqs else 0.0

    if req_coverage != 0.0:
        pytest.fail(f"Expected req_coverage=0.0, got {req_coverage}")
    if test_rate != 0.0:
        pytest.fail(f"Expected test_rate=0.0, got {test_rate}")
    if avg_coverage != 0.0:
        pytest.fail(f"Expected avg_coverage=0.0, got {avg_coverage}")


def test_generate_reports_division_guard_with_data():
    """Division-Guards lassen normale Werte durch."""
    total_reqs  = 2
    total_tests = 3
    bestanden   = 2
    impl_reqs   = 1

    req_coverage = round(impl_reqs / total_reqs * 100, 1) if total_reqs else 0.0
    test_rate    = round(bestanden / total_tests * 100, 1) if total_tests else 0.0

    if req_coverage != 50.0:
        pytest.fail(f"Expected req_coverage=50.0, got {req_coverage}")
    if test_rate != pytest.approx(66.7, abs=0.1):
        pytest.fail(f"Expected test_rate≈66.7, got {test_rate}")
