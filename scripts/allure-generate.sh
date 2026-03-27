#!/usr/bin/env bash
# Generates Allure HTML report and zips it.
# Usage: allure-generate.sh <pipeline-name>
# Output: allure-report.zip in workspace root
set -euo pipefail

PIPELINE=${1:-unknown}
ALLURE_VERSION=2.27.0
RESULTS_DIR=allure-results
REPORT_DIR=allure-report

apt-get update -q && apt-get install -y -q wget zip 2>/dev/null

wget -q "https://github.com/allure-framework/allure2/releases/download/$ALLURE_VERSION/allure-$ALLURE_VERSION.tgz" -O allure.tgz
tar -xzf allure.tgz

mkdir -p "$RESULTS_DIR"

# Copy any JUnit XML from reports/ into allure-results/
find reports/ -name "*.xml" -exec cp {} "$RESULTS_DIR/" \; 2>/dev/null || true

# If no XML found, write a synthetic "pipeline complete" result
if [ -z "$(ls -A $RESULTS_DIR 2>/dev/null)" ]; then
  cat > "$RESULTS_DIR/pipeline-result.xml" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<testsuites>
  <testsuite name="$PIPELINE" tests="1" failures="0">
    <testcase name="Pipeline completed" classname="pipeline"/>
  </testsuite>
</testsuites>
EOF
fi

./allure-$ALLURE_VERSION/bin/allure generate "$RESULTS_DIR" -o "$REPORT_DIR" --clean

zip -r allure-report.zip "$REPORT_DIR/"
echo "Allure report generated → allure-report.zip"
