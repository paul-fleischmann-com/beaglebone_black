#!/bin/bash
# Check indicator file and run reporting chain for a pipeline.
# Usage: report-pipeline.sh <pipeline-name> <step1> [step2 ...]
# Requires: DRONE_BUILD_NUMBER, DEPLOY_HOST env vars
# Requires: pipeline-results volume mounted at /pipeline-results
# Requires: www-downloads volume mounted at /var/www/downloads

set -e

PIPELINE=$1
shift

RESULTS_DIR="/pipeline-results/${DRONE_BUILD_NUMBER}/${PIPELINE}"

if [ ! -f "$RESULTS_DIR/indicator" ]; then
  echo "[$PIPELINE] Pipeline did not run in build $DRONE_BUILD_NUMBER — skipping."
  exit 0
fi

echo "[$PIPELINE] Restoring results from build $DRONE_BUILD_NUMBER..."
cp -r "$RESULTS_DIR/.step-status" .step-status 2>/dev/null || true
cp -r "$RESULTS_DIR/allure-results" allure-results 2>/dev/null || true
cp -r "$RESULTS_DIR/reports" reports 2>/dev/null || true

apt-get update -q && apt-get install -y --no-install-recommends make unzip -q

echo "[$PIPELINE] Running reporting chain..."
bash scripts/reporting-chain.sh "$PIPELINE" "$@"
