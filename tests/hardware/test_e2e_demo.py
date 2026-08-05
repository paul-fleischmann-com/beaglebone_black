"""
End-to-End-Demo REST -> CAN -> ACF-CAN (IEEE 1722) -> CAN -> BME280 über 5
virtuelle Devices (siehe Issue #270). Baut auf #256 (acfcan-Kernelmodul) und
#259 (vxcan/vcan-Demo-Muster) auf.

Nur EIN BeagleBone Black vorhanden (wie bereits in #256 festgehalten) — alle
5 "Devices" laufen deshalb als eigene Linux-Network-Namespaces auf demselben
Board, siehe scripts/setup_e2e_demo.sh für die interaktive Variante. Dieser
Test baut die Topologie unabhängig davon direkt per SSH auf (analog zu
test_acfcan.py, das ebenfalls unabhängig von setup_acfcan_vcan_demo.sh
testet), um nicht von einem Deploy des Shell-Skripts selbst abzuhängen.

Deployment (Vorbereitung, einmalig):
    make acfcan-mod                        # KERNEL_SRC muss gesetzt sein
    scp bin/kernel/bbb-acfcan.ko debian@192.168.7.2:/lib/modules/$(uname -r)/extra/acfcan.ko
    ssh debian@192.168.7.2 depmod -a
    make can-hal-bridge rest-can-gateway
    scp bin/can-hal-bridge bin/rest-can-gateway debian@192.168.7.2:/app/

Ausführen:
    BEAGLE_HOST=192.168.7.2 pytest tests/hardware/test_e2e_demo.py -v

Umgebungsvariablen:
    BEAGLE_HOST    IP des BeagleBone (Standard: 192.168.7.2)
    BEAGLE_USER    SSH-User          (Standard: debian)
"""

import json
import os
import subprocess
import time

import pytest

HOST = os.getenv("BEAGLE_HOST", "192.168.7.2")
USER = os.getenv("BEAGLE_USER", "debian")

_SSH_BASE = ["ssh", "-o", "StrictHostKeyChecking=no", "-o", "BatchMode=yes",
             f"{USER}@{HOST}"]

NAMESPACES = ["dev1", "dev2", "dev3", "dev4", "dev5"]
D1_ADDR = "10.270.1.1"
D2_ADDR = "10.270.1.2"
HTTP_PORT = 8080
# Mock-Treiber in pkg/hal/mock liefert deterministisch diesen Wert — der
# Round-Trip-Wert an D1 muss exakt diesem entsprechen (Akzeptanzkriterium #270).
EXPECTED_MOCK_TEMPERATURE = 23.45


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
def voraussetzungen_verfuegbar():
    """Prueft, ob acfcan.ko, vxcan/can-gw-Module und die Demo-Binaries vorhanden sind."""
    if ssh("sudo", "modprobe", "-n", "acfcan").returncode != 0:
        pytest.skip(f"acfcan-Kernelmodul nicht auf {HOST} gefunden — siehe Docstring")
    if ssh("sudo", "modprobe", "-n", "vxcan").returncode != 0:
        pytest.skip(f"vxcan-Kernelmodul nicht auf {HOST} gefunden")
    if ssh("sudo", "modprobe", "-n", "can-gw").returncode != 0:
        pytest.skip(f"can-gw-Kernelmodul nicht auf {HOST} gefunden")
    if ssh("test", "-x", "/app/can-hal-bridge").returncode != 0:
        pytest.skip("/app/can-hal-bridge nicht auf dem Board gefunden — siehe Docstring")
    if ssh("test", "-x", "/app/rest-can-gateway").returncode != 0:
        pytest.skip("/app/rest-can-gateway nicht auf dem Board gefunden — siehe Docstring")
    if ssh("which", "cangw").returncode != 0:
        pytest.skip("cangw (can-utils) nicht auf dem Board installiert")


