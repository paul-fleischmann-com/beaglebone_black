"""
PRU1-RPMsg-GPIO-Backend (siehe Issue #252). Nur auf echter Hardware sinnvoll
testbar — remoteproc/rpmsg/PRU-Timing lassen sich nicht mocken (siehe
docs/features/plans/252-...-echtzeit-hardwarezugriff.md, "Bekannte
Einschränkungen"). BEAGLE_HOST-gated über conftest.py.

Wichtig: "pin" bezeichnet hier das PRU-Bit (0-15, R30/R31), NICHT die
Linux-Sysfs-GPIO-Nummer der c/rust-Backends.
"""
import os

import pytest
import requests

HOST = os.getenv("BEAGLE_HOST", "192.168.7.2")
API = f"http://{HOST}:5000"


@pytest.fixture(autouse=True)
def set_pru_backend():
    requests.post(f"{API}/api/v1/backend", json={"backend": "pru"})


class TestPRUGpio:
    def test_set_high(self):
        r = requests.post(f"{API}/api/v1/gpio/0", json={"value": 1})
        assert r.status_code == 200

    def test_set_low(self):
        r = requests.post(f"{API}/api/v1/gpio/0", json={"value": 0})
        assert r.status_code == 200

    def test_backend_label(self):
        d = requests.get(f"{API}/api/v1/gpio/0").json()
        assert d["backend"] == "pru"

    def test_pin_out_of_range_rejected(self):
        r = requests.post(f"{API}/api/v1/gpio/99", json={"value": 1})
        assert r.status_code >= 400


class TestPRUUnsupported:
    """BME280/UART/SPI laufen auf dem PRU-Backend absichtlich nicht."""

    def test_bme280_not_supported(self):
        r = requests.get(f"{API}/api/v1/bme280")
        assert r.status_code >= 400
