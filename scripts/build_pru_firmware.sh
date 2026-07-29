#!/usr/bin/env bash
# Baut die PRU1-RPMsg-GPIO-Firmware (project/pru/fw/pru1_gpio_ctrl). Lädt bei
# Bedarf zuerst die GNU-PRU-Toolchain + PSSP (scripts/setup_pru_toolchain.sh).
# Ausgabe: bin/pru/bbb-pru1-gpio-ctrl.elf. Siehe Issue #252.

set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

PRU_TOOLCHAIN_DIR=${PRU_TOOLCHAIN_DIR:-$REPO_ROOT/toolchain/pru}
FW_DIR="$REPO_ROOT/project/pru/fw/pru1_gpio_ctrl"
OUT_DIR="$REPO_ROOT/bin/pru"

if [ ! -x "$PRU_TOOLCHAIN_DIR/gnupru/pru-elf/bin/pru-gcc" ] || [ ! -d "$PRU_TOOLCHAIN_DIR/pssp/.git" ]; then
  PRU_TOOLCHAIN_DIR="$PRU_TOOLCHAIN_DIR" "$REPO_ROOT/scripts/setup_pru_toolchain.sh"
fi

echo "=== Baue PRU1-Firmware ==="
make -C "$FW_DIR" PRU_TOOLCHAIN_DIR="$PRU_TOOLCHAIN_DIR"

mkdir -p "$OUT_DIR"
cp "$FW_DIR/out/pru1_gpio_ctrl.elf" "$OUT_DIR/bbb-pru1-gpio-ctrl.elf"

echo "=== Fertig: $OUT_DIR/bbb-pru1-gpio-ctrl.elf ==="
