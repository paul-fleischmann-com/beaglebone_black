"""
Open1722-User-Space-ACF-CAN-Tools (acf-can-bridge, siehe Issue #257). Kein
HAL-Backend, keine REST-API-Anbindung — Steuerung per SSH via bbcli (siehe
tools/cli/cmd/acfcan.go), analog zum Kernel-Modul-Test test_acfcan.py.

Anders als test_acfcan.py (zwei acfcan-Kernel-Interfaces gegenseitig
verbunden) prueft dieser Test nur EINE laufende acf-can-bridge-Instanz: dass
sie startet, ein auf ihrem CAN-Interface gesendetes Frame tatsaechlich als
IEEE-1722-Frame auf dem Ethernet-Interface auftaucht (per tcpdump verifiziert,
EtherType 0x22F0 nach Issue #256/Teil-1-Doku), und sich sauber stoppen laesst.
Ein Zwei-Bridge-Loopback-Test (analog test_acfcan.py) ist mit dem aktuellen
bbcli-Wrapper nicht moeglich, da dieser genau eine Instanz pro Board verwaltet
(eine globale PID-Datei, siehe acfcan.go) — bewusste Einschraenkung fuer den
Ein-Board-Testaufbau.

Deployment:
    make cli-arm && make deploy                 # bbcli
    make open1722-userspace                     # acf-can-talker/-listener/-bridge
    scp bin/open1722/acf-can-bridge debian@192.168.7.2:/app/open1722/acf-can-bridge

Ausfuehren:
    BEAGLE_HOST=192.168.7.2 pytest tests/hardware/test_acfcan_userspace.py -v

Umgebungsvariablen:
    BEAGLE_HOST    IP des BeagleBone (Standard: 192.168.7.2)
    BEAGLE_USER    SSH-User          (Standard: debian)
    BBCLI_REMOTE   Pfad zur bbcli-Binary auf dem Board (Standard: /app/bbcli)
    ACFCAN_CANIF   CAN-Interface fuer den Test (Standard: vcan0)
"""

import os
import subprocess
import time

import pytest

HOST = os.getenv("BEAGLE_HOST", "192.168.7.2")
USER = os.getenv("BEAGLE_USER", "debian")
BBCLI = os.getenv("BBCLI_REMOTE", "/app/bbcli")
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


def bbcli(*args):
    return ssh(BBCLI, *args)


@pytest.fixture(scope="module", autouse=True)
def bridge_verfuegbar():
    r = ssh("test", "-x", "/app/open1722/acf-can-bridge")
    if r.returncode != 0:
        pytest.skip(
            "acf-can-bridge nicht auf dem Board gefunden — zuerst "
            "'make open1722-userspace' und per scp deployen (siehe Docstring)"
        )
    ssh("sudo", "ip", "link", "add", CAN_IF, "type", "vcan")
    ssh("sudo", "ip", "link", "set", CAN_IF, "up")

    yield

    bbcli("acf-can", "bridge", "stop")
    ssh("sudo", "ip", "link", "del", CAN_IF)


class TestAcfCanBridgeLifecycle:
    def test_start_stop(self):
        """Bridge startet, meldet sich als laufend, laesst sich wieder stoppen."""
        out = bbcli(
            "acf-can", "bridge", "start",
            "--ethif", "eth0", "--canif", CAN_IF,
            "--dst-mac", "ff:ff:ff:ff:ff:ff",
        ).stdout
        if "gestartet" not in out:
            pytest.fail(f"Start-Ausgabe unerwartet: {out!r}")
        time.sleep(0.3)

        status = bbcli("acf-can", "bridge", "status").stdout
        if "läuft" not in status or "läuft nicht" in status:
            pytest.fail(f"Bridge sollte laufen, Status: {status!r}")

        stop_out = bbcli("acf-can", "bridge", "stop").stdout
        if "gestoppt" not in stop_out:
            pytest.fail(f"Stop-Ausgabe unerwartet: {stop_out!r}")

    def test_can_frame_wird_als_ieee1722_frame_gesendet(self):
        """Ein auf CAN_IF gesendetes Frame taucht als IEEE-1722-Frame (EtherType 0x22F0) auf eth0 auf."""
        bbcli(
            "acf-can", "bridge", "start",
            "--ethif", "eth0", "--canif", CAN_IF,
            "--dst-mac", "ff:ff:ff:ff:ff:ff",
        )
        time.sleep(0.3)

        dump = subprocess.Popen(  # nosec B603
            _SSH_BASE + ["sudo", "timeout", "3", "tcpdump", "-i", "eth0",
                         "-c", "1", "ether", "proto", "0x22f0"],
            stdout=subprocess.PIPE,
            text=True,
        )
        time.sleep(0.3)
        ssh("cansend", CAN_IF, "123#DEADBEEF", check=True)
        stdout, _ = dump.communicate(timeout=6)

        bbcli("acf-can", "bridge", "stop")

        if "0x22f0" not in stdout.lower():
            pytest.fail(f"Kein IEEE-1722-Frame (EtherType 0x22F0) auf eth0 gesehen: {stdout!r}")
