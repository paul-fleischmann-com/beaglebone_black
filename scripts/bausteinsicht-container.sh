#!/bin/bash
# bausteinsicht-container.sh — run Bausteinsicht container (robust version)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_URL="https://github.com/docToolchain/Bausteinsicht.git"
REPO_DIR="$SCRIPT_DIR/.bausteinsicht-repo"

# Prefer Docker, fallback to Podman if explicitly desired
RUNTIME="${RUNTIME:-docker}"

# Allow override for CI images
IMAGE_NAME="${IMAGE_NAME:-ghcr.io/paulefl/bausteinsicht:latest}"

MODEL="$SCRIPT_DIR/../arch/model/beaglebone_black.jsonc"
MODEL_DIR="$(cd "$(dirname "$MODEL")" && pwd)"
MODEL_IN_CONTAINER="/model/$(basename "$MODEL")"

CMD="${1:-}"

if [[ -z "$CMD" ]]; then
  echo "Usage:"
  echo "  $0 build"
  echo "  $0 <command> [args...]"
  echo ""
  echo "Env overrides:"
  echo "  RUNTIME=docker|podman"
  echo "  IMAGE_NAME=..."
  exit 1
fi

shift || true

# -------------------------
# BUILD (disabled / optional)
# -------------------------
if [[ "$CMD" == "build" ]]; then
  echo "⚠️  Local container build is disabled in this environment."
  echo "👉 Use CI pipeline or prebuilt image (GHCR)."
  exit 0
fi

# -------------------------
# Ensure image exists
# -------------------------
if ! $RUNTIME image inspect "$IMAGE_NAME" >/dev/null 2>&1; then
  echo "Error: image '$IMAGE_NAME' not found."
  echo "👉 Run CI build or pull remote image first."
  exit 1
fi

# -------------------------
# Run command
# -------------------------
echo "Running: bausteinsicht $CMD --model $MODEL_IN_CONTAINER $*"

$RUNTIME run --rm \
  -v "$MODEL_DIR:/model:rw" \
  "$IMAGE_NAME" \
  bausteinsicht "$CMD" --model "$MODEL_IN_CONTAINER" "$@"