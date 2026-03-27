#!/usr/bin/env bash
# Generates JUnit XML from .step-status/ files written by each pipeline step.
# Usage: generate-junit.sh <pipeline-name> <step1> [step2 ...]
# Output: reports/pipeline-steps-junit.xml

PIPELINE=$1; shift
mkdir -p reports .step-status

PASS=0; FAIL=0
XML_CASES=""

for step in "$@"; do
  if [ -f ".step-status/$step" ]; then
    XML_CASES="${XML_CASES}    <testcase name=\"${step}\" classname=\"${PIPELINE}\"/>\n"
    PASS=$((PASS + 1))
  else
    XML_CASES="${XML_CASES}    <testcase name=\"${step}\" classname=\"${PIPELINE}\">\n      <failure message=\"Step failed or was skipped\"/>\n    </testcase>\n"
    FAIL=$((FAIL + 1))
  fi
done

TOTAL=$((PASS + FAIL))
{
  echo '<?xml version="1.0" encoding="UTF-8"?>'
  echo '<testsuites>'
  printf '  <testsuite name="%s" tests="%d" failures="%d">\n' "$PIPELINE" "$TOTAL" "$FAIL"
  printf "%b" "$XML_CASES"
  echo '  </testsuite>'
  echo '</testsuites>'
} > reports/pipeline-steps-junit.xml

echo "JUnit: $PASS passed, $FAIL failed"
cat reports/pipeline-steps-junit.xml
