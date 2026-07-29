#!/usr/bin/env bash
# Lädt die GNU-PRU-Toolchain (dinuxbg/gnupru) sowie die GCC-kompatible
# pru-software-support-package (PSSP) für den PRU-ICSS-Firmware-Build.
# Idempotent: überspringt bereits vorhandene Downloads/Clones, damit das
# Script lokal und in CI wiederverwendbar ist. Siehe Issue #252.

set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

PRU_TOOLCHAIN_DIR=${PRU_TOOLCHAIN_DIR:-$REPO_ROOT/toolchain/pru}
GNUPRU_VERSION=${GNUPRU_VERSION:-2026.05}
GNUPRU_ARCH=${GNUPRU_ARCH:-amd64}
GNUPRU_URL=${GNUPRU_URL:-https://github.com/dinuxbg/gnupru/releases/download/$GNUPRU_VERSION/pru-elf-$GNUPRU_VERSION.$GNUPRU_ARCH.tar.xz}
PSSP_URL=${PSSP_URL:-https://github.com/dinuxbg/pru-software-support-package.git}
PSSP_BRANCH=${PSSP_BRANCH:-master}

GNUPRU_DIR="$PRU_TOOLCHAIN_DIR/gnupru"
PSSP_DIR="$PRU_TOOLCHAIN_DIR/pssp"

mkdir -p "$PRU_TOOLCHAIN_DIR"

if [ -x "$GNUPRU_DIR/pru-elf/bin/pru-gcc" ]; then
  echo "=== GNU-PRU-Toolchain bereits vorhanden, überspringe Download ==="
else
  echo "=== Lade GNU-PRU-Toolchain ($GNUPRU_VERSION, $GNUPRU_ARCH) ==="
  mkdir -p "$GNUPRU_DIR"
  tmp_tar="$PRU_TOOLCHAIN_DIR/pru-elf.tar.xz"
  curl -fsSL -o "$tmp_tar" "$GNUPRU_URL"
  tar xf "$tmp_tar" -C "$GNUPRU_DIR"
  rm -f "$tmp_tar"
fi

if [ -d "$PSSP_DIR/.git" ]; then
  echo "=== pru-software-support-package bereits vorhanden, überspringe Clone ==="
else
  echo "=== Klone pru-software-support-package ($PSSP_BRANCH) ==="
  git clone --depth 1 -b "$PSSP_BRANCH" "$PSSP_URL" "$PSSP_DIR"
fi

echo "=== Fertig. ==="
echo "PRU_GCC_BIN=$GNUPRU_DIR/pru-elf/bin"
echo "PSSP_DIR=$PSSP_DIR"
