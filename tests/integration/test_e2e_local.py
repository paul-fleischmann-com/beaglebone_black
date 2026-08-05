"""
Hardware-freie Verifikation der End-to-End-Kette REST -> CAN -> ACF-CAN
(IEEE 1722) -> CAN -> BME280 aus Issue #270 (siehe Issue #271).

Baut dieselbe 5-Namespace-Topologie wie scripts/setup_e2e_demo.sh und
tests/hardware/test_e2e_demo.py auf — aber lokal per subprocess (kein SSH,
kein physisches BeagleBone Black), auf jedem Linux-Host mit CAP_NET_ADMIN/
CAP_SYS_MODULE (z.B. ein privilegierter Drone-CI-Container). D5
(can-hal-bridge) läuft mit dem CGO-freien Mock-HAL-Treiber
(pkg/hal/mock) statt echtem I2C-Sensor.

Was dieser Test beweist:
    - REST<->CAN-Kodierung (D2 rest-can-gateway), CAN->HAL-Bridge (D5
      can-hal-bridge) und der ACF-CAN-Tunnel (acfcan-Kernelmodul, #256)
      arbeiten korrekt zusammen — Round-Trip-Wert an D1 entspricht exakt
      dem deterministischen Mock-Sensorwert von D5.
    - Das acfcan-Kernelmodul wird hier NATIV für den Kernel des Test-Hosts
      gebaut (siehe scripts/build_acfcan_native.sh) — derselbe
      Open1722-Quellcode wie im Cross-Build fuer den echten BBB-Kernel
      (scripts/build_open1722_acfcan.sh), aber eine andere Binärdatei.

Was dieser Test NICHT beweist:
    - Verhalten auf dem echten BeagleBone-Black-Kernel/-Treiber, echten
      I2C-Sensor oder echter Ethernet-Verkabelung — dafür bleibt
      tests/hardware/test_e2e_demo.py (BEAGLE_HOST-gated, #270 Schritt 8)
      zuständig. Dieser Test ist eine schnelle Vorstufe, kein Ersatz.

Voraussetzungen (werden per Fixture geprüft, Test wird sonst geskippt):
    - root/CAP_NET_ADMIN (Namespaces, veth, vxcan) und CAP_SYS_MODULE
      (acfcan-Kernelmodul laden), z.B. via privilegiertem Docker-Container
    - kmod (modprobe/lsmod/insmod/rmmod) installiert
    - Kernel-Module vxcan, can, can-gw ladbar (Mainline-Kernel-Standard)
    - acfcan.ko: entweder bereits geladen (lsmod) oder unter
      E2E_LOCAL_ACFCAN_KO vorhanden (siehe scripts/build_acfcan_native.sh)
    - can-hal-bridge/rest-can-gateway nativ gebaut (kein GOARM=7-Cross-Build
      wie im Makefile, siehe E2E_LOCAL_BRIDGE_BIN/E2E_LOCAL_GATEWAY_BIN):
          cd project/go-api
          go build -o ../../bin/can-hal-bridge-native ./cmd/can-hal-bridge/
          go build -o ../../bin/rest-can-gateway-native ./cmd/rest-can-gateway/
    - iproute2 (ip), can-utils (cangw; candump/tcpdump optional für die
      Frame-Mitschnitte unten)

Sichtbarer Frame-/Log-Output:
    Der Test faengt die CAN-Frames auf der D2<->D3-Strecke (candump) und die
    rohen ACF-CAN/IEEE-1722-Ethernet-Frames auf der D3<->D4-Strecke (tcpdump
    -X, Hex+ASCII) mit und gibt sie zusammen mit den D2-/D5-Prozess-Logs und
    der JSON-Antwort per print() aus — sichtbar mit `-s`:
    pytest tests/integration/test_e2e_local.py -v -s

Lokal ausführen (als root, nach obigen Builds):
    sudo E2E_LOCAL_ACFCAN_KO=toolchain/open1722/examples/acf-can/linux-kernel-mod/acfcan.ko \
        pytest tests/integration/test_e2e_local.py -v -s

Umgebungsvariablen:
    E2E_LOCAL_BRIDGE_BIN    Pfad zu can-hal-bridge  (Standard: bin/can-hal-bridge-native)
    E2E_LOCAL_GATEWAY_BIN   Pfad zu rest-can-gateway (Standard: bin/rest-can-gateway-native)
    E2E_LOCAL_ACFCAN_KO     Pfad zu acfcan.ko        (Standard: bin/kernel/acfcan-native.ko)
"""

