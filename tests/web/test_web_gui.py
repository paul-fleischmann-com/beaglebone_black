# [SDOC_LINK: SWR-017]
"""
Web GUI Tests — statische Analyse der index.html.

Prüft ohne Browser oder Server ob die Web App alle geforderten
Funktionen und HTML-Elemente enthält (SWR-017).

Kein Netzwerk oder BeagleBone notwendig.

Ausführen:
    pytest tests/web/ -v
"""

import os
import re

import pytest

HTML_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..", "tools", "web-gui", "index.html"
)


@pytest.fixture(scope="module")
def html() -> str:
    with open(HTML_PATH, encoding="utf-8") as f:
        return f.read()


class TestWebGuiStruktur:
    """HTML-Struktur: Alle Anzeigeelemente müssen vorhanden sein."""

    def test_html_datei_vorhanden(self):
        """tools/web-gui/index.html muss existieren."""
        assert os.path.isfile(HTML_PATH)

    def test_bme280_temperatur_element(self, html):
        """HTML muss Element mit id='temp' für Temperaturanzeige enthalten."""
        assert 'id="temp"' in html

    def test_bme280_luftfeuchtigkeit_element(self, html):
        """HTML muss Element mit id='hum' für Luftfeuchtigkeitsanzeige enthalten."""
        assert 'id="hum"' in html

    def test_bme280_luftdruck_element(self, html):
        """HTML muss Element mit id='press' für Luftdruckanzeige enthalten."""
        assert 'id="press"' in html

    def test_bme280_hoehe_element(self, html):
        """HTML muss Element mit id='alt' für Höhenanzeige enthalten."""
        assert 'id="alt"' in html

    def test_gpio_high_button(self, html):
        """HTML muss Button für GPIO HIGH (setGPIO(1)) enthalten."""
        assert "setGPIO(1)" in html

    def test_gpio_low_button(self, html):
        """HTML muss Button für GPIO LOW (setGPIO(0)) enthalten."""
        assert "setGPIO(0)" in html


class TestWebGuiJavaScript:
    """JavaScript-Funktionen: Kernfunktionen müssen implementiert sein."""

    def test_fetchbme280_funktion_vorhanden(self, html):
        """fetchBME280() muss als async function implementiert sein (SWR-017)."""
        assert "async function fetchBME280" in html

    def test_setgpio_funktion_vorhanden(self, html):
        """setGPIO() muss implementiert sein für GPIO-Steuerung."""
        assert "async function setGPIO" in html

    def test_setbackend_funktion_vorhanden(self, html):
        """setBackend() muss implementiert sein für Backend-Wechsel."""
        assert "async function setBackend" in html

    def test_api_host_konfigurierbar_via_url_parameter(self, html):
        """?host= URL-Parameter muss ausgewertet werden (SWR-017)."""
        assert "URLSearchParams" in html
        assert "params.get('host')" in html

    def test_automatisches_polling_vorhanden(self, html):
        """BME280-Daten müssen automatisch abgerufen werden (setInterval)."""
        assert "setInterval" in html
        assert "fetchBME280" in html

    def test_api_endpunkt_bme280_aufgerufen(self, html):
        """fetchBME280 muss /api/v1/bme280 aufrufen."""
        assert "/api/v1/bme280" in html

    def test_api_endpunkt_gpio_aufgerufen(self, html):
        """setGPIO muss /api/v1/gpio/ aufrufen."""
        assert "/api/v1/gpio/" in html
