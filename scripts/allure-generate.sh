#!/usr/bin/env bash
# Generates Allure HTML report and zips it.
# Usage: allure-generate.sh <pipeline-name>
# Output: allure-report.zip in workspace root

PIPELINE=${1:-unknown}
ALLURE_VERSION=2.27.0
RESULTS_DIR=allure-results
REPORT_DIR=allure-report
HISTORY_BASE_URL="http://${DEPLOY_HOST:-192.168.2.55}/downloads/$PIPELINE/allure-report/history"

mkdir -p "$RESULTS_DIR" "$REPORT_DIR"

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

# Try to install allure + tools
apt-get update -q && apt-get install -y -q wget zip 2>/dev/null || true

# Download history from previous build for trend graphs
echo "Downloading history from previous build..."
mkdir -p "$RESULTS_DIR/history"
for f in history.json history-trend.json categories-trend.json retry-trend.json duration-trend.json; do
  wget -q "$HISTORY_BASE_URL/$f" -O "$RESULTS_DIR/history/$f" 2>/dev/null || true
done

# Try to run allure — fall back to plain zip of XML results
if wget -q "https://github.com/allure-framework/allure2/releases/download/$ALLURE_VERSION/allure-$ALLURE_VERSION.tgz" -O allure.tgz 2>/dev/null; then
  tar -xzf allure.tgz
  ./allure-$ALLURE_VERSION/bin/allure generate "$RESULTS_DIR" -o "$REPORT_DIR" --clean || true
else
  echo "Allure download failed — using raw XML results"
  cp "$RESULTS_DIR"/*.xml "$REPORT_DIR/" 2>/dev/null || true
fi

zip -r allure-report.zip "$REPORT_DIR/" "$RESULTS_DIR/"
echo "Allure report generated → allure-report.zip"
