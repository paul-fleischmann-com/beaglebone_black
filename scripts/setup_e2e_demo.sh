#!/usr/bin/env bash
# BeagleBone-Black-Seite der REST→CAN→ACF-CAN→CAN→BME280-Demo (#270): baut
# alle 5 "Devices" aus dem Issue-Diagramm als eigene Linux-Network-Namespaces
# auf einem einzigen Board auf (nur ein physisches BeagleBone Black
# vorhanden, wie bereits in #256/#259 festgehalten):
#
#   dev1 --veth(REST)--> dev2 --vxcan(CAN)--> dev3 --veth+acfcan(IEEE1722)--> dev4 --vxcan(CAN)--> dev5
#
# dev2 startet rest-can-gateway (D2, #270), dev5 startet can-hal-bridge
# (D5, #270, Mock-HAL-Treiber als Default). dev3/dev4 nutzen das acfcan-
# Kernelmodul (#256) — die User-Space-Alternative (acf-can-talker/-listener,
# #257) ist eine reine Konfigurationsvariante dieses Skripts, hier nicht
# implementiert. Die Weiterleitung zwischen dem CAN-Interface Richtung
# D2/D5 (vxcan-dX) und dem ACF-CAN-Interface Richtung D4/D3 (ecu-dX) läuft
# rein im Kernel über das can-gw-Modul (cangw-Tool aus can-utils) — kein
# eigener Relay-Prozess nötig.
#
# Voraussetzung: acfcan.ko auf dem Board geladen (siehe
# tests/hardware/test_acfcan.py), can-utils (cangw) installiert,
# bin/can-hal-bridge + bin/rest-can-gateway deployed (siehe Pfade unten).
#
# Ausführen (als root, blockiert im Vordergrund):
#   sudo ./scripts/setup_e2e_demo.sh
# Test (in einer zweiten Sitzung):
#   sudo ip netns exec dev1 curl http://10.270.1.2:8080/temperature
# Aufräumen:
#   sudo ./scripts/setup_e2e_demo.sh teardown

set -e

NAMESPACES="dev1 dev2 dev3 dev4 dev5"
BRIDGE_BIN=${E2E_DEMO_BRIDGE_BIN:-/app/can-hal-bridge}
GATEWAY_BIN=${E2E_DEMO_GATEWAY_BIN:-/app/rest-can-gateway}
HTTP_PORT=${E2E_DEMO_HTTP_PORT:-8080}
D1_IP=${E2E_DEMO_D1_IP:-10.270.1.1/30}
D2_IP=${E2E_DEMO_D2_IP:-10.270.1.2/30}

if [ "${1:-}" = "teardown" ]; then
  echo "=== Räume Namespaces auf: $NAMESPACES ==="
  for ns in $NAMESPACES; do
    ip netns del "$ns" 2>/dev/null || true
  done
  exit 0
fi

if ! modprobe -n acfcan 2>/dev/null; then
  echo "FEHLER: acfcan-Kernelmodul nicht gefunden — zuerst 'make acfcan-mod' und deployen (siehe tests/hardware/test_acfcan.py)" >&2
  exit 1
fi
if ! command -v cangw >/dev/null 2>&1; then
  echo "FEHLER: cangw (can-utils) nicht gefunden — 'apt install can-utils'" >&2
  exit 1
fi

modprobe -q can || true
modprobe -q can-gw || true
modprobe -q vxcan || true
modprobe -q acfcan || true

echo "=== Lege Namespaces an: $NAMESPACES ==="
for ns in $NAMESPACES; do
  ip netns list | grep -qx "$ns" || ip netns add "$ns"
  ip netns exec "$ns" ip link set lo up
done

echo "=== D1<->D2 (REST, veth) ==="
if ! ip netns exec dev1 ip link show veth-d1 >/dev/null 2>&1; then
  ip link add veth-d1 netns dev1 type veth peer name veth-d2 netns dev2
  ip netns exec dev1 ip addr add "$D1_IP" dev veth-d1
  ip netns exec dev2 ip addr add "$D2_IP" dev veth-d2
  ip netns exec dev1 ip link set veth-d1 up
  ip netns exec dev2 ip link set veth-d2 up
fi

echo "=== D2<->D3 (CAN, vxcan) ==="
if ! ip netns exec dev2 ip link show vxcan-d2 >/dev/null 2>&1; then
  ip link add vxcan-d2 netns dev2 type vxcan peer name vxcan-d3 netns dev3
  ip netns exec dev2 ip link set vxcan-d2 up
  ip netns exec dev3 ip link set vxcan-d3 up
