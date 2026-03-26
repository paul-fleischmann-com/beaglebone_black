#!/usr/bin/env bash
# =============================================================================
# test.sh — Go Tests bauen und ausführen
#
# Verwendung:
#   ./scripts/test.sh              # alle Tests
#   ./scripts/test.sh -race        # mit Race Detector
#   ./scripts/test.sh -cover       # mit Coverage Report
#   ./scripts/test.sh -ci          # CI-Modus (Race + Coverage + Quality Gates)
#   ./scripts/test.sh -html        # Coverage als HTML öffnen
# =============================================================================
set -euo pipefail

GREEN='\033[0;32m'; BLUE='\033[0;34m'; YELLOW='\033[1;33m'; RED='\033[0;31m'
BOLD='\033[1m'; NC='\033[0m'
log()     { echo -e "${BLUE}[TEST]${NC}  $*"; return 0; }
success() { echo -e "${GREEN}[PASS]${NC}  $*"; return 0; }
warn()    { echo -e "${YELLOW}[WARN]${NC}  $*"; return 0; }
fail()    { echo -e "${RED}[FAIL]${NC}  $*" >&2; return 0; }

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
GO_API="$REPO_ROOT/project/go-api"
COVERAGE_OUT="$GO_API/coverage.out"
COVERAGE_PAK="./pkg/hal/,./pkg/hal/mock/,./pkg/hal/config/,./pkg/hal/c/,./pkg/hal/loader/,./pkg/hal/rust/,./pkg/api/"
COVERAGE_HTML="$GO_API/coverage.html"

# Quality Gates (aus CLAUDE.md)
MIN_COVERAGE_AVG=75   # % Durchschnitt
MIN_COVERAGE_FILE=50  # % pro Datei

MODE_RACE=false
MODE_COVER=false
MODE_HTML=false
MODE_CI=false

parse_args() {
    for arg in "$@"; do
        case "$arg" in
            -race)  MODE_RACE=true ;;
            -cover) MODE_COVER=true ;;
            -html)  MODE_COVER=true; MODE_HTML=true ;;
            -ci)    MODE_RACE=true; MODE_COVER=true; MODE_CI=true ;;
            -h|--help)
                echo "Verwendung: $0 [-race] [-cover] [-html] [-ci]"
                exit 0
                ;;
            *) fail "Unbekanntes Argument: $arg"; exit 1 ;;
        esac
    done
    return 0
}

# ── Tests ausführen ───────────────────────────────────────────────────────────
run_tests() {
    local args=("-v" "-count=1" "-timeout=60s")
    
    $MODE_RACE  && args+=("-race" "-count=3")
    # -coverpkg misst Coverage auch in importierten Packages (z.B. mock/driver.go
    # wird von hal_test.go aufgerufen — ohne -coverpkg zeigt es 0%)
    $MODE_COVER && args+=(
        "-coverprofile=$COVERAGE_OUT"
        "-covermode=atomic"
        "-coverpkg=$COVERAGE_PAK" 
    )

    # pkg/hal/c und pkg/hal/rust benötigen native C-Header (bme280.h, hardware_rs.h)
    # und die kompilierten Shared Libraries — nicht verfügbar in der Dev-Umgebung.
    # Tests laufen ausschliesslich gegen den Mock-Driver.
    # pkg/hal/c, pkg/hal/rust und pkg/hal/loader benötigen native C-Header
    # und kompilierte Shared Libraries — nicht verfügbar in der Dev-Umgebung.
    # Tests laufen ausschliesslich gegen den Mock-Driver.
    local pkgs=(
        "./pkg/hal/"
        "./pkg/hal/mock/"
        "./pkg/hal/config/"
        #"./pkg/hal/c/"
        #"./pkg/hal/loader/"
        #"./pkg/hal/rust/"
        "./pkg/api/"
    )

    log "Führe Tests aus: go test ${args[*]} ${pkgs[*]}"
    echo ""

    local exit_code=0
    (cd "$GO_API" && go test "${args[@]}" "${pkgs[@]}") || exit_code=$?

    echo ""
    if [[ $exit_code -eq 0 ]]; then
        success "Alle Tests bestanden"
    else
        fail "Tests fehlgeschlagen (Exit $exit_code)"
        return $exit_code
    fi
}

# ── Coverage auswerten ────────────────────────────────────────────────────────
check_coverage() {
    [[ ! -f "$COVERAGE_OUT" ]] && return

    echo ""
    log "Coverage-Bericht:"
    echo ""
    (cd "$GO_API" && go tool cover -func="$COVERAGE_OUT")
    echo ""

    # Gesamtcoverage auslesen
    local total
    total=$(cd "$GO_API" && go tool cover -func="$COVERAGE_OUT" \
        | grep "^total:" | awk '{print $3}' | tr -d '%')

    echo -e "${BOLD}Gesamt-Coverage: ${total}%${NC}"

    if $MODE_CI; then
        # Quality Gate: Durchschnitt
        if awk "BEGIN{exit !($total >= $MIN_COVERAGE_AVG)}"; then
            success "Coverage Gate: ${total}% >= ${MIN_COVERAGE_AVG}% ✓"
        else
            fail "Coverage Gate: ${total}% < ${MIN_COVERAGE_AVG}% (Minimum)"
            return 1
        fi

        # Quality Gate: pro Datei
        local failed_files=0
        while IFS= read -r line; do
            local pct file
            pct=$(echo "$line" | awk '{print $3}' | tr -d '%')
            file=$(echo "$line" | awk '{print $1}')
            if awk "BEGIN{exit !($pct < $MIN_COVERAGE_FILE)}"; then
                warn "Unter Minimum: $file → ${pct}% < ${MIN_COVERAGE_FILE}%"
                ((failed_files++))
            fi
        done < <(cd "$GO_API" && go tool cover -func="$COVERAGE_OUT" | grep -v "^total:")

        if [[ $failed_files -gt 0 ]]; then
            fail "$failed_files Datei(en) unter ${MIN_COVERAGE_FILE}% Coverage"
            return 1
        fi
    fi

    # HTML-Report
    if $MODE_HTML; then
        (cd "$GO_API" && go tool cover -html="$COVERAGE_OUT" -o "$COVERAGE_HTML")
        success "HTML-Report: $COVERAGE_HTML"
        if command -v xdg-open &>/dev/null; then
            xdg-open "$COVERAGE_HTML" 2>/dev/null &
        fi
    fi
}

# ── Main ──────────────────────────────────────────────────────────────────────
main() {
    parse_args "$@"

    echo ""
    echo -e "${BOLD}${BLUE}═══ BeagleBone Black — Go Tests ═══${NC}"
    $MODE_RACE  && echo -e "  Race Detector:  ${GREEN}an${NC}"
    $MODE_COVER && echo -e "  Coverage:       ${GREEN}an${NC}"
    $MODE_CI    && echo -e "  Quality Gates:  avg≥${MIN_COVERAGE_AVG}%  per-file≥${MIN_COVERAGE_FILE}%"
    echo ""

    run_tests
    check_coverage

    echo ""
    success "Fertig"
    return 0
}

main "$@"
