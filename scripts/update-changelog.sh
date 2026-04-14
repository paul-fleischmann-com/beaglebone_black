#!/bin/sh
# Download git-cliff, generate changelog and commit if changed.
set -e

GIT_CLIFF_VERSION="2.6.1"
TARBALL="git-cliff-${GIT_CLIFF_VERSION}-x86_64-unknown-linux-musl.tar.gz"
URL="https://github.com/orhun/git-cliff/releases/download/v${GIT_CLIFF_VERSION}/${TARBALL}"

apk add --no-cache curl tar make ca-certificates

echo "Downloading git-cliff ${GIT_CLIFF_VERSION}..."
curl -sSfL "$URL" | tar -xz -C /tmp
find /tmp -name "git-cliff" -type f -exec mv {} /usr/local/bin/ \;
chmod +x /usr/local/bin/git-cliff
git-cliff --version

git-cliff --unreleased --output unreleased.md
make prepend-changelog

sh scripts/ci-git-setup.sh
git add CHANGELOG.md
if git diff --cached --quiet; then
  echo "Keine Changelog-Änderungen"
else
  git commit -m "docs(changelog): update unreleased section [skip ci]"
fi