import json
import os
import shutil
import subprocess
import tempfile
import time

import pytest

NAMESPACES = ["dev1", "dev2", "dev3", "dev4", "dev5"]
D1_ADDR = "10.271.1.1"
D2_ADDR = "10.271.1.2"
HTTP_PORT = 8080
# Mock-Treiber in pkg/hal/mock liefert deterministisch diesen Wert (siehe
# tests/hardware/test_e2e_demo.py, dasselbe Akzeptanzkriterium aus #270).
EXPECTED_MOCK_TEMPERATURE = 23.45

BRIDGE_BIN = os.getenv("E2E_LOCAL_BRIDGE_BIN", "bin/can-hal-bridge-native")
GATEWAY_BIN = os.getenv("E2E_LOCAL_GATEWAY_BIN", "bin/rest-can-gateway-native")
ACFCAN_KO = os.getenv("E2E_LOCAL_ACFCAN_KO", "bin/kernel/acfcan-native.ko")


def run(*args, check=False):
    """Fuehrt ein Kommando lokal aus (kein SSH — anders als test_e2e_demo.py)."""
    result = subprocess.run(  # nosec B603 — Argumente sind Konstanten/Fixture-Werte
        list(args), capture_output=True, text=True, timeout=15,
    )
    if check and result.returncode != 0:
        pytest.fail(
            f"{' '.join(args)} fehlgeschlagen (RC={result.returncode}):\n"
            f"stdout: {result.stdout}\nstderr: {result.stderr}"
        )
    return result


def netns(ns, *args, check=False):
    return run("ip", "netns", "exec", ns, *args, check=check)


def _can_manage_netns() -> bool:
    """Testet CAP_NET_ADMIN/CAP_SYS_ADMIN per echtem Probe-Namespace statt
    nur auf os.geteuid() == 0 zu pruefen — auch root in einem unprivilegierten
    Docker-Container kann keine Namespaces anlegen (siehe #271: privilegierter
    CI-Container noetig)."""
    probe = "__e2e_local_probe__"
    run("ip", "netns", "del", probe)  # Aufräumen von evtl. Vorlauf-Leichen
    ok = run("ip", "netns", "add", probe).returncode == 0
    run("ip", "netns", "del", probe)
    return ok


@pytest.fixture(scope="session", autouse=True)
def voraussetzungen_verfuegbar():
    """Prueft Privilegien, Kernel-Module und Binaries — skippt (statt zu
    failen) wenn eine Voraussetzung fehlt, analog zu den BEAGLE_HOST-gated
    Hardware-Tests."""
    if shutil.which("ip") is None:
        pytest.skip("iproute2 (ip) nicht gefunden")
    if shutil.which("modprobe") is None:
        pytest.skip("modprobe (Paket kmod) nicht gefunden")
    if not _can_manage_netns():
        pytest.skip(
            "CAP_NET_ADMIN/CAP_SYS_ADMIN fehlt — Netzwerk-Namespaces koennen "
            "nicht angelegt werden (privilegierten Container/root noetig)"
        )
    for module in ("vxcan", "can", "can-gw"):
        if run("modprobe", "-n", module).returncode != 0:
            pytest.skip(f"Kernel-Modul {module} nicht verfuegbar")

    acfcan_loaded = "acfcan" in run("lsmod").stdout
    if not acfcan_loaded and not os.path.isfile(ACFCAN_KO):
        pytest.skip(
            f"acfcan-Kernelmodul weder geladen noch unter E2E_LOCAL_ACFCAN_KO "
            f"({ACFCAN_KO}) gefunden — siehe scripts/build_acfcan_native.sh"
        )

    for label, path in (("E2E_LOCAL_BRIDGE_BIN", BRIDGE_BIN), ("E2E_LOCAL_GATEWAY_BIN", GATEWAY_BIN)):
        if not (os.path.isfile(path) and os.access(path, os.X_OK)):
            pytest.skip(f"{label}={path} nicht gefunden/ausfuehrbar — siehe Docstring fuer den Build-Befehl")

    if run("which", "cangw").returncode != 0:
        pytest.skip("cangw (can-utils) nicht gefunden")


