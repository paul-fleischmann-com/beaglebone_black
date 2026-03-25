#!/usr/bin/env python3
"""collect_results.py — Liest echte Testergebnisse und schreibt test_results.json.

Aufruf (Drone CI):
    python3 scripts/collect_results.py \\
        --workspace /workspace \\
        --requirements reports/requirements.json \\
        --output /workspace/test_results.json

Aufruf (lokal via report.sh):
    python3 scripts/collect_results.py \\
        --workspace reports/ \\
        --requirements reports/requirements.json \\
        --output reports/test_results.json

Ausgabe: test_results.json mit nur {"test_ergebnisse": [...]}
generate_reports.py liest requirements.json + test_results.json getrennt.

Eingabe-Dateien im workspace:
    go-tests.json       go test -json (newline-delimited JSON)
    pytest-api.json     pytest --json-report
    pytest-cli.json     pytest --json-report
    pytest-hardware.json pytest --json-report  (optional)

Die requirements.json enthält logische Test-Namen wie test_bme280_endpoint.
Echte Tests heissen test_bme280 (Python) oder TestBME280Read_Erfolg (Go).
Dieses Script mappt beides aufeinander und aktualisiert test_ergebnisse.
"""
import argparse
import json
import os
import sys

# ── Mapping: logischer Req-Testname → (suite, echter Funktionsname) ──────────
# suite: "go" | "python" | None (noch kein Test implementiert)
NAME_MAP = {
    # EMB — Go HAL Tests
    "test_bme280_init":            ("go", "TestBME280Read_Erfolg"),
    "test_bme280_read":            ("go", "TestBME280Read_Erfolg"),
    "test_temperatur_plausibel":   ("go", "TestBME280Read_Erfolg"),
    "test_luftfeuchte_plausibel":  ("go", "TestBME280Read_Erfolg"),
    "test_luftdruck_plausibel":    ("go", "TestBME280Read_Erfolg"),
    "test_hoehe_plausibel":        ("go", "TestBME280Read_Erfolg"),
    "test_hoehe_berechnung":       ("go", "TestBME280Read_Erfolg"),
    "test_gpio_export":            ("go", "TestGPIO_SchreibenLesen"),
    "test_gpio_write":             ("go", "TestGPIO_SchreibenLesen"),
    "test_gpio_read":              ("go", "TestGPIO_SchreibenLesen"),
    "test_gpio_direction":         ("go", "TestGPIO_SetDirection"),
    "test_gpio_mehrere_pins":      ("go", "TestGPIO_Tabelle"),
    "test_uart_open":              ("go", "TestUART_SendEmpfangen"),
    "test_uart_write":             ("go", "TestUART_SendEmpfangen"),
    "test_uart_read":              ("go", "TestUART_SendEmpfangen"),
    "test_uart_baudrate":          ("go", "TestUART_SendEmpfangen"),
    "test_spi_transfer":           ("go", "TestSPI_Loopback"),
    "test_spi_loopback":           ("go", "TestSPI_Loopback"),
    "test_spi_mode":               ("go", "TestSPI_Loopback"),
    "test_spi_open":               ("go", "TestSPI_Loopback"),
    "test_simulation_armv7":       ("go", "TestInterface_Compliance"),
    "test_deploy_beaglebone":      ("go", "TestInterface_Compliance"),
    # HAL — Go HAL Tests
    "test_hal_c_init":             ("go", "TestInterface_Compliance"),
    "test_hal_c_bme280":           ("go", "TestBME280Read_Erfolg"),
    "test_hal_c_gpio":             ("go", "TestGPIO_SchreibenLesen"),
    "test_hal_rust_init":          ("go", "TestInterface_Compliance"),
    "test_hal_rust_bme280":        ("go", "TestBME280Read_Erfolg"),
    "test_hal_rust_gpio":          ("go", "TestGPIO_SchreibenLesen"),
    "test_backend_wechsel":        ("go", "TestDriver_Backend"),
    "test_backend_c_zu_rust":      ("go", "TestDriver_Backend"),
    "test_backend_env_var":        ("go", "TestLoadConfig_EnvOverride"),
    "test_fallback_primaer_fehler":("go", "TestFallback_PrimaerFehler"),
    "test_fallback_beide_fehlen":  ("go", "TestFallback_PrimaerFehler"),
    "test_fallback_auto":          ("go", "TestFallback_PrimaerFehler"),
    "test_mock_init":              ("go", "TestMock_Reset"),
    "test_mock_bme280":            ("go", "TestBME280Read_Erfolg"),
    "test_mock_fehler_injektion":  ("go", "TestBME280Read_Fehler"),
    "test_mock_call_tracking":     ("go", "TestMock_Reset"),
    "test_hal_race_condition":     ("go", "TestGPIO_SchreibenLesen"),
    "test_concurrent_gpio":        ("go", "TestGPIO_SchreibenLesen"),
    "test_concurrent_bme280":      ("go", "TestBME280Read_Erfolg"),
    "test_hal_i2c_fehler":         ("go", "TestBME280Read_Fehler"),
    "test_hal_gpio_fehler":        ("go", "TestGPIO_SchreibenLesen"),
    "test_hal_uart_fehler":        ("go", "TestUART_Close"),
    # API — Python API Tests (tests/api/test_api.py)
    "test_bme280_endpoint":        ("python", "test_bme280"),
    "test_bme280_json_struktur":   ("python", "test_bme280"),
    "test_bme280_backend_angabe":  ("python", "test_bme280"),
    "test_gpio_get":               ("python", "test_gpio_read"),
    "test_gpio_post":              ("python", "test_gpio_write"),
    "test_gpio_invalid_pin":       ("python", "test_gpio_write"),
    "test_backend_endpoint":       ("python", "test_backend_get"),
    "test_backend_wechsel_api":    ("python", "test_backend_wechsel"),
    "test_backend_invalid":        ("python", "test_backend_invalid"),
    "test_health_endpoint":        ("python", "test_health"),
    "test_health_felder":          ("python", "test_health"),
    # CORS — Go Tests (pkg/api)
    "test_cors_options_preflight": ("go", "TestCORSMiddleware_OptionsReturns200"),
    "test_cors_headers":           ("go", "TestCORSMiddleware_SetsHeaders"),
    # SSE / UART / SPI API — noch keine Python-Tests implementiert
    "test_uart_send":              None,
    "test_uart_receive":           None,
    "test_uart_config":            None,
    "test_spi_transfer_endpoint":  None,
    "test_spi_response_format":    None,
    "test_sse_bme280":             None,
    "test_sse_verbindung":         None,
    "test_sse_format":             None,
    # CLI — Python CLI Tests (tests/cli/test_cli.py)
    "test_cli_help":               ("python", "test_help"),
    "test_cli_version":            ("python", "test_version"),
    "test_cli_befehle":            ("python", "test_status"),
    "test_bme280_read_cmd":        ("python", "test_bme280"),
    "test_bme280_config_cmd":      ("python", "test_bme280"),
    "test_gpio_read_cmd":          ("python", "test_gpio_read"),
    "test_gpio_write_cmd":         ("python", "test_gpio_write"),
    "test_gpio_config_cmd":        ("python", "test_gpio_read"),
    "test_uart_send_cmd":          None,
    "test_uart_receive_cmd":       None,
    "test_completion_bash":        ("python", "test_completion_bash"),
    "test_completion_zsh":         ("python", "test_completion_zsh"),
    "test_completion_fish":        None,
    "test_config_init":            ("python", "test_config_init"),
    "test_config_laden":           ("python", "test_config_laden"),
    "test_config_set":             ("python", "test_config_set"),
    "test_config_profile":         ("python", "test_config_profile"),
    "test_build_linux_amd64":      None,
    "test_build_armv7":            None,
    "test_build_darwin":           None,
    "test_build_windows":          None,
    "test_installer_syntax":       ("python", "test_installer_syntax"),
    "test_installer_completion":   None,
    # GUI — Python Web/Desktop/TUI Tests
    "test_web_gui_html":           ("python", "test_web_gui_html"),
    "test_web_gui_bme280":         ("python", "test_web_gui_bme280"),
    "test_web_gui_gpio":           ("python", "test_web_gui_gpio"),
    "test_desktop_gui_build":      ("python", "test_desktop_gui_build"),
    "test_desktop_tabs":           None,
    "test_tui_build":              ("python", "test_tui_build"),
    "test_tui_navigation":         None,
    "test_gui_refresh":            ("python", "test_gui_refresh"),
    "test_sse_stream_gui":         None,
    "test_gui_backend_wechsel":    ("python", "test_gui_backend_wechsel"),
    "test_gui_backend_anzeige":    None,
    "test_gui_dark_theme":         ("python", "test_gui_dark_theme"),
}

