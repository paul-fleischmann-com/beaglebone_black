#!/usr/bin/env bash
# Lädt COVESA/Open1722 (BSD-3-Clause), Referenzimplementierung von IEEE 1722
# (AVTP/ACF), für den ACF-CAN-Kernel-Modul-Build
# (scripts/build_open1722_acfcan.sh, Issue #256) und die User-Space-Demo-Tools
# (scripts/build_open1722_userspace.sh, Issue #257).
# Idempotent: überspringt einen bereits vorhandenen Checkout, damit das Script
# lokal und in CI wiederverwendbar ist.

set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

OPEN1722_DIR=${OPEN1722_DIR:-$REPO_ROOT/toolchain/open1722}
OPEN1722_URL=${OPEN1722_URL:-https://github.com/COVESA/Open1722.git}
# Pinned auf den zum Zeitpunkt der Recherche aktuellen main-Commit — bewusst
# nicht "main" direkt, damit ein Upstream-Breaking-Change (Open1722 ist laut
# eigenem README "in active development") nicht unbemerkt den Build bricht.
OPEN1722_REV=${OPEN1722_REV:-8535cfd63da7a71ec1169d122b2c6d081b28e75b}

if [ -d "$OPEN1722_DIR/.git" ]; then
  echo "=== Open1722 bereits vorhanden, überspringe Clone ==="
else
  echo "=== Klone Open1722 ($OPEN1722_REV) ==="
  git clone "$OPEN1722_URL" "$OPEN1722_DIR"
fi

CURRENT_REV="$(git -C "$OPEN1722_DIR" rev-parse HEAD)"
if [ "$CURRENT_REV" != "$OPEN1722_REV" ]; then
  echo "=== Checke Open1722 auf $OPEN1722_REV aus ==="
  git -C "$OPEN1722_DIR" fetch --depth 1 origin "$OPEN1722_REV"
  # --force verwirft evtl. vorher hier angewendete lokale Patches (siehe
  # unten) — die werden nach dem Checkout ohnehin frisch neu angewendet,
  # ein Rev-Bump soll aber nie an einem stehengebliebenen Patch scheitern.
  git -C "$OPEN1722_DIR" checkout --force --detach "$OPEN1722_REV"
fi

# Lokale Patches auf bekannte Open1722-Bugs (siehe scripts/patches/*.patch) —
# idempotent per grep-Marker, damit ein erneuter Lauf (Checkout oben
# übersprungen, Datei bereits gepatcht) den Patch nicht ein zweites Mal
# anzuwenden versucht (git apply würde dann fehlschlagen).
ACFCAN_MAIN="$OPEN1722_DIR/examples/acf-can/linux-kernel-mod/acfcanmain.c"
if [ -f "$ACFCAN_MAIN" ] && ! grep -q "KERNEL_VERSION(6, 15, 0)" "$ACFCAN_MAIN"; then
  echo "=== Wende Patch an: rtnl_newlink_params-Versions-Guard-Fix (Issue #278) ==="
  git -C "$OPEN1722_DIR" apply "$REPO_ROOT/scripts/patches/open1722-fix-rtnl-newlink-version-guard.patch"
fi

echo "=== Fertig. ==="
echo "OPEN1722_DIR=$OPEN1722_DIR"
