#!/usr/bin/env bash
# Schneller Compile-Check des Open1722-ACF-CAN-Kernel-Moduls in CI: baut es
# NATIV (Open1722s unveränderte examples/acf-can/linux-kernel-mod/Makefile,
# `make -C /lib/modules/$(uname -r)/build M=$(pwd) modules`) gegen die im
# CI-Container laufende Kernel-Version — nicht gegen den echten
# BeagleBone-Black-Yocto-Kernel (das übernimmt bereits die
# build-yocto-image-Pipeline via bitbake, seit acfcan-mod Teil von
# bbb-full-image ist, siehe Issue #256). Zweck hier ist ausschließlich ein
# schneller Signal-Check, ob sich der C-Code noch gegen eine aktuelle
# Linux-Kernel-API kompilieren lässt — kein funktionaler Test, kein
# Zielarchitektur-Build.

set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OPEN1722_DIR=${OPEN1722_DIR:-$REPO_ROOT/toolchain/open1722}
MOD_DIR="$OPEN1722_DIR/examples/acf-can/linux-kernel-mod"

if [ ! -d "$OPEN1722_DIR/.git" ]; then
  "$REPO_ROOT/scripts/setup_open1722.sh"
fi

if ! [ -d "/lib/modules/$(uname -r)/build" ]; then
  echo "=== Installiere Kernel-Headers für $(uname -r) ==="
  apt-get update -qq
  apt-get install -y -qq "linux-headers-$(uname -r)" build-essential
fi

echo "=== Nativer Compile-Check: acfcan-Kernel-Modul gegen $(uname -r) ==="
CONFIG_ACF_CAN=m make -C "$MOD_DIR"

echo "=== Fertig: $MOD_DIR/acfcan.ko ==="
