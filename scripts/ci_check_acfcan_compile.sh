#!/usr/bin/env bash
# Schneller, HOST-KERNEL-UNABHÄNGIGER Compile-Check des Open1722-ACF-CAN-
# Kernel-Moduls in CI: baut es NATIV gegen ein generisches, aktuelles
# Debian-Headers-Paket (linux-headers-amd64) — bewusst NICHT gegen den
# exakten Kernel des CI-Runner-Hosts (linux-headers-$(uname -r)). Zweck ist
# ausschließlich ein schneller Signal-Check, ob sich der C-Code noch gegen
# eine aktuelle Linux-Kernel-API kompilieren lässt — keine funktionale
# Ladbarkeits-Prüfung, kein Zielarchitektur-Build.
#
# Vorher hing dieser Check am exakten Runner-Host-Kernel (uname -r) — das
# hat wiederholt zu False-Negatives geführt, wenn der Runner ein
# Kernel-Upgrade per apt bekam, aber noch nicht rebootet war (uname -r
# zeigt dann die alte Version, für die es im apt-Archiv keine Headers mehr
# gibt). Reine Host-Wartung sollte dieses Signal nicht rot machen, siehe
# Issue #271.
#
# Für ein tatsächlich per insmod ladbares, zum Runner-Host passendes
# acfcan.ko siehe stattdessen scripts/build_acfcan_native.sh (verwendet von
# tests/integration/test_e2e_local.py, #271) — das MUSS exakt zum laufenden
# Host-Kernel passen (Kernel-Modul-Vermagic-Check), lässt sich nicht
# entkoppeln, auch nicht durch Container (die teilen sich den Host-Kernel).
#
# Auch nicht gegen den echten BeagleBone-Black-Yocto-Kernel (das übernimmt
# bereits die build-yocto-image-Pipeline via bitbake, seit acfcan-mod Teil
# von bbb-full-image ist, siehe Issue #256).
#
# Upstreams eigenes Makefile (obj-$(CONFIG_ACF_CAN) += acfcan.o) hat kein
# KDIR-Argument — die `all:`-Regel baut hart gegen
# /lib/modules/$(uname -r)/build. Deshalb wird hier bewusst nicht `make all`
# aufgerufen, sondern das Modulverzeichnis direkt als externes Kbuild-Modul
# gegen das zuvor ermittelte $KDIR gebaut (Standard-Kbuild-Aufruf
# `-C <kernel-tree> M=<moduldir>`), analog zu build_open1722_acfcan.sh.

set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OPEN1722_DIR=${OPEN1722_DIR:-$REPO_ROOT/toolchain/open1722}
MOD_DIR="$OPEN1722_DIR/examples/acf-can/linux-kernel-mod"

if [ ! -d "$OPEN1722_DIR/.git" ]; then
  "$REPO_ROOT/scripts/setup_open1722.sh"
fi

echo "=== Installiere generische Kernel-Headers (linux-headers-amd64) ==="
apt-get update -qq
apt-get install -y -qq linux-headers-amd64 build-essential

KDIR=$(ls -d /lib/modules/*/build 2>/dev/null | head -1)
if [ -z "$KDIR" ]; then
  echo "FEHLER: kein /lib/modules/*/build nach Installation von linux-headers-amd64 gefunden" >&2
  exit 1
fi

echo "=== Nativer Compile-Check: acfcan-Kernel-Modul gegen $KDIR (unabhängig vom Runner-Host-Kernel) ==="
make -C "$KDIR" M="$MOD_DIR" CONFIG_ACF_CAN=m modules

echo "=== Fertig: $MOD_DIR/acfcan.ko ==="
