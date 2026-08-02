"""
acfcan-viewer — Open1722-ETH-Node-Empfänger mit Live-Visualisierung (#259).

Liest dekodierte CAN-Frames von einem lokalen SocketCAN-Interface (vcanX),
das der acf-can-listener-Prozess (Open1722, siehe #257) mit den über
Ethernet empfangenen ACF_CAN-Nachrichten befüllt, und streamt sie per
Server-Sent-Events an ein einfaches HTML/JS-Dashboard (siehe index.html).

Der Container selbst spricht kein AVTP/ACF — das übernimmt vollständig der
separat gestartete acf-can-listener-Prozess (siehe entrypoint.sh). Dieses
Skript ist bewusst nur der letzte Schritt der Pipeline (SocketCAN → Browser),
kein eigener IEEE-1722-Parser.
"""

import json
import os
import queue
import re
import subprocess
import threading
import time
from datetime import datetime, timezone

import can
from flask import Flask, Response, send_from_directory

CAN_IF = os.environ.get("ACFCAN_VIEWER_CANIF", "vcan1")
HTTP_PORT = int(os.environ.get("ACFCAN_VIEWER_PORT", "8080"))
MACSEC_IF = os.environ.get("ACFCAN_VIEWER_MACSEC_IF", "macsec0")
MAX_HISTORY = 100

app = Flask(__name__)
_subscribers: list[queue.Queue] = []
_subscribers_lock = threading.Lock()
_history: list[dict] = []
_history_lock = threading.Lock()


def _broadcast(frame: dict) -> None:
    with _history_lock:
        _history.append(frame)
        del _history[:-MAX_HISTORY]
    with _subscribers_lock:
        for q in _subscribers:
            q.put(frame)


def _can_listener_loop() -> None:
    """Läuft im Hintergrund, solange vcanX existiert — reconnectet bei Fehlern."""
    while True:
        try:
            bus = can.interface.Bus(channel=CAN_IF, interface="socketcan")
            for msg in bus:
                frame = {
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "can_id": f"{msg.arbitration_id:X}",
                    "dlc": msg.dlc,
                    "data": msg.data.hex().upper(),
                }
                _broadcast(frame)
        except Exception as exc:  # Interface evtl. noch nicht bereit
            print(f"[acfcan-viewer] CAN-Bus-Fehler auf {CAN_IF}: {exc} — retry in 2s")
            time.sleep(2)


@app.route("/")
def index():
    return send_from_directory(os.path.dirname(__file__), "index.html")


@app.route("/history")
def history():
    """Letzte empfangene Frames als JSON — für Tests/Skripte einfacher zu
    konsumieren als der SSE-Stream (siehe tests/hardware/test_acfcan_demo.py)."""
    with _history_lock:
        return {"frames": list(_history)}


@app.route("/stream")
def stream():
    q: queue.Queue = queue.Queue()
    with _subscribers_lock:
        _subscribers.append(q)

    def gen():
        with _history_lock:
            for frame in _history:
                yield f"data: {json.dumps(frame)}\n\n"
        try:
            while True:
                frame = q.get()
                yield f"data: {json.dumps(frame)}\n\n"
        finally:
            with _subscribers_lock:
                _subscribers.remove(q)

    return Response(gen(), mimetype="text/event-stream")


@app.route("/macsec-status")
def macsec_status():
    """Status-Badge für die MACsec/MKA-Absicherung (#260) — best-effort per
    `ip macsec show`, kein DBus-Client (mkad läuft mit DISABLE_DBUS=1)."""
    try:
        result = subprocess.run(  # nosec B603 B607 — kein User-Input, fester Interface-Name
            ["ip", "macsec", "show", MACSEC_IF],
            capture_output=True, text=True, timeout=5,
        )
    except FileNotFoundError:
        return {"active": False, "reason": "ip-Kommando nicht verfügbar"}

    if result.returncode != 0:
        return {"active": False, "interface": MACSEC_IF, "reason": "Interface nicht vorhanden"}

    active_sa = bool(re.search(r"state on", result.stdout))
    return {
        "active": active_sa,
        "interface": MACSEC_IF,
        "reason": "SA aktiv" if active_sa else "Interface vorhanden, keine aktive SA",
    }


@app.route("/health")
def health():
    return {"status": "ok", "canif": CAN_IF}


if __name__ == "__main__":
    threading.Thread(target=_can_listener_loop, daemon=True).start()
    app.run(host="0.0.0.0", port=HTTP_PORT, threaded=True)  # nosec B104 — Demo-Container, absichtlich auf allen Interfaces
