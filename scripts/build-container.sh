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
  SECRET_ARGS="--secret id=git_token,env=REGISTRY_TOKEN"
fi
podman build --build-arg VERSION="$VERSION" \
  $SECRET_ARGS \
  -t "$FULL_IMAGE:$VERSION" \
  -t "$FULL_IMAGE:latest" \
  -f "$DOCKERFILE" \
  "$CONTEXT"

podman push "$FULL_IMAGE:$VERSION"
podman push "$FULL_IMAGE:latest"
echo "$IMAGE:$VERSION pushed"
