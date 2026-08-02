#!/usr/bin/env bash
# Baut die Empfangs-Pipeline im Container auf: lokales vcan-Interface, das
# der acf-can-listener-Prozess mit den über Ethernet empfangenen
# ACF_CAN-Nachrichten befüllt, dann app.py als letzter Schritt (SocketCAN →
# Server-Sent-Events → Browser). Siehe Issue #259.
#
# Optional (ACFCAN_VIEWER_ENABLE_MACSEC=1, siehe Issue #260): startet zuerst
# mkad, das ein MACsec-Interface über ETH_IF aufbaut — acf-can-listener
# horcht dann auf diesem verschlüsselten Interface statt auf dem rohen
# ETH_IF. Standardmäßig AUS, damit die #259-Basisdemo unverändert
# funktioniert, wenn niemand explizit MACsec aktiviert.
#
# Braucht --cap-add=NET_ADMIN (vcan-/MACsec-Interface anlegen) und Zugriff
# auf ein echtes Host-Ethernet-Interface (--network host empfohlen, sonst
# müssen ACFCAN_VIEWER_ETHIF/-_ENABLE_MACSEC auf im Container sichtbare
# Interfaces zeigen).

set -e

CAN_IF=${ACFCAN_VIEWER_CANIF:-vcan1}
ETH_IF=${ACFCAN_VIEWER_ETHIF:-eth0}
LISTENER_ARGS=${ACFCAN_VIEWER_LISTENER_ARGS:-}
ENABLE_MACSEC=${ACFCAN_VIEWER_ENABLE_MACSEC:-}
MACSEC_IF=${ACFCAN_VIEWER_MACSEC_IF:-macsec0}
MKAD_CONFIG=${ACFCAN_VIEWER_MKAD_CONFIG:-/app/mkad-viewer.conf}
MKAD_WAIT_TIMEOUT=${ACFCAN_VIEWER_MKAD_WAIT_TIMEOUT:-15}

if ! ip link show "$CAN_IF" >/dev/null 2>&1; then
  echo "=== Lege $CAN_IF (vcan) an ==="
  modprobe vcan 2>/dev/null || true
  ip link add dev "$CAN_IF" type vcan
  ip link set up "$CAN_IF"
fi

LISTENER_ETH_IF="$ETH_IF"

if [ -n "$ENABLE_MACSEC" ]; then
  echo "=== Starte mkad ($MKAD_CONFIG) ==="
  mkad --config "$MKAD_CONFIG" &
  MKAD_PID=$!

  echo "=== Warte auf $MACSEC_IF (Timeout ${MKAD_WAIT_TIMEOUT}s) ==="
  elapsed=0
  while ! ip link show "$MACSEC_IF" >/dev/null 2>&1; do
    if [ "$elapsed" -ge "$MKAD_WAIT_TIMEOUT" ]; then
      echo "FEHLER: $MACSEC_IF nach ${MKAD_WAIT_TIMEOUT}s nicht erschienen — mkad-Log prüfen" >&2
      exit 1
    fi
    sleep 1
    elapsed=$((elapsed + 1))
  done
  LISTENER_ETH_IF="$MACSEC_IF"
  echo "=== $MACSEC_IF vorhanden, acf-can-listener hört darauf statt auf $ETH_IF ==="
fi

echo "=== Starte acf-can-listener (eth: $LISTENER_ETH_IF, can: $CAN_IF) ==="
# shellcheck disable=SC2086
acf-can-listener -i "$LISTENER_ETH_IF" --canif "$CAN_IF" $LISTENER_ARGS &
LISTENER_PID=$!

trap 'kill $LISTENER_PID 2>/dev/null; [ -n "$MKAD_PID" ] && kill $MKAD_PID 2>/dev/null; true' EXIT

echo "=== Starte acfcan-viewer (Web-Dashboard) ==="
exec python3 /app/app.py
