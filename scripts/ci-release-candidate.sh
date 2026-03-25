#!/usr/bin/env bash
# Create (or re-create) a toTestOnTarget pre-release on GitHub.
# Required env vars: VERSION (e.g. 1.1.0), GH_TOKEN
# Optional env vars: BIN_DIR (default: bin)
set -e

VERSION=${VERSION:-$(make version)}
BIN_DIR=${BIN_DIR:-bin}
TAG="v${VERSION}-toTestOnTarget"

echo "=== Release Candidate: $TAG ==="

# Delete any existing pre-release with the same tag
gh release delete "$TAG" --yes 2>/dev/null || true
git push origin --delete "$TAG" 2>/dev/null || true

# Extract release notes from CHANGELOG.md for this version
awk "/^## \[${VERSION}\]/{found=1; next} found && /^## \[/{exit} found{print}" \
  CHANGELOG.md > release_notes.md \
  || echo "Release candidate for v${VERSION}" > release_notes.md

gh release create "$TAG" \
  --title "v${VERSION} — Release Candidate" \
  --notes-file release_notes.md \
  --prerelease \
  "$BIN_DIR"/bbcli-* \
  "$BIN_DIR"/bbtui-* \
  "$BIN_DIR"/checksums.sha256

rm -f release_notes.md
echo "✅ Release candidate created: $TAG"
