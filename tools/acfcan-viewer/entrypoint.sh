#!/usr/bin/env bash
# Baut die Empfangs-Pipeline im Container auf: lokales vcan-Interface, das
# der acf-can-listener-Prozess mit den über Ethernet empfangenen
# ACF_CAN-Nachrichten befüllt, dann app.py als letzter Schritt (SocketCAN →
# Server-Sent-Events → Browser). Siehe Issue #259.
#
# Braucht --cap-add=NET_ADMIN (vcan-Interface anlegen) und Zugriff auf ein
# echtes Host-Ethernet-Interface (--network host empfohlen, sonst muss
# ACFCAN_VIEWER_ETHIF auf ein im Container sichtbares Interface zeigen).

set -e

CAN_IF=${ACFCAN_VIEWER_CANIF:-vcan1}
ETH_IF=${ACFCAN_VIEWER_ETHIF:-eth0}
LISTENER_ARGS=${ACFCAN_VIEWER_LISTENER_ARGS:-}

if ! ip link show "$CAN_IF" >/dev/null 2>&1; then
  echo "=== Lege $CAN_IF (vcan) an ==="
  modprobe vcan 2>/dev/null || true
  ip link add dev "$CAN_IF" type vcan
  ip link set up "$CAN_IF"
fi

echo "=== Starte acf-can-listener (eth: $ETH_IF, can: $CAN_IF) ==="
# shellcheck disable=SC2086
acf-can-listener -i "$ETH_IF" --canif "$CAN_IF" $LISTENER_ARGS &
LISTENER_PID=$!

trap 'kill $LISTENER_PID 2>/dev/null || true' EXIT

echo "=== Starte acfcan-viewer (Web-Dashboard) ==="
exec python3 /app/app.py
