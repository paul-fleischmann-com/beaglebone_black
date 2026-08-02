#!/usr/bin/env bash
# Cross-kompiliert die Open1722-User-Space-Beispielprogramme (CMake-Target
# "examples", EXCLUDE_FROM_ALL): acf-can-talker/-listener/-bridge und
# cvf-talker/-listener. Lädt bei Bedarf zuerst Open1722
# (scripts/setup_open1722.sh). Ausgabe: bin/open1722/{acf-can-talker,...}.
# Siehe Issue #257.

set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

OPEN1722_DIR=${OPEN1722_DIR:-$REPO_ROOT/toolchain/open1722}
CROSS=${CROSS:-arm-linux-gnueabihf-}
BUILD_DIR="$OPEN1722_DIR/build-arm"
OUT_DIR="$REPO_ROOT/bin/open1722"

BINARIES="acf-can-talker acf-can-listener acf-can-bridge cvf-talker cvf-listener"

if [ ! -d "$OPEN1722_DIR/.git" ]; then
  OPEN1722_DIR="$OPEN1722_DIR" "$REPO_ROOT/scripts/setup_open1722.sh"
fi

echo "=== Konfiguriere Open1722-User-Space-Build (CMake, Cross arm-linux-gnueabihf) ==="
cmake -S "$OPEN1722_DIR" -B "$BUILD_DIR" \
  -DCMAKE_SYSTEM_NAME=Linux \
  -DCMAKE_SYSTEM_PROCESSOR=arm \
  -DCMAKE_C_COMPILER="${CROSS}gcc" \
  -DCMAKE_CXX_COMPILER="${CROSS}g++" \
  -DCMAKE_BUILD_TYPE=Release

echo "=== Baue Open1722 examples-Target ==="
cmake --build "$BUILD_DIR" --target examples -- -j"$(nproc)"

mkdir -p "$OUT_DIR"
for bin in $BINARIES; do
  found="$(find "$BUILD_DIR/examples" -maxdepth 3 -name "$bin" -type f | head -1)"
  if [ -z "$found" ]; then
    echo "FEHLER: $bin nicht im Build-Verzeichnis gefunden" >&2
    exit 1
  fi
  cp "$found" "$OUT_DIR/$bin"
done

echo "=== Fertig: $OUT_DIR/{$(echo "$BINARIES" | tr ' ' ',')} ==="
