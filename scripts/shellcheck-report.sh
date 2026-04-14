#!/bin/sh
# Run shellcheck on all scripts and generate a log + JUnit XML report.
# Does not fail the build — findings are documented only.
set -e

mkdir -p reports
> reports/shellcheck.txt

TOTAL=0
FAILURES=0
JUNIT=reports/shellcheck-junit.xml

{
  echo '<?xml version="1.0" encoding="UTF-8"?>'
  echo '<testsuites>'
  for f in scripts/*.sh; do
    findings=$(shellcheck -f gcc "$f" 2>&1 || true)
    count=$(echo "$findings" | grep -c '.' 2>/dev/null || echo 0)
    TOTAL=$((TOTAL + 1))
    name=$(basename "$f")
    if [ "$count" -eq 0 ]; then
      echo "  <testsuite name=\"shellcheck\" tests=\"1\" failures=\"0\"><testcase name=\"$name\" classname=\"shellcheck\"/></testsuite>"
    else
      FAILURES=$((FAILURES + 1))
      safe=$(echo "$findings" | sed 's/&/\&amp;/g;s/</\&lt;/g;s/>/\&gt;/g')
      echo "  <testsuite name=\"shellcheck\" tests=\"1\" failures=\"1\"><testcase name=\"$name\" classname=\"shellcheck\"><failure message=\"$count finding(s)\">$safe</failure></testcase></testsuite>"
    fi
    echo "$findings" >> reports/shellcheck.txt
  done
  echo '</testsuites>'
} > "$JUNIT"

echo "--- ShellCheck Summary: $FAILURES/$TOTAL scripts with findings ---"
[ -s reports/shellcheck.txt ] && cat reports/shellcheck.txt || echo "No findings."
