#!/usr/bin/env bash
# Baut das Open1722-ACF-CAN-Kernel-Modul NATIV gegen den exakt laufenden
# Kernel des Build-Hosts (linux-headers-$(uname -r)) — anders als
# scripts/ci_check_acfcan_compile.sh (host-unabhängiger reiner Compile-
# Check, Issue #271) MUSS dieses Modul auf demselben Host per insmod
# tatsächlich ladbar sein: tests/integration/test_e2e_local.py (#271) lädt
# es dort funktional. Kernel-Module müssen exakt zum laufenden Kernel
# passen (Vermagic-Check) — das lässt sich nicht entkoppeln, auch nicht
# durch einen Container-Build (Container teilen sich den Host-Kernel).
#
# Voraussetzung: der Build-Host hat für seinen laufenden Kernel
# (uname -r) ein passendes linux-headers-Paket im apt-Archiv. Bei einem
# Kernel-Upgrade ohne Reboot (uname -r zeigt die ALTE Version, apt bietet
# nur noch Headers für die NEUE) schlägt dieses Skript bewusst fehl statt
# ein falsches/nicht ladbares Modul zu bauen — dann hilft nur
# `apt-get install linux-image-amd64 linux-headers-amd64 && reboot`
# auf dem Host selbst (siehe #271-Diskussion).
#
# Ausgabe: bin/kernel/acfcan-native.ko

set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OPEN1722_DIR=${OPEN1722_DIR:-$REPO_ROOT/toolchain/open1722}
MOD_DIR="$OPEN1722_DIR/examples/acf-can/linux-kernel-mod"
OUT_DIR="$REPO_ROOT/bin/kernel"

if [ ! -d "$OPEN1722_DIR/.git" ]; then
  "$REPO_ROOT/scripts/setup_open1722.sh"
fi

if ! [ -d "/lib/modules/$(uname -r)/build" ]; then
  echo "=== Installiere Kernel-Headers für $(uname -r) ==="
  apt-get update -qq
  apt-get install -y -qq "linux-headers-$(uname -r)" build-essential
fi

# Upstreams eigenes Makefile hat kein KDIR-Argument (die `all:`-Regel baut
# hart gegen /lib/modules/$(uname -r)/build) — deshalb wird hier bewusst
# nicht `make all` aufgerufen, sondern das Modulverzeichnis direkt als
# externes Kbuild-Modul gebaut (Standard-Kbuild-Aufruf
# `-C <kernel-tree> M=<moduldir>`), analog zu build_open1722_acfcan.sh /
# ci_check_acfcan_compile.sh.
echo "=== Nativer Build: acfcan-Kernel-Modul gegen $(uname -r) (muss hier per insmod ladbar sein) ==="
make -C "/lib/modules/$(uname -r)/build" M="$MOD_DIR" CONFIG_ACF_CAN=m modules

mkdir -p "$OUT_DIR"
cp "$MOD_DIR/acfcan.ko" "$OUT_DIR/acfcan-native.ko"

echo "=== Fertig: $OUT_DIR/acfcan-native.ko ==="
