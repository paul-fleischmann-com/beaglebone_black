#!/usr/bin/env bash
# Generates a Markdown summary of AsciiDoc build output.
# Writes to GITHUB_STEP_SUMMARY (CI) or stdout (local).
# Usage: OUTPUT_DIR=build/docs bash scripts/adoc_summary.sh
set -euo pipefail

OUTPUT_DIR="${OUTPUT_DIR:-build/docs}"
SUMMARY_OUT="${GITHUB_STEP_SUMMARY:-/dev/stdout}"

HTML_FILES=$(find "$OUTPUT_DIR" -name "*.html" -not -path "*/.cache/*" 2>/dev/null | sort)
PDF_FILES=$(find  "$OUTPUT_DIR" -name "*.pdf"  -not -path "*/.cache/*" 2>/dev/null | sort)

{
  echo "## AsciiDoc Build"
  echo ""

  if [[ -z "$HTML_FILES" && -z "$PDF_FILES" ]]; then
    echo "> [!CAUTION]"
    echo "> Keine Ausgabedateien generiert — Build fehlgeschlagen oder keine .buildadoc Marker gefunden."
  else
    if [[ -n "$HTML_FILES" ]]; then
      echo "### HTML"
      echo "| Datei | Größe |"
      echo "|-------|-------|"
      while IFS= read -r f; do
        rel="${f#"$OUTPUT_DIR/"}"
        size=$(du -sh "$f" 2>/dev/null | cut -f1 || echo "?")
        echo "| \`$rel\` | $size |"
      done <<< "$HTML_FILES"
      echo ""
    fi

    if [[ -n "$PDF_FILES" ]]; then
      echo "### PDF"
      echo "| Datei | Größe |"
      echo "|-------|-------|"
      while IFS= read -r f; do
        rel="${f#"$OUTPUT_DIR/"}"
        size=$(du -sh "$f" 2>/dev/null | cut -f1 || echo "?")
        echo "| \`$rel\` | $size |"
      done <<< "$PDF_FILES"
    fi
  fi
} >> "$SUMMARY_OUT"