@pytest.fixture(scope="module", autouse=True)
def e2e_topologie():
    """
    Baut die 5-Namespace-Topologie aus Issue #270 lokal auf (D1<->D2
    veth/REST, D2<->D3 und D4<->D5 vxcan/CAN, D3<->D4 veth+acfcan/ACF-CAN),
    startet can-hal-bridge (D5) und rest-can-gateway (D2) als lokale
    Subprozesse, und raeumt in jedem Fall (auch bei fehlgeschlagenem Setup)
    wieder auf — kein Ressourcen-Leck ueber mehrere Testlaeufe (#271 Punkt 4).
    """
    created_namespaces = []
    bridge_proc = None
    gateway_proc = None
    inserted_acfcan = False

    # Leichen eines vorherigen abgebrochenen Laufs defensiv entfernen.
    for ns in NAMESPACES:
        run("ip", "netns", "del", ns)

    try:
        for ns in NAMESPACES:
            run("ip", "netns", "add", ns, check=True)
            created_namespaces.append(ns)
            netns(ns, "ip", "link", "set", "lo", "up", check=True)

        if "acfcan" not in run("lsmod").stdout:
            run("insmod", ACFCAN_KO, check=True)
            inserted_acfcan = True

        # D1<->D2 (REST, veth)
        run("ip", "link", "add", "veth-d1", "netns", "dev1", "type", "veth",
            "peer", "name", "veth-d2", "netns", "dev2", check=True)
        netns("dev1", "ip", "addr", "add", f"{D1_ADDR}/30", "dev", "veth-d1", check=True)
        netns("dev2", "ip", "addr", "add", f"{D2_ADDR}/30", "dev", "veth-d2", check=True)
        netns("dev1", "ip", "link", "set", "veth-d1", "up", check=True)
        netns("dev2", "ip", "link", "set", "veth-d2", "up", check=True)

        # D2<->D3 und D4<->D5 (CAN, vxcan)
        run("ip", "link", "add", "vxcan-d2", "netns", "dev2", "type", "vxcan",
            "peer", "name", "vxcan-d3", "netns", "dev3", check=True)
        netns("dev2", "ip", "link", "set", "vxcan-d2", "up", check=True)
        netns("dev3", "ip", "link", "set", "vxcan-d3", "up", check=True)

        run("ip", "link", "add", "vxcan-d4", "netns", "dev4", "type", "vxcan",
            "peer", "name", "vxcan-d5", "netns", "dev5", check=True)
        netns("dev4", "ip", "link", "set", "vxcan-d4", "up", check=True)
        netns("dev5", "ip", "link", "set", "vxcan-d5", "up", check=True)

        # D3<->D4 (ACF-CAN ueber Ethernet, veth + acfcan-Modul, #256)
        run("ip", "link", "add", "veth-d3", "netns", "dev3", "type", "veth",
            "peer", "name", "veth-d4", "netns", "dev4", check=True)
        netns("dev3", "ip", "link", "set", "veth-d3", "up", check=True)
        netns("dev4", "ip", "link", "set", "veth-d4", "up", check=True)

        netns("dev3", "ip", "link", "add", "dev", "ecu-d3", "type", "acfcan", check=True)
        netns("dev4", "ip", "link", "add", "dev", "ecu-d4", "type", "acfcan", check=True)
        netns("dev3", "ip", "link", "set", "ecu-d3", "mtu", "72", check=True)
        netns("dev4", "ip", "link", "set", "ecu-d4", "mtu", "72", check=True)

        mac_d3 = netns("dev3", "cat", "/sys/class/net/veth-d3/address", check=True).stdout.strip()
        mac_d4 = netns("dev4", "cat", "/sys/class/net/veth-d4/address", check=True).stdout.strip()

        netns("dev3", "sh", "-c", "echo -n veth-d3 > /sys/class/net/ecu-d3/acfcan/ethif", check=True)
        netns("dev4", "sh", "-c", "echo -n veth-d4 > /sys/class/net/ecu-d4/acfcan/ethif", check=True)
        netns("dev3", "sh", "-c", f"echo -n {mac_d4} > /sys/class/net/ecu-d3/acfcan/dstmac", check=True)
        netns("dev4", "sh", "-c", f"echo -n {mac_d3} > /sys/class/net/ecu-d4/acfcan/dstmac", check=True)

        # Gegenlaeufig gespiegelte Stream-IDs — haeufigste ACF-Fehlerquelle (#256/#259).
        netns("dev3", "sh", "-c", "echo -n cafe11 > /sys/class/net/ecu-d3/acfcan/tx_streamid", check=True)
        netns("dev3", "sh", "-c", "echo -n dead22 > /sys/class/net/ecu-d3/acfcan/rx_streamid", check=True)
        netns("dev4", "sh", "-c", "echo -n dead22 > /sys/class/net/ecu-d4/acfcan/tx_streamid", check=True)
        netns("dev4", "sh", "-c", "echo -n cafe11 > /sys/class/net/ecu-d4/acfcan/rx_streamid", check=True)

        netns("dev3", "ip", "link", "set", "ecu-d3", "up", check=True)
        netns("dev4", "ip", "link", "set", "ecu-d4", "up", check=True)

        netns("dev3", "cangw", "-A", "-s", "vxcan-d3", "-d", "ecu-d3", "-e", check=True)
        netns("dev3", "cangw", "-A", "-s", "ecu-d3", "-d", "vxcan-d3", "-e", check=True)
        netns("dev4", "cangw", "-A", "-s", "ecu-d4", "-d", "vxcan-d4", "-e", check=True)
        netns("dev4", "cangw", "-A", "-s", "vxcan-d4", "-d", "ecu-d4", "-e", check=True)

        log_dir = tempfile.mkdtemp(prefix="e2e-local-")
        bridge_log_path = os.path.join(log_dir, "can-hal-bridge.log")
        gateway_log_path = os.path.join(log_dir, "rest-can-gateway.log")

        # Log-Dateien statt DEVNULL, damit der Test die D2-/D5-Ausgabe
        # (u.a. gelesener Mock-Wert, gesendete/empfangene CAN-IDs) sichtbar
        # machen kann — siehe TestE2ELocal (#271).
        with open(bridge_log_path, "wb") as bridge_log:
            bridge_proc = subprocess.Popen(
                ["ip", "netns", "exec", "dev5", os.path.abspath(BRIDGE_BIN), "--canif", "vxcan-d5"],
                stdout=bridge_log, stderr=subprocess.STDOUT,
            )
        with open(gateway_log_path, "wb") as gateway_log:
            gateway_proc = subprocess.Popen(
                ["ip", "netns", "exec", "dev2", os.path.abspath(GATEWAY_BIN),
                 "--canif", "vxcan-d2", "--http-addr", f"0.0.0.0:{HTTP_PORT}"],
                stdout=gateway_log, stderr=subprocess.STDOUT,
            )
        time.sleep(1)

        yield {"bridge_log": bridge_log_path, "gateway_log": gateway_log_path}
    finally:
        for proc in (gateway_proc, bridge_proc):
            if proc is None:
                continue
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()
                proc.wait(timeout=5)

        for ns in created_namespaces:
            run("ip", "netns", "del", ns)

        if inserted_acfcan:
            run("rmmod", "acfcan")


