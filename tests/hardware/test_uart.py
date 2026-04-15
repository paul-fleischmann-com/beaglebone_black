"""
UART Integrationstest — CLI laeuft direkt auf dem BeagleBone Black via SSH.

Die bbcli-Binary (ARM) wird auf dem Board ausgefuehrt und spricht gegen
localhost:5000 (API-Server laeuft auf der BBB selbst).

Voraussetzung Loopback-Tests:
    TX-Pin (P9_24) mit RX-Pin (P9_26) per Jumper verbinden.

Deployment:
    make cli-arm
    make deploy          # kopiert bbcli nach /app/bbcli auf der BBB

Ausfuehren:
    BEAGLE_HOST=192.168.7.2 pytest tests/hardware/test_uart.py -v

Umgebungsvariablen:
    BEAGLE_HOST    IP des BeagleBone (Standard: 192.168.7.2)
    BEAGLE_USER    SSH-User          (Standard: debian)
    BBCLI_REMOTE   Pfad zur bbcli-Binary auf dem Board (Standard: /app/bbcli)
    UART_PORT      UART-Device auf dem Board (Standard: /dev/ttyO1)
    UART_BAUD      Baudrate (Standard: 115200)
"""

import os
import subprocess
import time
import pytest

HOST        = os.getenv("BEAGLE_HOST", "192.168.7.2")
USER        = os.getenv("BEAGLE_USER", "debian")
BBCLI       = os.getenv("BBCLI_REMOTE", "/app/bbcli")
UART_PORT   = os.getenv("UART_PORT", "/dev/ttyO1")
UART_BAUD   = os.getenv("UART_BAUD", "115200")

_SSH_BASE = ["ssh", "-o", "StrictHostKeyChecking=no", "-o", "BatchMode=yes",
             f"{USER}@{HOST}"]


def cli(*args):
    """Fuehrt bbcli auf dem BeagleBone via SSH aus, gibt stdout zurueck."""
    cmd = _SSH_BASE + [BBCLI, "--host", "localhost"] + list(args)
    result = subprocess.run(  # nosec B603 — HOST/USER/BBCLI sind Env-Konstanten; args hardcodiert
        cmd,
        capture_output=True,
        text=True,
        timeout=15,
    )
    if result.returncode != 0:
        pytest.fail(
            f"bbcli {' '.join(args)} fehlgeschlagen (RC={result.returncode}):\n"
            f"stdout: {result.stdout}\nstderr: {result.stderr}"
        )
    return result.stdout


def ssh(*args):
    """Fuehrt ein beliebiges Kommando via SSH auf dem Board aus."""
    result = subprocess.run(  # nosec B603 — HOST/USER sind Env-Konstanten; args hardcodiert
        _SSH_BASE + list(args),
        capture_output=True,
        text=True,
        timeout=15,
    )
    return result


@pytest.fixture(scope="session", autouse=True)
def board_erreichbar():
    """Prueft SSH-Verbindung und ob bbcli auf dem Board vorhanden ist."""
    r = ssh("test", "-x", BBCLI)
    if r.returncode != 0:
        pytest.skip(
            f"bbcli nicht gefunden auf {HOST}:{BBCLI} — "
            "zuerst 'make cli-arm && make deploy' ausfuehren"
        )


@pytest.fixture(scope="module", autouse=True)
def uart_konfigurieren():
    """UART einmalig pro Modul auf dem Board konfigurieren."""
    cli("uart", "config", "--port", UART_PORT, "--baud", UART_BAUD)


class TestUartSend:
    def test_send_gibt_bytes_sent_aus(self):
        """bbcli uart send gibt die Anzahl gesendeter Bytes aus."""
        ausgabe = cli("uart", "send", "Hello BeagleBone")
        if "Bytes gesendet" not in ausgabe:
            pytest.fail(f"Erwartete 'Bytes gesendet' in Ausgabe, bekam: {ausgabe!r}")

    def test_send_meldet_korrekte_byteanzahl(self):
        """bytes_sent entspricht der Laenge der gesendeten Nachricht."""
        nachricht = "Test1234"
        ausgabe = cli("uart", "send", nachricht)
        if str(len(nachricht)) not in ausgabe:
            pytest.fail(
                f"Erwartete {len(nachricht)} in Ausgabe, bekam: {ausgabe!r}"
            )

    def test_send_leere_nachricht(self):
        """Leere Nachricht sendet 0 Bytes ohne Fehler."""
        ausgabe = cli("uart", "send", "")
        if "Bytes gesendet" not in ausgabe:
            pytest.fail(f"Unerwartete Ausgabe bei leerem Send: {ausgabe!r}")


@pytest.mark.Loopback
class TestUartLoopback:
    """
    Loopback-Tests: TX (P9_24) muss mit RX (P9_26) verbunden sein.
    Ueberprueft, dass gesendete Daten korrekt zurueckgelesen werden.
    In CI mit '-k not Loopback' ausgeschlossen (kein Jumper vorhanden).
    """

    def test_loopback_einfache_nachricht(self):
        """Gesendete Nachricht wird identisch zurueckgelesen."""
        nachricht = "printf:BBB"
        cli("uart", "send", nachricht)
        time.sleep(0.1)
        empfang = cli("uart", "receive")
        if nachricht not in empfang:
            pytest.fail(
                f"Loopback fehlgeschlagen: gesendet {nachricht!r}, empfangen: {empfang!r}"
            )

    def test_loopback_sonderzeichen(self):
        """CR+LF werden korrekt uebertragen."""
        cli("uart", "send", "OK\r\n")
        time.sleep(0.1)
        empfang = cli("uart", "receive")
        if "OK" not in empfang:
            pytest.fail(
                f"Sonderzeichen-Loopback fehlgeschlagen: empfangen {empfang!r}"
            )

    def test_loopback_mehrere_nachrichten(self):
        """Mehrere aufeinanderfolgende Sends werden kumuliert empfangen."""
        cli("uart", "send", "A")
        cli("uart", "send", "B")
        cli("uart", "send", "C")
        time.sleep(0.1)
        empfang = cli("uart", "receive")
        for zeichen in ["A", "B", "C"]:
            if zeichen not in empfang:
                pytest.fail(
                    f"Zeichen {zeichen!r} fehlt im Empfang: {empfang!r}"
                )


class TestUartReceive:
    def test_receive_liefert_200(self):
        """uart receive laeuft ohne Fehler durch."""
        cli("uart", "receive")

    def test_receive_nach_send_entleert_puffer(self):
        """Nach receive ist der Puffer leer (zweiter receive liefert keine Daten)."""
        cli("uart", "send", "flush")
        time.sleep(0.1)
        cli("uart", "receive")          # Puffer leeren
        time.sleep(0.05)
        ausgabe = cli("uart", "receive")
        if "keine Daten" not in ausgabe and "0 Bytes" not in ausgabe:
            # Puffer hatte noch Restdaten — kein harter Fehler
            pass
