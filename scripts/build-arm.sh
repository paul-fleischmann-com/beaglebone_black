#!/usr/bin/env bash
# ARM cross-build: C + Rust + Go
# Runs inside the generic-builder container.
# /src = repo root (source_dir: .), /output = bin output.
set -e

SRC=${SRC:-/src}
OUTPUT=${OUTPUT:-/output}
PROJECT=${PROJECT:-$SRC/project}

mkdir -p "$OUTPUT"

echo "=== Build C ==="
arm-linux-gnueabihf-gcc -shared -fPIC \
  --coverage \
  -o "$OUTPUT/libhardware.so" \
  $(ls "$PROJECT/c/src/"*.c) \
  -I "$PROJECT/c/include" -lm
find "$PROJECT/c" -name "*.gcno" -exec cp {} "$OUTPUT/" \; || true

echo "=== Build C executable ==="
arm-linux-gnueabihf-gcc \
  --coverage \
  -o "$OUTPUT/bme280_main" \
  "$PROJECT/c/test/bbb_smoke.c" \
  -I "$PROJECT/c/include" \
  -L "$OUTPUT" -lhardware -lm
find "$PROJECT/c" -name "*.gcno" -exec cp {} "$OUTPUT/" \; || true

echo "=== Build Rust ==="
PKG_CONFIG_ALLOW_CROSS=1 \
PKG_CONFIG_PATH=/usr/lib/arm-linux-gnueabihf/pkgconfig \
cargo build \
  --target armv7-unknown-linux-gnueabihf \
  --release \
  --manifest-path "$PROJECT/rust-lib/Cargo.toml"

cp "$PROJECT/rust-lib/target/armv7-unknown-linux-gnueabihf/release/libhardware_rs.so" "$OUTPUT/"
cp "$PROJECT/rust-lib/target/armv7-unknown-linux-gnueabihf/release/rust_app" "$OUTPUT/"

echo "=== Build Go ==="
GOOS=linux GOARCH=arm GOARM=7 go build -o "$OUTPUT/go_app" "$PROJECT/go/main.go"

echo "=== Done ==="
ls -l "$OUTPUT"