# Status-Übersetzung: pytest/go → requirements.json
_PY_STATUS = {
    "passed":  "BESTANDEN",
    "failed":  "FEHLGESCHLAGEN",
    "skipped": "ÜBERSPRUNGEN",
    "error":   "FEHLGESCHLAGEN",
}
_GO_STATUS = {
    "pass": "BESTANDEN",
    "fail": "FEHLGESCHLAGEN",
    "skip": "ÜBERSPRUNGEN",
}


def load_go_results(workspace: str) -> dict:
    """Liest go test -json Output und gibt {TestName: {status, dauer_ms}} zurück."""
    path = os.path.join(workspace, "go-tests.json")
    if not os.path.exists(path):
        return {}
    results = {}
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue
            action = entry.get("Action", "")
            test   = entry.get("Test", "")
            if not test or action not in _GO_STATUS:
                continue
            elapsed_ms = int(entry.get("Elapsed", 0) * 1000)
            results[test] = {
                "status":   _GO_STATUS[action],
                "dauer_ms": elapsed_ms,
            }
    return results


def load_pytest_results(workspace: str) -> dict:
    """Liest alle pytest-json-report Dateien und gibt {test_func_name: {status, dauer_ms}} zurück."""
    files = [
        os.path.join(workspace, "pytest-api.json"),
        os.path.join(workspace, "pytest-cli.json"),
        os.path.join(workspace, "pytest-hardware.json"),
        # Drone CI names
        os.path.join(workspace, "api_tests.json"),
        os.path.join(workspace, "cli_tests.json"),
        os.path.join(workspace, "hw_tests.json"),
    ]
    results = {}
    for path in files:
        if not os.path.exists(path):
            continue
        try:
            data = json.load(open(path))
        except Exception:
            continue
        for t in data.get("tests", []):
            func_name = t["nodeid"].split("::")[-1]
            outcome   = t.get("outcome", "")
            dur_s     = t.get("call", {}).get("duration", 0) or 0
            results[func_name] = {
                "status":   _PY_STATUS.get(outcome, "ÜBERSPRUNGEN"),
                "dauer_ms": int(dur_s * 1000),
            }
    return results


