"""
MACsec/MKA-Absicherung der ACF-CAN-Demo via mkad (siehe Issue #260). Baut auf
test_acfcan_demo.py auf (#259) — hier zusätzlich: Board und Viewer sprechen
über ein mkad-verschlüsseltes MACsec-Interface (macsec0) statt über das rohe
Ethernet-Interface.

Zwei Tests:
  1. Positiv: Mit laufendem mkad auf beiden Seiten kommt ein gesendetes
     CAN-Frame im Viewer an UND der Viewer meldet eine aktive MACsec-SA.
  2. Negativ: Ohne mkad (kein macsec0) kommt kein Frame über den
     MACsec-Pfad an — verifiziert, dass acf-can-listener tatsächlich vom
     MACsec-Interface abhängt statt (ungewollt) auf das rohe Interface
     zurückzufallen.

Deployment:
    # Board:
    scp project/macsec/mkad-board.conf debian@192.168.7.2:/app/mkad-board.conf
    ./scripts/setup_macsec_mka.sh &
    ACFCAN_DEMO_ETHIF=macsec0 ACFCAN_DEMO_DST_MAC=<Viewer-MAC> \
        ./scripts/setup_acfcan_vcan_demo.sh &

    # Viewer:
    docker run --network host --cap-add=NET_ADMIN \
        -e ACFCAN_VIEWER_ENABLE_MACSEC=1 acfcan-viewer

Ausfuehren:
    BEAGLE_HOST=192.168.7.2 VIEWER_HOST=192.168.7.50 \
        pytest tests/hardware/test_macsec_mka.py -v

Umgebungsvariablen: siehe test_acfcan_demo.py (BEAGLE_HOST, BEAGLE_USER,
VIEWER_HOST, ACFCAN_CANIF).
"""

import os
import subprocess
import time

import pytest
import requests

HOST = os.getenv("BEAGLE_HOST", "192.168.7.2")
USER = os.getenv("BEAGLE_USER", "debian")
VIEWER_HOST = os.getenv("VIEWER_HOST")
CAN_IF = os.getenv("ACFCAN_CANIF", "vcan0")

_SSH_BASE = ["ssh", "-o", "StrictHostKeyChecking=no", "-o", "BatchMode=yes",
             f"{USER}@{HOST}"]


def ssh(*args, check=False):
    result = subprocess.run(  # nosec B603 — HOST/USER sind Env-Konstanten; args hardcodiert
        _SSH_BASE + list(args),
        capture_output=True,
        text=True,
        timeout=15,
    )
    if check and result.returncode != 0:
        pytest.fail(
            f"ssh {' '.join(args)} fehlgeschlagen (RC={result.returncode}):\n"
            f"stdout: {result.stdout}\nstderr: {result.stderr}"
        )
    return result


@pytest.fixture(scope="module", autouse=True)
def viewer_verfuegbar():
    if not VIEWER_HOST:
        pytest.skip("VIEWER_HOST nicht gesetzt — kein acfcan-viewer-Endpunkt konfiguriert")
    try:
        r = requests.get(f"http://{VIEWER_HOST}:8080/health", timeout=5)
        r.raise_for_status()
    except Exception as exc:
        pytest.skip(f"acfcan-viewer unter {VIEWER_HOST}:8080 nicht erreichbar: {exc}")


def _frame_in_history(can_id: str, data: str, timeout: float) -> bool:
    deadline = time.time() + timeout
    while time.time() < deadline:
        resp = requests.get(f"http://{VIEWER_HOST}:8080/history", timeout=5)
        frames = resp.json().get("frames", [])
        if any(f["can_id"].upper() == can_id.upper() and f["data"].upper() == data.upper() for f in frames):
            return True
        time.sleep(0.5)
    return False


class TestMacsecActive:
    def test_macsec_sa_aktiv_und_frame_kommt_an(self):
        """Mit laufendem mkad: aktive SA im Viewer UND Frame kommt an."""
        status = requests.get(f"http://{VIEWER_HOST}:8080/macsec-status", timeout=5).json()
        if not status.get("active"):
            pytest.skip(f"Keine aktive MACsec-SA im Viewer ({status}) — mkad auf beiden Seiten prüfen")

        if ssh("test", "-e", f"/sys/class/net/{CAN_IF}").returncode != 0:
            pytest.skip(f"{CAN_IF} nicht auf {HOST} vorhanden — setup_acfcan_vcan_demo.sh laufen lassen")

        can_id, data = "654", "5EC0DE01"
        ssh("cansend", CAN_IF, f"{can_id}#{data}", check=True)

        if not _frame_in_history(can_id, data, timeout=10):
            pytest.fail(f"Frame {can_id}#{data} nicht über MACsec-Pfad im Viewer angekommen")


class TestMacsecInactive:
    def test_kein_frame_ohne_aktive_sa(self):
        """Ohne aktive MACsec-SA kommt kein Frame über den MACsec-Pfad an."""
        status = requests.get(f"http://{VIEWER_HOST}:8080/macsec-status", timeout=5).json()
        if status.get("active"):
            pytest.skip("MACsec-SA ist aktiv — dieser Negativ-Test braucht gestopptes mkad")

        can_id, data = "654", "DEAD0000"
        if ssh("test", "-e", f"/sys/class/net/{CAN_IF}").returncode == 0:
            ssh("cansend", CAN_IF, f"{can_id}#{data}")

        if _frame_in_history(can_id, data, timeout=5):
            pytest.fail("Frame ohne aktive MACsec-SA im Viewer angekommen — MACsec-Gate wirkungslos")
