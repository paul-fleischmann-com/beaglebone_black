"""
End-to-End-Test für die vcan→Eth→Container-Demo (siehe Issue #259):
BeagleBone Black (vcan0 → acf-can-talker) → Ethernet → acfcan-viewer-Container
(acf-can-listener → vcan1 → Web-Dashboard). Prüft, dass ein auf dem Board
gesendetes CAN-Frame tatsächlich im Viewer ankommt (per /history-Endpoint,
siehe tools/acfcan-viewer/app.py).

Getrennt von test_acfcan.py/test_acfcan_userspace.py: dort testet nur das
Board sich selbst (Ein-Board-veth-Loopback, siehe #256/#257 — kein zweites
Board vorhanden). Dieser Test braucht zusätzlich einen erreichbaren
acfcan-viewer-Container (VIEWER_HOST), daher separat und eigenständig
skippable, falls kein Viewer läuft.

Deployment:
    # Board:
    make open1722-userspace && make deploy
    ACFCAN_DEMO_DST_MAC=<Viewer-MAC> ./scripts/setup_acfcan_vcan_demo.sh &

    # Viewer (auf einem beliebigen Host im selben Netz):
    cd tools/acfcan-viewer
    docker build -t acfcan-viewer . && docker run --network host --cap-add=NET_ADMIN acfcan-viewer

Ausfuehren:
    BEAGLE_HOST=192.168.7.2 VIEWER_HOST=192.168.7.50 \
        pytest tests/hardware/test_acfcan_demo.py -v

Umgebungsvariablen:
    BEAGLE_HOST    IP des BeagleBone (Standard: 192.168.7.2)
    BEAGLE_USER    SSH-User          (Standard: debian)
    VIEWER_HOST    IP/Host des acfcan-viewer-Containers (kein Standard — Pflicht)
    ACFCAN_CANIF   CAN-Interface auf dem Board (Standard: vcan0)
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
def demo_verfuegbar():
    if not VIEWER_HOST:
        pytest.skip("VIEWER_HOST nicht gesetzt — kein acfcan-viewer-Endpunkt konfiguriert")
    try:
        r = requests.get(f"http://{VIEWER_HOST}:8080/health", timeout=5)
        r.raise_for_status()
    except Exception as exc:
        pytest.skip(f"acfcan-viewer unter {VIEWER_HOST}:8080 nicht erreichbar: {exc}")

    if ssh("test", "-e", f"/sys/class/net/{CAN_IF}").returncode != 0:
        pytest.skip(f"{CAN_IF} nicht auf {HOST} vorhanden — setup_acfcan_vcan_demo.sh laufen lassen")


class TestAcfCanDemoEndToEnd:
    def test_frame_erscheint_im_viewer(self):
        """Ein auf dem Board gesendetes CAN-Frame taucht im Viewer-/history auf."""
        can_id = "321"
        data = "C0FFEE00"

        ssh("cansend", CAN_IF, f"{can_id}#{data}", check=True)

        deadline = time.time() + 10
        gefunden = False
        while time.time() < deadline and not gefunden:
            resp = requests.get(f"http://{VIEWER_HOST}:8080/history", timeout=5)
            frames = resp.json().get("frames", [])
            gefunden = any(
                f["can_id"].upper() == can_id.upper() and f["data"].upper() == data.upper()
                for f in frames
            )
            if not gefunden:
                time.sleep(0.5)

        if not gefunden:
            pytest.fail(f"Frame {can_id}#{data} nicht im Viewer angekommen (Timeout)")
