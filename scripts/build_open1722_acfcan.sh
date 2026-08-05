#!/usr/bin/env bash
# Cross-kompiliert das Open1722-ACF-CAN-Kernel-Modul
# (examples/acf-can/linux-kernel-mod, obj-$(CONFIG_ACF_CAN) += acfcan.o) gegen
# einen Yocto-Kernel-Quellbaum. Lädt bei Bedarf zuerst Open1722
# (scripts/setup_open1722.sh). Ausgabe: bin/kernel/bbb-acfcan.ko. Siehe Issue #256.
#
# Voraussetzung: KERNEL_SRC zeigt auf einen konfigurierten Yocto-Kernel-
# Quellbaum (z. B. tmp/work-shared/beaglebone-yocto/kernel-source nach einem
# `make yocto-image`-Lauf) — exakt dieselbe Kernel-Version/-Konfiguration wie
# auf dem Zielsystem, sonst schlägt das spätere Laden mit einem
# Versions-Mismatch fehl (siehe project/kernel-modul-von-grund-auf-Post).
#
# Hinweis zur Cross-Compilation: das Open1722-eigene Makefile hat kein
# KDIR-Argument (die Upstream-`all:`-Regel baut hart gegen
# `/lib/modules/$(uname -r)/build`, den *laufenden* Kernel des Build-Hosts).
# Für den Cross-Build wird deshalb bewusst nicht `make all` aufgerufen,
# sondern das Modulverzeichnis direkt als externes Kbuild-Modul gegen
# $KERNEL_SRC gebaut (Standard-Kbuild-Aufruf `-C <kernel-tree> M=<moduldir>`),
# mit demselben arm-linux-gnueabihf-Cross-Compiler wie der Rest des Projekts
# (siehe CROSS in Makefile).

set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

OPEN1722_DIR=${OPEN1722_DIR:-$REPO_ROOT/toolchain/open1722}
CROSS=${CROSS:-arm-linux-gnueabihf-}
OUT_DIR="$REPO_ROOT/bin/kernel"
MOD_DIR="$OPEN1722_DIR/examples/acf-can/linux-kernel-mod"

if [ -z "$KERNEL_SRC" ]; then
  echo "FEHLER: KERNEL_SRC ist nicht gesetzt (Pfad zum Yocto-Kernel-Quellbaum, z.B." >&2
  echo "        tmp/work-shared/beaglebone-yocto/kernel-source nach 'make yocto-image')." >&2
  exit 1
fi

# Immer aufrufen, nicht nur wenn $OPEN1722_DIR/.git fehlt — siehe
# ci_check_acfcan_compile.sh für die Begründung (Issue #278: lokale Patches
# blieben bei warmem Cache sonst dauerhaft unangewendet).
OPEN1722_DIR="$OPEN1722_DIR" "$REPO_ROOT/scripts/setup_open1722.sh"

echo "=== Baue Open1722-ACF-CAN-Kernel-Modul gegen $KERNEL_SRC ==="
make -C "$KERNEL_SRC" M="$MOD_DIR" ARCH=arm CROSS_COMPILE="$CROSS" \
  CONFIG_ACF_CAN=m modules

mkdir -p "$OUT_DIR"
cp "$MOD_DIR/acfcan.ko" "$OUT_DIR/bbb-acfcan.ko"

echo "=== Fertig: $OUT_DIR/bbb-acfcan.ko ==="
