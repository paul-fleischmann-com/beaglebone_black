#!/usr/bin/env bash
# ARM cross-build: C + Rust + Go
# Runs inside the generic-builder container.
# Paths are container-internal: /src = source, /output = bin output.
set -e

SRC=${SRC:-/src}
OUTPUT=${OUTPUT:-/output}

mkdir -p "$OUTPUT"

echo "=== Build C ==="
arm-linux-gnueabihf-gcc -shared -fPIC \
  --coverage \
  -o "$OUTPUT/libhardware.so" \
  $(ls "$SRC/c/src/"*.c) \
  -I "$SRC/c/include" -lm
find "$SRC/c" -name "*.gcno" -exec cp {} "$OUTPUT/" \; || true

echo "=== Build C executable ==="
arm-linux-gnueabihf-gcc \
  --coverage \
  -o "$OUTPUT/bme280_main" \
  "$SRC/c/test/bbb_smoke.c" \
  -I "$SRC/c/include" \
  -L "$OUTPUT" -lhardware -lm
find "$SRC/c" -name "*.gcno" -exec cp {} "$OUTPUT/" \; || true

echo "=== Build Rust ==="
PKG_CONFIG_ALLOW_CROSS=1 \
PKG_CONFIG_PATH=/usr/lib/arm-linux-gnueabihf/pkgconfig \
cargo build \
  --target armv7-unknown-linux-gnueabihf \
  --release \
  --manifest-path "$SRC/rust-lib/Cargo.toml"

cp "$SRC/rust-lib/target/armv7-unknown-linux-gnueabihf/release/libhardware_rs.so" "$OUTPUT/"
cp "$SRC/rust-lib/target/armv7-unknown-linux-gnueabihf/release/rust_app" "$OUTPUT/"

echo "=== Build Go ==="
GOOS=linux GOARCH=arm GOARM=7 go build -o "$OUTPUT/go_app" "$SRC/go/main.go"

echo "=== Done ==="
ls -l "$OUTPUT"