def _capture_can_frames(ns: str, iface: str, count: int, timeout_s: float = 6.0):
    """Optionale Zwischenstrecken-Pruefung (#271 Punkt 3): faengt bis zu
    `count` CAN-Frames auf `iface` in Namespace `ns` mit `candump` ab. Gibt
    None zurueck (statt zu failen), wenn candump fehlt — die Pruefung ist
    laut Issue #271 optional, das Round-Trip-Ergebnis ist das eigentliche
    Akzeptanzkriterium."""
    if shutil.which("candump") is None:
        return None
    proc = subprocess.Popen(
        ["ip", "netns", "exec", ns, "timeout", str(int(timeout_s)), "candump", "-n", str(count), iface],
        stdout=subprocess.PIPE, text=True,
    )
    return proc


def _capture_eth_frames(ns: str, iface: str, count: int, timeout_s: float = 6.0):
    """Faengt die rohen ACF-CAN/IEEE-1722-Ethernet-Frames auf der D3<->D4-
    Strecke mit (Hex+ASCII via `tcpdump -X`) — macht sichtbar, dass die
    CAN-Frames tatsaechlich als AVTP/ACF-CAN ueber Ethernet getunnelt werden,
    nicht nur dass am Ende ein plausibler CAN-Wert ankommt. Optional wie
    _capture_can_frames: None statt Fehlschlag, wenn tcpdump fehlt."""
    if shutil.which("tcpdump") is None:
        return None
    proc = subprocess.Popen(
        ["ip", "netns", "exec", ns, "timeout", str(int(timeout_s)),
         "tcpdump", "-i", iface, "-c", str(count), "-X", "-n"],
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
    )
    return proc


