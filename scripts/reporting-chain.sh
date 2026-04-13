#!/bin/bash
# Reporting chain: generate-junit → allure-generate → publish-allure
# Replaces three separate pipeline steps with one combined step.
# Usage: reporting-chain.sh <pipeline-name> <step1> [step2 ...]
# Requires: DEPLOY_HOST env var (from Drone secret deploy_host)
# Requires: www-downloads volume mounted at /var/www/downloads

set -e

PIPELINE=$1
shift

sh scripts/generate-junit.sh "$PIPELINE" "$@"
bash scripts/allure-generate.sh "$PIPELINE"
echo "Allure Report http://${DEPLOY_HOST}/downloads/$PIPELINE/allure-report/index.html"
make publish-allure PIPELINE="$PIPELINE"
