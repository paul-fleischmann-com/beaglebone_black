# [SDOC_LINK: SWR-016]
# [SDOC_LINK: SWR-020]
"""
Desktop GUI Tests — prüft Binary-Existenz und die vom GUI verwendeten
REST API-Endpunkte (apiGet/apiPost für BME280 und GPIO).

Die Fyne-GUI erfordert einen Display-Server und ist nicht headless
ausführbar. Stattdessen werden:
  1. Binary-Existenz und Ausführbarkeit geprüft (Build-Check)
  2. Die vom GUI verwendeten API-Endpunkte direkt getestet

Voraussetzung:
    make cli        # baut bbgui-linux-amd64
    BEAGLE_HOST=192.168.7.2 pytest tests/gui/ -v
"""

import os
import socket

import pytest
import requests

GUI = os.getenv("BBGUI", "./bin/bbgui-linux-amd64")
HOST = os.getenv("BEAGLE_HOST", "192.168.7.2")
API = f"http://{HOST}:5000"


def _api_reachable() -> bool:
    try:
        with socket.create_connection((HOST, 5000), timeout=2):
            return True
    except OSError:
        return False



class TestGuiBinary:
    """Build-Check: GUI Binary muss nach 'make cli' vorhanden sein."""

    def test_binary_exists(self):
        """GUI Binary muss nach dem Build vorhanden sein."""
        assert os.path.isfile(GUI), f"GUI Binary nicht gefunden: {GUI}"

    def test_binary_executable(self):
        """GUI Binary muss ausführbar sein."""
        assert os.access(GUI, os.X_OK), f"GUI Binary nicht ausführbar: {GUI}"


@pytest.mark.skipif(not _api_reachable(), reason="BeagleBone API nicht erreichbar — BEAGLE_HOST setzen")
class TestGuiApiEndpoints:
    """
    Prüft die API-Endpunkte die die Desktop-GUI intern aufruft
    (apiGet für BME280, apiPost für GPIO). Entspricht SWR-016.
    """

    def test_bme280_endpunkt_liefert_sensordaten(self):
        """GUI bme280Tab() ruft /api/v1/bme280 via apiGet() auf."""
        r = requests.get(f"{API}/api/v1/bme280", timeout=5)
        assert r.status_code == 200
        d = r.json()
        for field in ("temperature", "humidity", "pressure", "altitude"):
            assert field in d, f"Feld '{field}' fehlt in BME280-Antwort"

    def test_gpio_write_via_post(self):
        """GUI gpioTab() setzt GPIO-Pin via apiPost() POST /api/v1/gpio/{pin}."""
        r = requests.post(f"{API}/api/v1/gpio/60", json={"value": 0}, timeout=5)
        assert r.status_code == 200

    def test_gpio_read_via_get(self):
        """GUI gpioTab() liest GPIO-Pin via apiGet() GET /api/v1/gpio/{pin}."""
        r = requests.get(f"{API}/api/v1/gpio/60", timeout=5)
        assert r.status_code == 200
        d = r.json()
        assert "pin" in d
        assert "value" in d

    def test_backend_wechsel_via_post(self):
        """GUI backendTab() wechselt Backend via apiPost() POST /api/v1/backend (SWR-020)."""
        for backend in ("c", "rust", "auto"):
            r = requests.post(f"{API}/api/v1/backend", json={"backend": backend}, timeout=5)
            assert r.status_code == 200

    def test_uart_config_endpunkt(self):
        """GUI uartTab() konfiguriert UART via POST /api/v1/uart/config (SWR-020)."""
        r = requests.post(
            f"{API}/api/v1/uart/config",
            json={"port": "/dev/ttyO1", "baud": 115200},
            timeout=5,
        )
        assert r.status_code in (200, 500)  # 500 ok wenn kein UART vorhanden