class TestE2ELocal:
    def test_temperatur_kommt_exakt_ueber_die_gesamte_kette_zurueck(self, e2e_topologie):
        """
        GET /temperature auf D1 durchlaeuft REST -> CAN -> ACF-CAN -> CAN ->
        HAL (Mock) und liefert exakt den Wert zurueck, den D5 lokal vom
        Mock-Treiber liest (Akzeptanzkriterium aus Issue #270, hier ohne
        physisches Board verifiziert, siehe #271).

        Gibt dabei CAN-Frames (D2<->D3), rohe ACF-CAN/IEEE-1722-Ethernet-
        Frames (D3<->D4) und die D2-/D5-Prozess-Logs per print() aus — mit
        `-s` am Terminal sichtbar (siehe Docstring des Moduls).
        """
        # Optional: Request/Response-Frames auf der D2<->D3-CAN-Strecke und
        # den rohen ACF-CAN/IEEE-1722-Ethernet-Frames auf der D3<->D4-Strecke
        # mitschneiden, um zu beweisen dass tatsaechlich CAN- bzw. ACF-CAN-
        # Verkehr unterwegs ist, nicht nur ein plausibler JSON-Wert am Ende
        # zurueckkommt (#271 Punkt 3).
        candump_proc = _capture_can_frames("dev2", "vxcan-d2", count=2)
        tcpdump_proc = _capture_eth_frames("dev3", "veth-d3", count=2)

        try:
            result = netns(
                "dev1", "curl", "-sf", "--max-time", "10", f"http://{D2_ADDR}:{HTTP_PORT}/temperature",
            )
            if result.returncode != 0:
                pytest.fail(f"curl auf D1 fehlgeschlagen (RC={result.returncode}): {result.stderr}")

            body = json.loads(result.stdout)
            print(f"\n=== D1 REST-Antwort (GET /temperature) ===\n{json.dumps(body, indent=2)}")

            assert body["temperature"] == pytest.approx(EXPECTED_MOCK_TEMPERATURE, abs=0.01), (
                f"Round-Trip-Temperatur {body['temperature']} weicht vom lokalen "
                f"Mock-Wert {EXPECTED_MOCK_TEMPERATURE} ab — Nutzsignal wurde auf dem Weg verfälscht"
            )

            if candump_proc is not None:
                candump_out, _ = candump_proc.communicate(timeout=8)
                print(f"\n=== CAN-Frames auf vxcan-d2 (D2<->D3, REST<->ACF-CAN) ===\n{candump_out}")
                frame_lines = [line for line in candump_out.splitlines() if "vxcan-d2" in line]
                assert len(frame_lines) >= 2, (
                    f"Erwartete mindestens 2 CAN-Frames (Anfrage+Antwort) auf vxcan-d2, "
                    f"gefunden: {frame_lines!r} — Round-Trip-Wert stimmte, aber die "
                    f"Zwischenstrecke zeigt kein CAN-Verkehr"
                )
            else:
                print("\n(candump nicht gefunden — CAN-Frame-Mitschnitt uebersprungen)")
        finally:
            if tcpdump_proc is not None:
                tcpdump_out, _ = tcpdump_proc.communicate(timeout=8)
                print(f"\n=== ACF-CAN/IEEE-1722-Ethernet-Frames auf veth-d3 (D3<->D4) ===\n{tcpdump_out}")
            else:
                print("\n(tcpdump nicht gefunden — ACF-CAN/IEEE-1722-Frame-Mitschnitt uebersprungen)")

            for label, path in (("D5 can-hal-bridge", e2e_topologie["bridge_log"]),
                                 ("D2 rest-can-gateway", e2e_topologie["gateway_log"])):
                with open(path) as log_file:
                    print(f"\n=== {label} Log ===\n{log_file.read()}")
