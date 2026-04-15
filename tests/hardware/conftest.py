import os
import pytest
import requests

HOST = os.getenv("BEAGLE_HOST", "192.168.7.2")
API  = f"http://{HOST}:5000"


def _api_reachable() -> tuple[bool, str]:
    """Prüft nur ob das Board erreichbar ist — unabhängig vom aktiven Backend."""
    try:
        r = requests.get(f"{API}/health", timeout=5)
        if r.status_code == 200:
            return True, ""
        return False, f"Health-Endpoint HTTP {r.status_code}"
    except Exception as exc:
        return False, str(exc)


def pytest_collection_modifyitems(config, items):
    ok, reason = _api_reachable()
    if not ok:
        skip = pytest.mark.skip(reason=f"BeagleBone nicht erreichbar: {reason}")
        for item in items:
            item.add_marker(skip)