def resolve_result(req_name: str, go: dict, python: dict) -> dict | None:
    """Gibt das Testergebnis für einen Requirements-Testnamen zurück, oder None."""
    # 1. Exakter Name-Match (falls req_name == echter Testname)
    if req_name in go:
        r = go[req_name]
        return {"name": req_name, "status": r["status"],
                "dauer_ms": r["dauer_ms"], "komponente": "HAL"}
    if req_name in python:
        r = python[req_name]
        return {"name": req_name, "status": r["status"],
                "dauer_ms": r["dauer_ms"], "komponente": ""}

    # 2. Mapping-Lookup
    mapping = NAME_MAP.get(req_name)
    if mapping is None:
        return None  # kein Test implementiert → ❓

    suite, actual_name = mapping
    if suite == "go" and actual_name in go:
        r = go[actual_name]
        return {"name": req_name, "status": r["status"],
                "dauer_ms": r["dauer_ms"], "komponente": ""}
    if suite == "python" and actual_name in python:
        r = python[actual_name]
        return {"name": req_name, "status": r["status"],
                "dauer_ms": r["dauer_ms"], "komponente": ""}

    return None  # Mapping vorhanden, aber Test nicht gelaufen → ❓


def collect(workspace: str, requirements_path: str, output_path: str) -> None:
    # Test-Ergebnisse laden
    go_results     = load_go_results(workspace)
    python_results = load_pytest_results(workspace)

    print(f"📥 Go-Tests geladen:     {len(go_results)} Ergebnisse")
    print(f"📥 Python-Tests geladen: {len(python_results)} Ergebnisse")

    # Requirements laden
    with open(requirements_path) as f:
        data = json.load(f)

    # Alle Test-Namen sammeln die in Requirements referenziert werden
    all_req_tests: set[str] = set()
    kat_by_test: dict[str, str] = {}
    for kat in data["kategorien"]:
        for req in kat["requirements"]:
            for t in req["tests"]:
                all_req_tests.add(t)
                kat_by_test[t] = kat["id"]

    # test_ergebnisse neu aufbauen
    new_ergebnisse = []
    found = not_found = 0

    for req_name in sorted(all_req_tests):
        result = resolve_result(req_name, go_results, python_results)
        if result is not None:
            if not result["komponente"]:
                result["komponente"] = kat_by_test.get(req_name, "")
            new_ergebnisse.append(result)
            found += 1
        else:
            not_found += 1

    print(f"✅ Zugeordnet:           {found}/{len(all_req_tests)} Tests")
    if not_found:
        # Zeige welche Tests kein Ergebnis haben
        missing = sorted(
            t for t in all_req_tests
            if resolve_result(t, go_results, python_results) is None
        )
        print(f"❓ Ohne Ergebnis:        {not_found} Tests (kein Test implementiert)")
        for m in missing:
            mapping = NAME_MAP.get(m)
            reason = "kein Mapping" if m not in NAME_MAP else "Test nicht gelaufen"
            print(f"   - {m}  ({reason})")

    # Sortierung: nach Komponente dann Name
    kat_order = {k["id"]: i for i, k in enumerate(data["kategorien"])}
    new_ergebnisse.sort(key=lambda t: (
        kat_order.get(t["komponente"], 99), t["name"]
    ))

    # Nur test_results.json schreiben (dynamischer Teil)
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump({"test_ergebnisse": new_ergebnisse}, f, ensure_ascii=False, indent=2)
    print(f"✅ Output: {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Sammelt echte Testergebnisse und aktualisiert requirements.json")
    parser.add_argument("--workspace",    required=True,
                        help="Verzeichnis mit Test-JSON-Dateien")
    parser.add_argument("--requirements", required=True,
                        help="Pfad zur requirements.json (Input)")
    parser.add_argument("--output",       required=True,
                        help="Pfad zur test_results.json (Output, nur test_ergebnisse)")
    parser.add_argument("--meta",         default=None,
                        help="Pfad zur build_meta.json (optional, wird ignoriert)")
    args = parser.parse_args()

    if not os.path.exists(args.requirements):
        print(f"❌ requirements.json nicht gefunden: {args.requirements}",
              file=sys.stderr)
        sys.exit(1)

    collect(args.workspace, args.requirements, args.output)


if __name__ == "__main__":
    main()
