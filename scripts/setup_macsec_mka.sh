#!/usr/bin/env bash
# BeagleBone-Black-Seite der MACsec/MKA-Absicherung (#260): startet mkad mit
# project/macsec/mkad-board.conf, wartet bis das MACsec-Interface (macsec0)
# existiert. Danach sollten acf-can-talker/acfcan/acf-can-bridge (#256/#257)
# gegen "macsec0" statt "eth0" konfiguriert werden — sie tunneln dann
# automatisch über die verschlüsselte Verbindung, ohne selbst etwas von
# MACsec zu wissen (macsec0 ist ein ganz normales Netzwerkinterface).
#
# Voraussetzung: mkad auf dem Board vorhanden (Yocto-Recipe project/yocto/
# meta-bbb-sensors/recipes-bbb/mkad/, Teil von bbb-full-image), cak/ckn in
# mkad-board.conf identisch zur Gegenstelle (mkad-viewer.conf).

set -e

# Läuft auf dem Board selbst (analog scripts/setup_acfcan_vcan_demo.sh) —
# Standardpfad geht von einem Deploy nach /app/ aus (scp
# project/macsec/mkad-board.conf debian@192.168.7.2:/app/mkad-board.conf),
# nicht von einem vollständigen Repo-Checkout auf dem Board.
MKAD_BIN=${MKAD_BIN:-/usr/bin/mkad}
CONFIG=${MKAD_CONFIG:-/app/mkad-board.conf}
PROTECTED_IF=${MACSEC_PROTECTED_IF:-macsec0}
TIMEOUT=${MACSEC_WAIT_TIMEOUT:-15}

echo "=== Starte mkad ($CONFIG) ==="
"$MKAD_BIN" --config "$CONFIG" &
MKAD_PID=$!
trap 'kill $MKAD_PID 2>/dev/null || true' EXIT

echo "=== Warte auf $PROTECTED_IF (Timeout ${TIMEOUT}s) ==="
elapsed=0
while ! ip link show "$PROTECTED_IF" >/dev/null 2>&1; do
  if [ "$elapsed" -ge "$TIMEOUT" ]; then
    echo "FEHLER: $PROTECTED_IF nach ${TIMEOUT}s nicht erschienen — mkad-Log prüfen" >&2
    exit 1
  fi
  sleep 1
  elapsed=$((elapsed + 1))
done

echo "=== $PROTECTED_IF vorhanden ==="
ip macsec show "$PROTECTED_IF" 2>/dev/null || true

echo "=== mkad läuft (PID $MKAD_PID) — acf-can-talker/-bridge jetzt gegen $PROTECTED_IF starten ==="
wait $MKAD_PID
