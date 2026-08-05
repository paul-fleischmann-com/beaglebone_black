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

if [ -z "${REGISTRY_USER:-}" ] || [ -z "${REGISTRY_TOKEN:-}" ]; then
  echo "ERROR: REGISTRY_USER oder REGISTRY_TOKEN nicht gesetzt (Drone Secrets prüfen: registry_user, Bau_token)"
  exit 1
fi
printf '%s' "$REGISTRY_TOKEN" | podman login ghcr.io -u "$REGISTRY_USER" --password-stdin

INSPECT=$(podman manifest inspect "$FULL_IMAGE:$VERSION" 2>&1 || true)
if echo "$INSPECT" | grep -q 'schemaVersion'; then
  echo "$IMAGE:$VERSION already exists in ghcr.io — skipping build"
  exit 0
fi
echo "$IMAGE:$VERSION not found in ghcr.io — building ..."


echo "Building $IMAGE:$VERSION ..."
SECRET_ARGS=""
if [ -n "${REGISTRY_TOKEN:-}" ]; then
  echo -n "$REGISTRY_TOKEN" > /tmp/bau_token
  SECRET_ARGS="--secret id=Bau_token,src=/tmp/bau_token"
fi

# For the bausteinsicht image: read the required Go version from upstream go.mod
# so the builder stage always matches what Bausteinsicht declares. Reads from
# the SAME pinned tag as BAUSTEINSICHT_REV in docker/bausteinsicht/Dockerfile
# (not "main") — otherwise the pin only covers the cloned source, not the Go
# toolchain selection, and an unrelated upstream main-branch bump could still
# break this build. Keep both in sync when bumping the pin.
GO_VERSION_ARG=""
if [[ "$IMAGE" == "bausteinsicht" ]]; then
  GO_MOD_URL="https://raw.githubusercontent.com/docToolchain/Bausteinsicht/v1.2.1/go.mod"
  GO_VERSION=$(curl -fsSL "$GO_MOD_URL" | grep -E '^go ' | awk '{print $2}' | cut -d. -f1,2)
  if [[ -n "$GO_VERSION" ]]; then
    echo "Detected Go version from Bausteinsicht go.mod: $GO_VERSION"
    GO_VERSION_ARG="--build-arg GO_VERSION=$GO_VERSION"
  fi
fi

podman build --build-arg VERSION="$VERSION" \
  $GO_VERSION_ARG \
  $SECRET_ARGS \
  -t "$FULL_IMAGE:$VERSION" \
  -t "$FULL_IMAGE:latest" \
  -f "$DOCKERFILE" \
  "$CONTEXT"

podman push "$FULL_IMAGE:$VERSION"
podman push "$FULL_IMAGE:latest"
rm -f /tmp/bau_token
echo "$IMAGE:$VERSION pushed"
