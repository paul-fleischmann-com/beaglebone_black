#!/usr/bin/env bash
# BeagleBone-Black-Seite der vcan→Eth→Container-Demo (#259): legt vcan0 an,
# startet einen Testframe-Generator und tunnelt vcan0 per acf-can-talker
# (Open1722 User-Space-Tool, #257) über Ethernet zur Viewer-Gegenstelle
# (tools/acfcan-viewer, #259). Voraussetzung: bin/open1722/acf-can-talker
# vorhanden (make open1722-userspace) und auf das Board deployed.

set -e

CAN_IF=${ACFCAN_DEMO_CANIF:-vcan0}
ETH_IF=${ACFCAN_DEMO_ETHIF:-eth0}
DST_MAC=${ACFCAN_DEMO_DST_MAC:?"ACFCAN_DEMO_DST_MAC (MAC-Adresse der Viewer-Gegenstelle) muss gesetzt sein"}
TALKER_BIN=${ACFCAN_DEMO_TALKER_BIN:-/app/open1722/acf-can-talker}
FRAME_INTERVAL=${ACFCAN_DEMO_FRAME_INTERVAL:-1}

if ! ip link show "$CAN_IF" >/dev/null 2>&1; then
  echo "=== Lege $CAN_IF (vcan) an ==="
  sudo modprobe vcan
  sudo ip link add dev "$CAN_IF" type vcan
  sudo ip link set up "$CAN_IF"
else
  echo "=== $CAN_IF existiert bereits ==="
fi

echo "=== Starte Testframe-Generator auf $CAN_IF (Intervall ${FRAME_INTERVAL}s) ==="
(
  counter=0
  while true; do
    id=$(printf '%03X' $((counter % 2048)))
    data=$(printf '%02X%02X%02X%02X' $((counter % 256)) $(( (counter / 256) % 256 )) 0xCA 0xFE)
    cansend "$CAN_IF" "${id}#${data}"
    counter=$((counter + 1))
    sleep "$FRAME_INTERVAL"
  done
) &
GENERATOR_PID=$!
trap 'kill $GENERATOR_PID 2>/dev/null || true' EXIT

echo "=== Starte acf-can-talker ($ETH_IF -> $DST_MAC, canif=$CAN_IF) ==="
exec "$TALKER_BIN" -i "$ETH_IF" -d "$DST_MAC" --canif "$CAN_IF"