@pytest.fixture(scope="module", autouse=True)
def e2e_topologie():
    """
    Baut die 5-Namespace-Topologie aus Issue #270 auf (D1<->D2 veth/REST,
    D2<->D3 und D4<->D5 vxcan/CAN, D3<->D4 veth+acfcan/ACF-CAN), startet
    can-hal-bridge (D5) und rest-can-gateway (D2), und raeumt am Ende
    wieder auf.
    """
    ssh("sudo", "modprobe", "can")
    ssh("sudo", "modprobe", "can-gw")
    ssh("sudo", "modprobe", "vxcan")
    ssh("sudo", "modprobe", "acfcan")

    for ns in NAMESPACES:
        ssh("sudo", "ip", "netns", "add", ns)
        ssh("sudo", "ip", "netns", "exec", ns, "ip", "link", "set", "lo", "up")

    # D1<->D2 (REST, veth)
    ssh("sudo", "ip", "link", "add", "veth-d1", "netns", "dev1", "type", "veth",
        "peer", "name", "veth-d2", "netns", "dev2", check=True)
    ssh("sudo", "ip", "netns", "exec", "dev1", "ip", "addr", "add", f"{D1_ADDR}/30", "dev", "veth-d1")
    ssh("sudo", "ip", "netns", "exec", "dev2", "ip", "addr", "add", f"{D2_ADDR}/30", "dev", "veth-d2")
    ssh("sudo", "ip", "netns", "exec", "dev1", "ip", "link", "set", "veth-d1", "up")
    ssh("sudo", "ip", "netns", "exec", "dev2", "ip", "link", "set", "veth-d2", "up")

    # D2<->D3 und D4<->D5 (CAN, vxcan)
    ssh("sudo", "ip", "link", "add", "vxcan-d2", "netns", "dev2", "type", "vxcan",
        "peer", "name", "vxcan-d3", "netns", "dev3", check=True)
    ssh("sudo", "ip", "netns", "exec", "dev2", "ip", "link", "set", "vxcan-d2", "up")
    ssh("sudo", "ip", "netns", "exec", "dev3", "ip", "link", "set", "vxcan-d3", "up")

    ssh("sudo", "ip", "link", "add", "vxcan-d4", "netns", "dev4", "type", "vxcan",
        "peer", "name", "vxcan-d5", "netns", "dev5", check=True)
    ssh("sudo", "ip", "netns", "exec", "dev4", "ip", "link", "set", "vxcan-d4", "up")
    ssh("sudo", "ip", "netns", "exec", "dev5", "ip", "link", "set", "vxcan-d5", "up")

    # D3<->D4 (ACF-CAN über Ethernet, veth + acfcan-Modul, #256)
    ssh("sudo", "ip", "link", "add", "veth-d3", "netns", "dev3", "type", "veth",
        "peer", "name", "veth-d4", "netns", "dev4", check=True)
    ssh("sudo", "ip", "netns", "exec", "dev3", "ip", "link", "set", "veth-d3", "up")
    ssh("sudo", "ip", "netns", "exec", "dev4", "ip", "link", "set", "veth-d4", "up")

    ssh("sudo", "ip", "netns", "exec", "dev3", "ip", "link", "add", "dev", "ecu-d3", "type", "acfcan")
    ssh("sudo", "ip", "netns", "exec", "dev4", "ip", "link", "add", "dev", "ecu-d4", "type", "acfcan")
    ssh("sudo", "ip", "netns", "exec", "dev3", "ip", "link", "set", "ecu-d3", "mtu", "72")
    ssh("sudo", "ip", "netns", "exec", "dev4", "ip", "link", "set", "ecu-d4", "mtu", "72")

    mac_d3 = ssh("sudo", "ip", "netns", "exec", "dev3", "cat", "/sys/class/net/veth-d3/address").stdout.strip()
    mac_d4 = ssh("sudo", "ip", "netns", "exec", "dev4", "cat", "/sys/class/net/veth-d4/address").stdout.strip()

    ssh("sudo", "ip", "netns", "exec", "dev3", "sh", "-c",
        "echo -n veth-d3 | tee /sys/class/net/ecu-d3/acfcan/ethif")
    ssh("sudo", "ip", "netns", "exec", "dev4", "sh", "-c",
        "echo -n veth-d4 | tee /sys/class/net/ecu-d4/acfcan/ethif")
    ssh("sudo", "ip", "netns", "exec", "dev3", "sh", "-c",
        f"echo -n {mac_d4} | tee /sys/class/net/ecu-d3/acfcan/dstmac")
    ssh("sudo", "ip", "netns", "exec", "dev4", "sh", "-c",
        f"echo -n {mac_d3} | tee /sys/class/net/ecu-d4/acfcan/dstmac")

    # Gegenlaeufig gespiegelte Stream-IDs — haeufigste ACF-Fehlerquelle (#256/#259)
    ssh("sudo", "ip", "netns", "exec", "dev3", "sh", "-c",
        "echo -n cafe11 | tee /sys/class/net/ecu-d3/acfcan/tx_streamid")
    ssh("sudo", "ip", "netns", "exec", "dev3", "sh", "-c",
        "echo -n dead22 | tee /sys/class/net/ecu-d3/acfcan/rx_streamid")
    ssh("sudo", "ip", "netns", "exec", "dev4", "sh", "-c",
        "echo -n dead22 | tee /sys/class/net/ecu-d4/acfcan/tx_streamid")
    ssh("sudo", "ip", "netns", "exec", "dev4", "sh", "-c",
        "echo -n cafe11 | tee /sys/class/net/ecu-d4/acfcan/rx_streamid")

    ssh("sudo", "ip", "netns", "exec", "dev3", "ip", "link", "set", "ecu-d3", "up")
    ssh("sudo", "ip", "netns", "exec", "dev4", "ip", "link", "set", "ecu-d4", "up")

    ssh("sudo", "ip", "netns", "exec", "dev3", "cangw", "-A", "-s", "vxcan-d3", "-d", "ecu-d3", "-e")
    ssh("sudo", "ip", "netns", "exec", "dev3", "cangw", "-A", "-s", "ecu-d3", "-d", "vxcan-d3", "-e")
    ssh("sudo", "ip", "netns", "exec", "dev4", "cangw", "-A", "-s", "ecu-d4", "-d", "vxcan-d4", "-e")
    ssh("sudo", "ip", "netns", "exec", "dev4", "cangw", "-A", "-s", "vxcan-d4", "-d", "ecu-d4", "-e")

    # D5: can-hal-bridge (Mock-HAL) und D2: rest-can-gateway im Hintergrund starten.
    ssh("sudo", "ip", "netns", "exec", "dev5", "sh", "-c",
        "nohup /app/can-hal-bridge --canif vxcan-d5 > /tmp/e2e-can-hal-bridge.log 2>&1 &")
    ssh("sudo", "ip", "netns", "exec", "dev2", "sh", "-c",
        f"nohup /app/rest-can-gateway --canif vxcan-d2 --http-addr 0.0.0.0:{HTTP_PORT} "
        "> /tmp/e2e-rest-can-gateway.log 2>&1 &")
    time.sleep(1)

    yield

    ssh("sudo", "pkill", "-f", "can-hal-bridge")
    ssh("sudo", "pkill", "-f", "rest-can-gateway")
    for ns in NAMESPACES:
        ssh("sudo", "ip", "netns", "del", ns)
    ssh("sudo", "rmmod", "acfcan")


