#!/bin/sh
# Save pipeline results to shared volume for centralized reporting.
# Usage: save-pipeline-results.sh <pipeline-name>
# Requires: DRONE_BUILD_NUMBER env var
# Requires: pipeline-results volume mounted at /pipeline-results

PIPELINE=$1
DEST=/pipeline-results/${DRONE_BUILD_NUMBER}/${PIPELINE}

mkdir -p "$DEST"
cp -r .step-status "$DEST/" 2>/dev/null || true
cp -r allure-results "$DEST/" 2>/dev/null || true
cp -r reports "$DEST/" 2>/dev/null || true
printf 'done\n' > "$DEST/indicator"
echo "[$PIPELINE] Results saved for build $DRONE_BUILD_NUMBER"
