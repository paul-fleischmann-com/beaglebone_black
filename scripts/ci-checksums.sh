#!/usr/bin/env bash
# Generate SHA256 checksums for all files in the bin/ directory.
# Output: bin/checksums.sha256
set -e

BIN_DIR=${BIN_DIR:-bin}

cd "$BIN_DIR"
find . -maxdepth 1 -type f ! -name "checksums.sha256" | sort | xargs sha256sum > checksums.sha256
echo "=== checksums.sha256 ==="
cat checksums.sha256