class TestE2EDemo:
    def test_temperatur_kommt_exakt_ueber_die_gesamte_kette_zurueck(self):
        """
        GET /temperature auf D1 durchlaeuft REST -> CAN -> ACF-CAN -> CAN ->
        HAL (Mock) und liefert exakt den Wert zurueck, den D5 lokal vom
        Mock-Treiber liest (Akzeptanzkriterium aus Issue #270).
        """
        result = ssh(
            "sudo", "ip", "netns", "exec", "dev1",
            "curl", "-sf", "--max-time", "10", f"http://{D2_ADDR}:{HTTP_PORT}/temperature",
        )
        if result.returncode != 0:
            pytest.fail(
                f"curl auf D1 fehlgeschlagen (RC={result.returncode}): {result.stderr}\n"
                f"Bridge-Log: {ssh('cat', '/tmp/e2e-can-hal-bridge.log').stdout}\n"
                f"Gateway-Log: {ssh('cat', '/tmp/e2e-rest-can-gateway.log').stdout}"
            )

        body = json.loads(result.stdout)
        assert body["temperature"] == pytest.approx(EXPECTED_MOCK_TEMPERATURE, abs=0.01), (
            f"Round-Trip-Temperatur {body['temperature']} weicht vom lokalen "
            f"Mock-Wert {EXPECTED_MOCK_TEMPERATURE} ab — Nutzsignal wurde auf dem Weg verfälscht"
        )
