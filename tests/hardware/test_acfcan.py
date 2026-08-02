"""
Open1722-ACF-CAN-Kernel-Modul (siehe Issue #256). Kein Teil der Go-HAL/REST-API
(anders als test_pru.py) — acfcan ist ein reines Linux-Kernel-Netzwerkmodul,
angesprochen über SocketCAN (cansend/candump), nicht ueber :5000/api/v1/*.
Kommandos laufen daher wie in test_uart.py per SSH direkt auf dem Board.

Testaufbau: nur EIN BeagleBone Black vorhanden (siehe Issue #256, "Testaufbau
mit nur einem Board") — zwei acfcan-Interfaces (ecu0/ecu1) werden lokal ueber
ein veth-Paar (mon1/mon2) gebrueckt, analog zum Open1722-Upstream-Beispiel
(examples/acf-can/linux-kernel-mod/Readme.md), statt ueber zwei echte
eth0-Ports zwischen zwei physischen Boards.

Deployment:
    make acfcan-mod                       # KERNEL_SRC muss gesetzt sein
    scp bin/kernel/bbb-acfcan.ko debian@192.168.7.2:/lib/modules/$(uname -r)/extra/acfcan.ko
    ssh debian@192.168.7.2 depmod -a

Ausfuehren:
    BEAGLE_HOST=192.168.7.2 pytest tests/hardware/test_acfcan.py -v

Umgebungsvariablen:
    BEAGLE_HOST    IP des BeagleBone (Standard: 192.168.7.2)
    BEAGLE_USER    SSH-User          (Standard: debian)
"""

import os
import subprocess
import time

import pytest

HOST = os.getenv("BEAGLE_HOST", "192.168.7.2")
USER = os.getenv("BEAGLE_USER", "debian")

_SSH_BASE = ["ssh", "-o", "StrictHostKeyChecking=no", "-o", "BatchMode=yes",
             f"{USER}@{HOST}"]


def ssh(*args, check=False):
    """Fuehrt ein Kommando via SSH auf dem Board aus (ggf. mit sudo)."""
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


@pytest.fixture(scope="session", autouse=True)
def modul_verfuegbar():
    """Prueft, ob acfcan.ko auf dem Board vorhanden/ladbar ist."""
    r = ssh("sudo", "modprobe", "-n", "acfcan")
    if r.returncode != 0:
        pytest.skip(
            f"acfcan-Kernel-Modul nicht auf {HOST} gefunden — zuerst "
            "'make acfcan-mod' (KERNEL_SRC setzen) und per scp deployen "
            "(siehe Docstring)"
        )


@pytest.fixture(scope="module", autouse=True)
def acfcan_veth_setup():
    """
    Baut den Ein-Board-Testaufbau auf: veth-Paar (mon1/mon2) + zwei
    acfcan-Interfaces (ecu0/ecu1), gegenseitig ueber die veth-MACs und
    gespiegelte Stream-IDs verbunden. Raeumt am Ende wieder auf.
    """
    ssh("sudo", "modprobe", "can")
    ssh("sudo", "modprobe", "acfcan")

    ssh("sudo", "ip", "link", "add", "dev", "mon1", "type", "veth", "peer", "name", "mon2")
    ssh("sudo", "ip", "link", "set", "mon1", "up")
    ssh("sudo", "ip", "link", "set", "mon2", "up")

    ssh("sudo", "ip", "link", "add", "dev", "ecu0", "type", "acfcan")
    ssh("sudo", "ip", "link", "add", "dev", "ecu1", "type", "acfcan")
    ssh("sudo", "ip", "link", "set", "ecu0", "mtu", "72")
    ssh("sudo", "ip", "link", "set", "ecu1", "mtu", "72")

    mon1_mac = ssh("cat", "/sys/class/net/mon1/address").stdout.strip()
    mon2_mac = ssh("cat", "/sys/class/net/mon2/address").stdout.strip()

    ssh("sh", "-c", "echo -n mon1 | sudo tee /sys/class/net/ecu0/acfcan/ethif")
    ssh("sh", "-c", "echo -n mon2 | sudo tee /sys/class/net/ecu1/acfcan/ethif")
    ssh("sh", "-c", f"echo -n {mon2_mac} | sudo tee /sys/class/net/ecu0/acfcan/dstmac")
    ssh("sh", "-c", f"echo -n {mon1_mac} | sudo tee /sys/class/net/ecu1/acfcan/dstmac")

    # tx_streamid/rx_streamid gegenlaeufig gespiegelt (siehe Issue #256/#259) —
    # sonst verwirft die Gegenseite die ACF-CAN-Pakete kommentarlos.
    ssh("sh", "-c", "echo -n cafe11 | sudo tee /sys/class/net/ecu0/acfcan/tx_streamid")
    ssh("sh", "-c", "echo -n dead22 | sudo tee /sys/class/net/ecu0/acfcan/rx_streamid")
    ssh("sh", "-c", "echo -n dead22 | sudo tee /sys/class/net/ecu1/acfcan/tx_streamid")
    ssh("sh", "-c", "echo -n cafe11 | sudo tee /sys/class/net/ecu1/acfcan/rx_streamid")

    ssh("sudo", "ip", "link", "set", "up", "ecu0")
    ssh("sudo", "ip", "link", "set", "up", "ecu1")
    time.sleep(0.5)

    yield

    ssh("sudo", "ip", "link", "del", "ecu0")
    ssh("sudo", "ip", "link", "del", "ecu1")
    ssh("sudo", "ip", "link", "del", "mon1")
    ssh("sudo", "rmmod", "acfcan")


class TestAcfCanTunneling:
    def test_frame_kommt_ueber_ecu1_an(self):
        """Ein auf ecu0 gesendetes CAN-Frame erscheint per ACF-CAN-Tunnel auf ecu1."""
        dump = subprocess.Popen(  # nosec B603
            _SSH_BASE + ["timeout", "3", "candump", "ecu1"],
            stdout=subprocess.PIPE,
            text=True,
        )
        time.sleep(0.3)
        ssh("cansend", "ecu0", "123#DEADBEEF", check=True)
        stdout, _ = dump.communicate(timeout=5)

        if "123" not in stdout or "DEADBEEF" not in stdout.replace(" ", "").upper():
            pytest.fail(f"Frame nicht (korrekt) auf ecu1 angekommen: {stdout!r}")

    def test_beide_richtungen_funktionieren(self):
        """Tunnel funktioniert auch in Gegenrichtung (ecu1 -> ecu0)."""
        dump = subprocess.Popen(  # nosec B603
            _SSH_BASE + ["timeout", "3", "candump", "ecu0"],
            stdout=subprocess.PIPE,
            text=True,
        )
        time.sleep(0.3)
        ssh("cansend", "ecu1", "456#CAFEBABE", check=True)
        stdout, _ = dump.communicate(timeout=5)

        if "456" not in stdout:
            pytest.fail(f"Frame nicht in Gegenrichtung angekommen: {stdout!r}")
