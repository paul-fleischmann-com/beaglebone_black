import os
import pytest
import requests

HOST = os.getenv("BEAGLE_HOST", "192.168.7.2")
API  = f"http://{HOST}:5000"


def _hardware_available() -> tuple[bool, str]:
    try:
        r = requests.get(f"{API}/api/v1/bme280", timeout=5)
        if r.status_code == 200:
            return True, ""
        body = r.json() if r.headers.get("content-type", "").startswith("application/json") else {}
        return False, body.get("error", f"HTTP {r.status_code}")
    except Exception as exc:
        return False, str(exc)


def pytest_collection_modifyitems(config, items):
    ok, reason = _hardware_available()
    if not ok:
        skip = pytest.mark.skip(reason=f"Hardware nicht verfügbar: {reason}")
        for item in items:
            item.add_marker(skip)
