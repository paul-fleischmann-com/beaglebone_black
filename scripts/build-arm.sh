#!/usr/bin/env bash
# ARM cross-build: C + Rust + Go
# Runs inside the generic-builder container.
# /src = repo root (source_dir: .), /output = bin output.

SRC=${SRC:-/src}
OUTPUT=${OUTPUT:-/output}
PROJECT=${PROJECT:-$SRC/project}
JUNIT=${JUNIT:-$SRC/reports/build-libraries-junit.xml}

mkdir -p "$OUTPUT" "$(dirname "$JUNIT")"

# --- helpers -------------------------------------------------------
FAILURES=0
declare -a RESULTS  # "name|status|message"

run_step() {
  local name="$1"; shift
  echo "=== $name ==="
  local out
  out=$("$@" 2>&1) && rc=0 || rc=$?
  echo "$out"
  if [ $rc -eq 0 ]; then
    RESULTS+=("$name|pass|")
  else
    RESULTS+=("$name|fail|$(echo "$out" | tail -5 | sed 's/&/\&amp;/g;s/</\&lt;/g;s/>/\&gt;/g')")
    FAILURES=$((FAILURES + 1))
  fi
}

# --- build steps ---------------------------------------------------
run_step "Build C Library" \
  arm-linux-gnueabihf-gcc -shared -fPIC --coverage \
    -o "$OUTPUT/libhardware.so" \
    $(ls "$PROJECT/c/src/"*.c) \
    -I "$PROJECT/c/include" -lm

find "$PROJECT/c" -name "*.gcno" -exec cp {} "$OUTPUT/" \; || true

run_step "Build C Executable" \
  arm-linux-gnueabihf-gcc --coverage \
    -o "$OUTPUT/bme280_main" \
    "$PROJECT/c/test/bbb_smoke.c" \
    -I "$PROJECT/c/include" \
    -L "$OUTPUT" -lhardware -lm

find "$PROJECT/c" -name "*.gcno" -exec cp {} "$OUTPUT/" \; || true

run_step "Build Rust Library" \
  env PKG_CONFIG_ALLOW_CROSS=1 \
    PKG_CONFIG_PATH=/usr/lib/arm-linux-gnueabihf/pkgconfig \
    cargo build \
      --target armv7-unknown-linux-gnueabihf \
      --release \
      --manifest-path "$PROJECT/rust-lib/Cargo.toml"

if [ -f "$PROJECT/rust-lib/target/armv7-unknown-linux-gnueabihf/release/libhardware_rs.so" ]; then
  cp "$PROJECT/rust-lib/target/armv7-unknown-linux-gnueabihf/release/libhardware_rs.so" "$OUTPUT/"
  cp "$PROJECT/rust-lib/target/armv7-unknown-linux-gnueabihf/release/rust_app" "$OUTPUT/"
fi

run_step "Build Go API" \
  env GOOS=linux GOARCH=arm GOARM=7 \
    go build -o "$OUTPUT/go_app" "$PROJECT/go/main.go"

# --- write JUnit XML -----------------------------------------------
echo "=== Writing JUnit XML → $JUNIT ==="
{
  echo '<?xml version="1.0" encoding="UTF-8"?>'
  echo "<testsuites>"
  echo "  <testsuite name=\"build-libraries\" tests=\"${#RESULTS[@]}\" failures=\"$FAILURES\">"
  for entry in "${RESULTS[@]}"; do
    IFS='|' read -r name status msg <<< "$entry"
    if [ "$status" = "pass" ]; then
      echo "    <testcase name=\"$name\" classname=\"build\"/>"
    else
      echo "    <testcase name=\"$name\" classname=\"build\">"
      echo "      <failure message=\"Build failed\">$msg</failure>"
      echo "    </testcase>"
    fi
  done
  echo "  </testsuite>"
  echo "</testsuites>"
} > "$JUNIT"

echo "=== Done ==="
ls -l "$OUTPUT"

[ $FAILURES -eq 0 ] || exit 1
