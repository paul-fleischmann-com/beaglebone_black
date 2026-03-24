#!/usr/bin/env bash
# c_coverage.sh — C Code Coverage mit gcov/lcov für SonarCloud
#
# Erzeugt eine lcov .info-Datei aus gcov-Daten (*.gcda/*.gcno) eines Build-Verzeichnisses.
# SonarCloud liest sie via sonar.c.lcov.reportPaths ein.
#
# Verwendung:
#   c_coverage.sh <source-dir> <output.info> [<filter-pattern>...]
#
# Argumente:
#   source-dir      Verzeichnis mit den *.gcda/*.gcno Dateien (z.B. c-lib/)
#   output.info     Zieldatei für den lcov-Report (z.B. reports/c-coverage.info)
#   filter-pattern  Optionale Exclude-Muster (Default: '/usr/*')
#                   Mehrere Muster als separate Argumente möglich.
#
# Beispiel:
#   c_coverage.sh c-lib/ reports/c-coverage.info '/usr/*' '*/test/*'
#
# Voraussetzungen: gcc (mit -fprofile-arcs -ftest-coverage gebaut), lcov

set -euo pipefail

# ── Argument-Validierung ──────────────────────────────────────────────────────

usage() {
    echo "Verwendung: $0 <source-dir> <output.info> [<filter-pattern>...]" >&2
    echo "" >&2
    echo "  source-dir      Verzeichnis mit *.gcda/*.gcno Dateien" >&2
    echo "  output.info     Zieldatei für lcov-Report" >&2
    echo "  filter-pattern  Exclude-Muster (Standard: '/usr/*')" >&2
    exit 1
}

if [ $# -lt 2 ]; then
    usage
fi

SOURCE_DIR="$1"
OUTPUT_FILE="$2"
shift 2

# Standard-Filter wenn keine angegeben
if [ $# -eq 0 ]; then
    set -- '/usr/*'
fi

# ── Voraussetzungen prüfen ────────────────────────────────────────────────────

if ! command -v lcov >/dev/null 2>&1; then
    echo "Fehler: lcov nicht gefunden. Installation: apt-get install lcov" >&2
    exit 2
fi

if [ ! -d "$SOURCE_DIR" ]; then
    echo "Fehler: Quell-Verzeichnis '$SOURCE_DIR' nicht gefunden." >&2
    exit 3
fi

# ── Coverage erfassen ─────────────────────────────────────────────────────────

OUTPUT_DIR="$(dirname "$OUTPUT_FILE")"
if [ -n "$OUTPUT_DIR" ] && [ "$OUTPUT_DIR" != "." ]; then
    mkdir -p "$OUTPUT_DIR"
fi

echo "[c_coverage] Erfasse Coverage aus: $SOURCE_DIR"
lcov --capture \
     --directory "$SOURCE_DIR" \
     --output-file "$OUTPUT_FILE" \
     --rc lcov_branch_coverage=1 \
     --quiet

# ── Filter anwenden ───────────────────────────────────────────────────────────

for pattern in "$@"; do
    echo "[c_coverage] Filtere aus: $pattern"
    lcov --remove "$OUTPUT_FILE" \
         "$pattern" \
         --output-file "$OUTPUT_FILE" \
         --rc lcov_branch_coverage=1 \
         --quiet
done

# ── Zusammenfassung ───────────────────────────────────────────────────────────

echo "[c_coverage] Report geschrieben: $OUTPUT_FILE"
lcov --summary "$OUTPUT_FILE" --rc lcov_branch_coverage=1
