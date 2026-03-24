#!/bin/bash
# bausteinsicht-container.sh — run Bausteinsicht via Podman container
# Usage:
#   $0 build               — clone repo and build container image
#   $0 <command> [args...] — run bausteinsicht in the container
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_URL="https://github.com/docToolchain/Bausteinsicht.git"
REPO_DIR="$SCRIPT_DIR/.bausteinsicht-repo"
IMAGE_NAME="bausteinsicht:local"
MODEL="$SCRIPT_DIR/../arch/model/beaglebone_black.jsonc"
MODEL_DIR="$(cd "$(dirname "$MODEL")" && pwd)"
MODEL_IN_CONTAINER="/model/$(basename "$MODEL")"

CMD="${1:-}"

if [[ -z "$CMD" ]]; then
  echo "Usage: $0 build"
  echo "       $0 <command> [args...]"
  echo "Example: $0 build"
  echo "         $0 validate"
  echo "         $0 export --output /output"
  exit 1
fi
shift

if [[ "$CMD" == "build" ]]; then
  # Clone or update repository if not already present
  if [[ ! -d "$REPO_DIR/.git" ]]; then
    echo "Cloning Bausteinsicht repo..."
    git clone --depth 1 "$REPO_URL" "$REPO_DIR"
  else
    echo "Repo already present at $REPO_DIR"
  fi

  # Build container image from Dockerfile in repo
  echo "Building Bausteinsicht container image..."
  podman build -t "$IMAGE_NAME" "$REPO_DIR"
  exit 0
fi

# Run container with model directory mounted (image must be built first)
if ! podman image exists "$IMAGE_NAME"; then
  echo "Error: image '$IMAGE_NAME' not found. Run '$0 build' first." >&2
  exit 1
fi

echo "Running: bausteinsicht $CMD --model $MODEL_IN_CONTAINER $*"
podman run --rm \
  -v "$MODEL_DIR:/model:rw" \
  "$IMAGE_NAME" \
  bausteinsicht "$CMD" --model "$MODEL_IN_CONTAINER" "$@"
