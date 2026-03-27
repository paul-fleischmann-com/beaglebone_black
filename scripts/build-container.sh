#!/usr/bin/env bash
# Usage: build-container.sh <image-name> <dockerfile> <context> <version-file>
# Env:   REGISTRY_USER, REGISTRY_TOKEN
set -euo pipefail

IMAGE=$1
DOCKERFILE=$2
CONTEXT=$3
VERSION_FILE=$4

VERSION=$(cat "$VERSION_FILE" | tr -d '[:space:]')
FULL_IMAGE="ghcr.io/$REGISTRY_USER/$IMAGE"

podman login ghcr.io -u "$REGISTRY_USER" -p "$REGISTRY_TOKEN"

echo "--- podman manifest inspect debug ---"
podman manifest inspect "$FULL_IMAGE:$VERSION" || true
echo "--- end debug ---"
if podman pull "$FULL_IMAGE:$VERSION" > /dev/null 2>&1; then
  echo "$IMAGE:$VERSION already exists in ghcr.io — skipping build"
  exit 0
fi
echo "$IMAGE:$VERSION not found in ghcr.io — building ..."

echo "Building $IMAGE:$VERSION ..."
podman build --build-arg VERSION="$VERSION" \
  -t "$FULL_IMAGE:$VERSION" \
  -t "$FULL_IMAGE:latest" \
  -f "$DOCKERFILE" \
  "$CONTEXT"

podman push "$FULL_IMAGE:$VERSION"
podman push "$FULL_IMAGE:latest"
echo "$IMAGE:$VERSION pushed"
