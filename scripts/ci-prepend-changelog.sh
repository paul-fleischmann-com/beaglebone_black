#!/bin/sh
# Prepend an unreleased.md section to CHANGELOG.md.
# Used by the CI changelog job after git-cliff generates unreleased.md.
set -e

if [ -s unreleased.md ]; then
  cat unreleased.md CHANGELOG.md > CHANGELOG.md.tmp
  mv CHANGELOG.md.tmp CHANGELOG.md
  rm unreleased.md
  echo "✅ Changelog updated"
else
  echo "No unreleased changes — nothing to prepend"
fi
