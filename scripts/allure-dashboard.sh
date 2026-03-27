#!/usr/bin/env bash
# Downloads allure-results from all pipelines and generates a combined dashboard report.
# Usage: allure-dashboard.sh
# Output: allure-dashboard.zip in workspace root

ALLURE_VERSION=2.27.0
BASE_URL="http://192.168.2.55/downloads"
MERGED_DIR=allure-results-dashboard
REPORT_DIR=allure-report-dashboard
HISTORY_URL="$BASE_URL/dashboard/allure-report-dashboard/history"

PIPELINES="1-libraries 2-embedded-sw 3-tools 4-webapp 5-release 6-nightly 7-reports 8-bausteinsicht 9-build-container 10-integration-tests 11-version-bump 12-changelog"

apt-get update -q && apt-get install -y -q wget zip unzip 2>/dev/null || true

mkdir -p "$MERGED_DIR" "$REPORT_DIR"

# Download and merge allure-results from each pipeline
for pipeline in $PIPELINES; do
  echo "=== Downloading results from $pipeline ==="
  wget -q "$BASE_URL/$pipeline/allure-report.zip" -O "/tmp/$pipeline.zip" 2>/dev/null || \
    { echo "  No report found for $pipeline — skipping"; continue; }

  mkdir -p "/tmp/$pipeline-extract"
  unzip -q "/tmp/$pipeline.zip" "allure-results/*" -d "/tmp/$pipeline-extract" 2>/dev/null || true

  # Copy result files with pipeline prefix to avoid name conflicts
  count=0
  for f in "/tmp/$pipeline-extract/allure-results/"*; do
    [ -f "$f" ] || continue
    ext="${f##*.}"
    cp "$f" "$MERGED_DIR/${pipeline}-$(basename "$f")"
    count=$((count + 1))
  done
  echo "  Merged $count result files from $pipeline"

  # Add a synthetic environment label so Allure groups by pipeline
  cat > "$MERGED_DIR/${pipeline}-environment.properties" <<EOF
Pipeline=$pipeline
Server=192.168.2.55
EOF
done

# If nothing was collected, write synthetic result
if [ -z "$(ls -A $MERGED_DIR 2>/dev/null)" ]; then
  cat > "$MERGED_DIR/dashboard-result.xml" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<testsuites>
  <testsuite name="dashboard" tests="1" failures="0">
    <testcase name="No pipeline results found" classname="dashboard"/>
  </testsuite>
</testsuites>
EOF
fi

# Download history from previous dashboard run for trends
echo "=== Downloading dashboard history ==="
mkdir -p "$MERGED_DIR/history"
for f in history.json history-trend.json categories-trend.json retry-trend.json duration-trend.json; do
  wget -q "$HISTORY_URL/$f" -O "$MERGED_DIR/history/$f" 2>/dev/null || true
done

# Generate combined Allure report
echo "=== Generating combined Allure report ==="
if wget -q "https://github.com/allure-framework/allure2/releases/download/$ALLURE_VERSION/allure-$ALLURE_VERSION.tgz" -O allure.tgz 2>/dev/null; then
  tar -xzf allure.tgz
  ./allure-$ALLURE_VERSION/bin/allure generate "$MERGED_DIR" -o "$REPORT_DIR" --clean || true
else
  echo "Allure download failed — copying raw results"
  cp "$MERGED_DIR"/*.xml "$REPORT_DIR/" 2>/dev/null || true
fi

zip -r allure-dashboard.zip "$REPORT_DIR/"
echo "Dashboard report generated → allure-dashboard.zip"
echo "Allure Dashboard http://192.168.2.55/downloads/dashboard/allure-report-dashboard/index.html"
