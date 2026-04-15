# [SDOC_LINK: SWR-015]
# [SDOC_LINK: SWR-019]
"""
TUI Tests — prüft ob das TUI Binary korrekt gebaut wurde und die
benötigten REST API-Endpunkte (fetchBME280, setBackend) erreichbar sind.

Das TUI selbst ist ein interaktives Terminal-Programm (bubbletea) und
nicht headless testbar. Stattdessen werden:
  1. Binary-Existenz und Ausführbarkeit geprüft (Build-Check)
  2. Die vom TUI verwendeten API-Endpunkte direkt getestet

Voraussetzung:
    make cli        # baut bbtui-linux-amd64
    BEAGLE_HOST=192.168.7.2 pytest tests/tui/ -v
"""

import os
import socket

import pytest
import requests

TUI = os.getenv("BBTUI", "./bin/bbtui-linux-amd64")
HOST = os.getenv("BEAGLE_HOST", "192.168.7.2")
API = f"http://{HOST}:5000"


def _api_reachable() -> bool:
    try:
        with socket.create_connection((HOST, 5000), timeout=2):
            return True
    except OSError:
        return False



class TestTuiBinary:
    """Build-Check: TUI Binary muss nach 'make cli' vorhanden sein."""

    def test_binary_exists(self):
        """TUI Binary muss nach dem Build vorhanden sein."""
        assert os.path.isfile(TUI), f"TUI Binary nicht gefunden: {TUI}"

    def test_binary_executable(self):
        """TUI Binary muss ausführbar sein."""
        assert os.access(TUI, os.X_OK), f"TUI Binary nicht ausführbar: {TUI}"


@pytest.mark.skipif(not _api_reachable(), reason="BeagleBone API nicht erreichbar — BEAGLE_HOST setzen")
class TestTuiApiEndpoints:
    """
    Prüft die API-Endpunkte die das TUI intern aufruft (fetchBME280, setBackend).
    Entspricht dem Integration-Test für SWR-015.
    """

    def test_bme280_endpunkt_liefert_alle_felder(self):
        """TUI fetchBME280() erwartet temperature, humidity, pressure, altitude."""
        r = requests.get(f"{API}/api/v1/bme280", timeout=5)
        assert r.status_code == 200
        d = r.json()
        for field in ("temperature", "humidity", "pressure", "altitude"):
            assert field in d, f"Feld '{field}' fehlt in BME280-Antwort"

    def test_bme280_werte_in_physikalischen_grenzen(self):
        """BME280-Werte müssen physikalisch plausibel sein."""
        r = requests.get(f"{API}/api/v1/bme280", timeout=5)
        d = r.json()
        assert -40  <= d["temperature"] <= 85
        assert   0  <= d["humidity"]    <= 100
        assert 300  <= d["pressure"]    <= 1100

    def test_backend_endpunkt_erreichbar(self):
        """TUI setBackendCmd() setzt Backend via POST /api/v1/backend."""
        r = requests.post(f"{API}/api/v1/backend", json={"backend": "auto"}, timeout=5)
        assert r.status_code == 200

    def test_gpio_read_endpunkt(self):
        """TUI GPIO-Tab liest Pin via GET /api/v1/gpio/{pin} (SWR-019)."""
        r = requests.get(f"{API}/api/v1/gpio/60", timeout=5)
        assert r.status_code == 200
        d = r.json()
        assert "pin" in d and "value" in d

    def test_gpio_write_endpunkt(self):
        """TUI GPIO-Tab setzt Pin via POST /api/v1/gpio/{pin} (SWR-019)."""
        r = requests.post(f"{API}/api/v1/gpio/60", json={"value": 0}, timeout=5)
        assert r.status_code == 200
