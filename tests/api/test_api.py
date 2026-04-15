# [SDOC_LINK: SWR-015]
# [SDOC_LINK: SWR-016]
# [SDOC_LINK: SWR-017]
import requests, os, pytest

HOST = os.getenv("BEAGLE_HOST","192.168.7.2")
API  = f"http://{HOST}:5000"

def test_health():
    r = requests.get(f"{API}/health", timeout=5)
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

def test_bme280():
    r = requests.get(f"{API}/api/v1/bme280", timeout=5)
    assert r.status_code == 200
    d = r.json()
    assert -40 <= d["temperature"] <= 85
    assert   0 <= d["humidity"]    <= 100
    assert 300 <= d["pressure"]    <= 1100
    assert -500<= d["altitude"]    <= 9000

def test_gpio_read():
    r = requests.get(f"{API}/api/v1/gpio/60", timeout=5)
    assert r.status_code == 200
    d = r.json()
    assert "pin"   in d
    assert "value" in d

def test_gpio_write():
    r = requests.post(f"{API}/api/v1/gpio/60",
        json={"value":1}, timeout=5)
    assert r.status_code == 200

def test_backend_wechsel():
    for backend in ["c","rust","auto"]:
        r = requests.post(f"{API}/api/v1/backend",
            json={"backend":backend}, timeout=5)
        assert r.status_code == 200