fi

echo "=== D4<->D5 (CAN, vxcan) ==="
if ! ip netns exec dev4 ip link show vxcan-d4 >/dev/null 2>&1; then
  ip link add vxcan-d4 netns dev4 type vxcan peer name vxcan-d5 netns dev5
  ip netns exec dev4 ip link set vxcan-d4 up
  ip netns exec dev5 ip link set vxcan-d5 up
fi

echo "=== D3<->D4 (ACF-CAN über Ethernet, veth + acfcan-Modul, #256) ==="
if ! ip netns exec dev3 ip link show ecu-d3 >/dev/null 2>&1; then
  ip link add veth-d3 netns dev3 type veth peer name veth-d4 netns dev4
  ip netns exec dev3 ip link set veth-d3 up
  ip netns exec dev4 ip link set veth-d4 up

  ip netns exec dev3 ip link add dev ecu-d3 type acfcan
  ip netns exec dev4 ip link add dev ecu-d4 type acfcan
  ip netns exec dev3 ip link set ecu-d3 mtu 72
  ip netns exec dev4 ip link set ecu-d4 mtu 72

  mac_d3=$(ip netns exec dev3 cat /sys/class/net/veth-d3/address)
  mac_d4=$(ip netns exec dev4 cat /sys/class/net/veth-d4/address)

  ip netns exec dev3 sh -c "echo -n veth-d3 > /sys/class/net/ecu-d3/acfcan/ethif"
  ip netns exec dev4 sh -c "echo -n veth-d4 > /sys/class/net/ecu-d4/acfcan/ethif"
  ip netns exec dev3 sh -c "echo -n $mac_d4 > /sys/class/net/ecu-d3/acfcan/dstmac"
  ip netns exec dev4 sh -c "echo -n $mac_d3 > /sys/class/net/ecu-d4/acfcan/dstmac"

  # Gegenläufig gespiegelte Stream-IDs — häufigste ACF-Fehlerquelle (#256/#259):
  # tx auf der einen Seite muss exakt rx auf der anderen sein.
  ip netns exec dev3 sh -c "echo -n cafe11 > /sys/class/net/ecu-d3/acfcan/tx_streamid"
  ip netns exec dev3 sh -c "echo -n dead22 > /sys/class/net/ecu-d3/acfcan/rx_streamid"
  ip netns exec dev4 sh -c "echo -n dead22 > /sys/class/net/ecu-d4/acfcan/tx_streamid"
  ip netns exec dev4 sh -c "echo -n cafe11 > /sys/class/net/ecu-d4/acfcan/rx_streamid"

  ip netns exec dev3 ip link set ecu-d3 up
  ip netns exec dev4 ip link set ecu-d4 up
fi

echo "=== CAN-Gateway-Regeln (Kernel can-gw): vxcan-dX <-> ecu-dX ==="
ip netns exec dev3 cangw -A -s vxcan-d3 -d ecu-d3 -e 2>/dev/null || true
ip netns exec dev3 cangw -A -s ecu-d3 -d vxcan-d3 -e 2>/dev/null || true
ip netns exec dev4 cangw -A -s ecu-d4 -d vxcan-d4 -e 2>/dev/null || true
ip netns exec dev4 cangw -A -s vxcan-d4 -d ecu-d4 -e 2>/dev/null || true

echo "=== Starte D5 can-hal-bridge (Mock-HAL, vxcan-d5) ==="
ip netns exec dev5 "$BRIDGE_BIN" --canif vxcan-d5 &
BRIDGE_PID=$!

echo "=== Starte D2 rest-can-gateway (vxcan-d2, :$HTTP_PORT) ==="
ip netns exec dev2 "$GATEWAY_BIN" --canif vxcan-d2 --http-addr "0.0.0.0:$HTTP_PORT" &
GATEWAY_PID=$!

trap 'kill $BRIDGE_PID $GATEWAY_PID 2>/dev/null || true' EXIT

d2_addr=${D2_IP%/*}
echo "=== Bereit ==="
echo "Test (zweite Sitzung): ip netns exec dev1 curl http://$d2_addr:$HTTP_PORT/temperature"
echo "Aufräumen: $0 teardown"

wait $BRIDGE_PID $GATEWAY_PID
