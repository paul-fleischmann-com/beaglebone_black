#!/usr/bin/env bash
# =============================================================================
# report.sh — Vollständiger Test-Report aller Komponenten
#
# Komponenten:
#   1. Go HAL Tests      (go test -json)
#   2. Python API Tests  (pytest-json-report)
#   3. Python CLI Tests  (pytest-json-report)
#   4. Python HW Tests   (pytest-json-report)
#   5. Shell Syntax      (bash -n)
#   6. Web GUI HTML      (HTMLParser)
#
# Verwendung:
#   ./scripts/report.sh
#   ./scripts/report.sh --open   # HTML Coverage im Browser öffnen
# =============================================================================
set -euo pipefail

GREEN='\033[0;32m'; BLUE='\033[0;34m'; YELLOW='\033[1;33m'
RED='\033[0;31m'; BOLD='\033[1m'; GRAY='\033[0;37m'; NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
GO_API="$REPO_ROOT/go-api"
REPORT_DIR="$REPO_ROOT/reports"
OPEN_HTML=false
[[ "${1:-}" == "--open" ]] && OPEN_HTML=true

mkdir -p "$REPORT_DIR"

# Gesamt-Zähler
TOTAL_PASSED=0
TOTAL_FAILED=0
TOTAL_SKIPPED=0
declare -a SECTION_SUMMARY=()

# ── Hilfsfunktionen ───────────────────────────────────────────────────────────
section_header() {
    echo ""
    echo -e "${BOLD}$1${NC}"
    echo -e "${GRAY}────────────────────────────────────────────────${NC}"
}

record_section() {
    local name="$1" passed="$2" failed="$3" skipped="$4" extra="${5:-}"
    TOTAL_PASSED=$((TOTAL_PASSED + passed))
    TOTAL_FAILED=$((TOTAL_FAILED + failed))
    TOTAL_SKIPPED=$((TOTAL_SKIPPED + skipped))

    local icon
    if   [[ $failed -gt 0 ]]; then icon="${RED}❌${NC}"
    elif [[ $passed -eq 0 && $skipped -gt 0 ]]; then icon="${YELLOW}⏭ ${NC}"
    else icon="${GREEN}✅${NC}"
    fi

    local line="  ${icon} ${BOLD}${name}${NC}"
    [[ -n "$extra" ]] && line+="  ${GRAY}${extra}${NC}"
    SECTION_SUMMARY+=("$line  ${GRAY}(passed:${passed} failed:${failed} skipped:${skipped})${NC}")
}

# ── 1. Go HAL Tests ───────────────────────────────────────────────────────────
run_go_tests() {
    section_header "1. Go HAL Tests"
    local go_json="$REPORT_DIR/go-tests.json"
    local pkgs=("./pkg/hal/" "./pkg/hal/mock/" "./pkg/hal/config/")

    (cd "$GO_API" && go test -json -count=1 -timeout=60s \
        -coverprofile="$REPORT_DIR/go-coverage.out" \
        -covermode=atomic \
        -coverpkg=./pkg/hal/,./pkg/hal/mock/,./pkg/hal/config/ \
        "${pkgs[@]}" 2>&1) > "$go_json" || true

    local passed=0 failed=0 skipped=0
    while IFS= read -r line; do
        local action test elapsed
        action=$(echo "$line"  | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('Action',''))"  2>/dev/null) || continue
        test=$(echo "$line"    | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('Test',''))"    2>/dev/null) || continue
        elapsed=$(echo "$line" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('Elapsed',''))" 2>/dev/null) || continue
        [[ -z "$test" ]] && continue
        case "$action" in
            pass)   echo -e "  ${GREEN}✅${NC} $test  ${GRAY}${elapsed}s${NC}"; passed=$((passed + 1)) ;;
            fail)   echo -e "  ${RED}❌${NC} $test  ${GRAY}${elapsed}s${NC}";  failed=$((failed + 1)) ;;
            skip)   echo -e "  ${YELLOW}⏭ ${NC} $test";                        skipped=$((skipped + 1)) ;;
            *)      ;;
        esac
    done < "$go_json"

    local coverage="–"
    if [[ -f "$REPORT_DIR/go-coverage.out" ]]; then
        coverage=$(cd "$GO_API" && go tool cover -func="$REPORT_DIR/go-coverage.out" \
            | grep "^total:" | awk '{print $3}')
        (cd "$GO_API" && go tool cover -html="$REPORT_DIR/go-coverage.out" \
            -o "$REPORT_DIR/go-coverage.html" 2>/dev/null)
    fi

    echo -e "  ${GRAY}Coverage: ${BOLD}${coverage}${NC}"
    record_section "Go HAL Tests" "$passed" "$failed" "$skipped" "coverage: $coverage"
}

# ── Python Test-Suite (generisch) ────────────────────────────────────────────
run_pytest_suite() {
    local title="$1" dir="$2" report_file="$3"

    section_header "$title"

    local junit_file="${report_file%.json}.pytest.junit.xml"
    pytest "$dir" \
        --timeout=10 \
        --json-report \
        --json-report-file="$report_file" \
        --junit-xml="$junit_file" \
        -q 2>&1 || true

    if [[ ! -f "$report_file" ]]; then
        echo -e "  ${YELLOW}⚠${NC}  Kein Report erstellt"
        record_section "$title" 0 0 0
        return
    fi

    python3 - "$report_file" <<'EOF'
import json, sys

GREEN  = "\033[0;32m"; RED    = "\033[0;31m"
YELLOW = "\033[1;33m"; GRAY   = "\033[0;37m"; NC = "\033[0m"

data  = json.load(open(sys.argv[1]))
tests = data.get("tests", [])

for t in tests:
    name    = t["nodeid"].split("::")[-1]
    outcome = t["outcome"]
    dur     = t.get("call", {}).get("duration", 0)

    skip_msg = ""
    if outcome == "skipped":
        longrepr = t.get("setup", {}).get("longrepr", "")
        if isinstance(longrepr, list):
            longrepr = longrepr[-1] if longrepr else ""
        raw = str(longrepr)
        skip_msg = raw.split("Skipped: ", 1)[-1].strip() if "Skipped: " in raw else raw.strip()
        skip_msg = f"  {GRAY}({skip_msg[:70]}){NC}" if skip_msg else ""

    icon    = {"passed": f"{GREEN}✅{NC}", "failed": f"{RED}❌{NC}",
               "skipped": f"{YELLOW}⏭ {NC}"}.get(outcome, "  ")
    dur_str = f"  {GRAY}{dur:.2f}s{NC}" if outcome != "skipped" else ""
    print(f"  {icon} {name}{dur_str}{skip_msg}")
EOF

    record_section "$title" \
        "$(python3 -c "import json; d=json.load(open('$report_file')); print(d['summary'].get('passed',0))")" \
        "$(python3 -c "import json; d=json.load(open('$report_file')); print(d['summary'].get('failed',0))")" \
        "$(python3 -c "import json; d=json.load(open('$report_file')); print(d['summary'].get('skipped',0))")"
}

# ── 5. Shell Syntax ───────────────────────────────────────────────────────────
run_shell_syntax() {
    section_header "5. Shell Script Syntax"
    local passed=0 failed=0
    local log_file="$REPORT_DIR/shell-syntax.txt"
    : > "$log_file"

    while IFS= read -r f; do
        local rel="${f#$REPO_ROOT/}"
        if bash -n "$f" 2>/dev/null; then
            echo -e "  ${GREEN}✅${NC} $rel"
            echo "✅ $rel" >> "$log_file"
            passed=$((passed + 1))
        else
            echo -e "  ${RED}❌${NC} $rel"
            bash -n "$f" 2>&1 | sed 's/^/     /'
            echo "❌ $rel" >> "$log_file"
            bash -n "$f" >> "$log_file" 2>&1 || true
            failed=$((failed + 1))
        fi
    done < <(find "$REPO_ROOT" -name "*.sh" -not -path "*/.git/*" | sort)

    export _SH_PASSED=$passed _SH_FAILED=$failed
    record_section "Shell Syntax" "$passed" "$failed" 0
}

# ── 6. Web GUI HTML ───────────────────────────────────────────────────────────
run_html_validation() {
    section_header "6. Web GUI HTML Validation"
    local html_file="$REPO_ROOT/tools/web-gui/index.html"

    if [[ ! -f "$html_file" ]]; then
        echo -e "  ${YELLOW}⚠${NC}  $html_file nicht gefunden"
        record_section "Web GUI HTML" 0 0 1
        return
    fi

    if python3 -c "
from html.parser import HTMLParser
class StrictParser(HTMLParser):
    def handle_starttag(self, tag, attrs): pass
    def handle_endtag(self, tag): pass
StrictParser().feed(open('$html_file').read())
" 2>/dev/null; then
        echo -e "  ${GREEN}✅${NC} tools/web-gui/index.html"
        export _HTML_OK=1
        record_section "Web GUI HTML" 1 0 0
    else
        echo -e "  ${RED}❌${NC} tools/web-gui/index.html — HTML-Fehler gefunden"
        export _HTML_OK=0
        record_section "Web GUI HTML" 0 1 0
    fi
}

# ── GitHub Actions Markdown Summary ──────────────────────────────────────────
generate_github_summary() {
    [[ -z "${GITHUB_STEP_SUMMARY:-}" ]] && return

    python3 - "$REPORT_DIR" "$TOTAL_PASSED" "$TOTAL_FAILED" "$TOTAL_SKIPPED" \
        "${SECTION_SUMMARY[@]+"${SECTION_SUMMARY[@]}"}" <<'PYEOF' >> "$GITHUB_STEP_SUMMARY"
import json, sys, os, re
from datetime import datetime

report_dir   = sys.argv[1]
total_passed = int(sys.argv[2])
total_failed = int(sys.argv[3])
total_skipped= int(sys.argv[4])

def load_json(path):
    try:
        return json.load(open(path)) if os.path.isfile(path) else None
    except Exception:
        return None

def outcome_icon(o):
    return {"passed": "✅", "pass": "✅", "failed": "❌", "fail": "❌", "skipped": "⏭", "skip": "⏭"}.get(o, "❓")

def summary_icon(p, f, s):
    if f > 0:   return "❌"
    if p == 0:  return "⏭"
    return "✅"

# ── Header ────────────────────────────────────────────────────────────────────
print("# 🧪 Test Report — BeagleBone Black")
print(f"_{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_\n")

overall = "🟢 PASS" if total_failed == 0 else "🔴 FAIL"
print(f"> **{overall}** &nbsp; ✅ {total_passed} passed &nbsp; ❌ {total_failed} failed &nbsp; ⏭ {total_skipped} skipped\n")

# ── 1. Go HAL Tests ───────────────────────────────────────────────────────────
go_cov  = ""
cov_file = f"{report_dir}/go-coverage.out"
if os.path.isfile(cov_file):
    for line in open(cov_file):
        if line.startswith("total:"):
            go_cov = line.split()[-1]

go_tests = {}
go_json_path = f"{report_dir}/go-tests.json"
if os.path.isfile(go_json_path):
    for raw in open(go_json_path):
        try:
            d = json.loads(raw)
        except Exception:
            continue
        if d.get("Action") in ("pass","fail","skip") and d.get("Test"):
            go_tests[d["Test"]] = {"action": d["Action"], "elapsed": d.get("Elapsed", 0)}

gp = sum(1 for v in go_tests.values() if v["action"] == "pass")
gf = sum(1 for v in go_tests.values() if v["action"] == "fail")
gs = sum(1 for v in go_tests.values() if v["action"] == "skip")
icon = summary_icon(gp, gf, gs)
cov_str = f" — Coverage: **{go_cov}**" if go_cov else ""
print(f"<details><summary>{icon} <b>1. Go HAL Tests</b> &nbsp; ✅ {gp} &nbsp; ❌ {gf} &nbsp; ⏭ {gs}{cov_str}</summary>\n")
if go_tests:
    print("| Test | Result | Duration |")
    print("|---|---|---|")
    for name, v in go_tests.items():
        print(f"| `{name}` | {outcome_icon(v['action'])} | {v['elapsed']}s |")
print("\n</details>\n")

# ── Python Test Suites ────────────────────────────────────────────────────────
suites = [
    ("2. Python API Tests",      f"{report_dir}/pytest-api.json"),
    ("3. Python CLI Tests",      f"{report_dir}/pytest-cli.json"),
    ("4. Python Hardware Tests", f"{report_dir}/pytest-hardware.json"),
]
for title, path in suites:
    data = load_json(path)
    if not data:
        print(f"<details><summary>⚠️ <b>{title}</b> — kein Report</summary>\n</details>\n")
        continue
    s = data.get("summary", {})
    p, f, sk = s.get("passed",0), s.get("failed",0), s.get("skipped",0)
    icon = summary_icon(p, f, sk)
    print(f"<details><summary>{icon} <b>{title}</b> &nbsp; ✅ {p} &nbsp; ❌ {f} &nbsp; ⏭ {sk}</summary>\n")
    tests = data.get("tests", [])
    if tests:
        print("| Test | Result | Info |")
        print("|---|---|---|")
        for t in tests:
            name = t["nodeid"].split("::")[-1]
            o    = t["outcome"]
            info = ""
            if o == "skipped":
                lr = t.get("setup", {}).get("longrepr", "")
                if isinstance(lr, list): lr = lr[-1] if lr else ""
                raw = str(lr)
                info = raw.split("Skipped: ",1)[-1][:80] if "Skipped: " in raw else raw[:80]
            elif o == "failed":
                info = str(t.get("call",{}).get("longrepr",""))[:100]
            print(f"| `{name}` | {outcome_icon(o)} | {info} |")
    print("\n</details>\n")

# ── Shell Syntax ──────────────────────────────────────────────────────────────
sh_passed = int(os.getenv("_SH_PASSED", "0"))
sh_failed = int(os.getenv("_SH_FAILED", "0"))
icon = summary_icon(sh_passed, sh_failed, 0)
print(f"<details><summary>{icon} <b>5. Shell Script Syntax</b> &nbsp; ✅ {sh_passed} &nbsp; ❌ {sh_failed}</summary>\n")
for line in open(f"{report_dir}/shell-syntax.txt"):
    print(line.rstrip())
print("\n</details>\n")

# ── Web GUI ───────────────────────────────────────────────────────────────────
html_ok = os.getenv("_HTML_OK", "1") == "1"
icon = "✅" if html_ok else "❌"
print(f"**{icon} 6. Web GUI HTML Validation** — {'valide' if html_ok else 'Fehler gefunden'}\n")

PYEOF
}

# ── Gesamt-Zusammenfassung ────────────────────────────────────────────────────
print_summary() {
    echo ""
    echo -e "${BOLD}${BLUE}═══ Zusammenfassung ══════════════════════════════${NC}"
    for line in "${SECTION_SUMMARY[@]}"; do
        echo -e "$line"
    done
    echo ""
    echo -e "  ${GREEN}✅ Passed:${NC}  ${BOLD}${TOTAL_PASSED}${NC}"
    echo -e "  ${RED}❌ Failed:${NC}  ${BOLD}${TOTAL_FAILED}${NC}"
    echo -e "  ${YELLOW}⏭  Skipped:${NC} ${BOLD}${TOTAL_SKIPPED}${NC}"
    echo -e "  ${GRAY}Reports:   ${REPORT_DIR}/${NC}"
    echo -e "${BOLD}${BLUE}══════════════════════════════════════════════════${NC}"

    if [[ $TOTAL_FAILED -gt 0 ]]; then
        echo -e "${RED}${BOLD}FAIL${NC}"
        return 1
    else
        echo -e "${GREEN}${BOLD}PASS${NC}"
    fi
}

# ── Main ──────────────────────────────────────────────────────────────────────
echo ""
echo -e "${BOLD}${BLUE}═══ BeagleBone Black — Vollständiger Test-Report ═══${NC}"
echo -e "${GRAY}    $(date '+%Y-%m-%d %H:%M:%S')${NC}"

run_go_tests
run_pytest_suite "2. Python API Tests"      "$REPO_ROOT/tests/api/"      "$REPORT_DIR/pytest-api.json"
run_pytest_suite "3. Python CLI Tests"      "$REPO_ROOT/tests/cli/"      "$REPORT_DIR/pytest-cli.json"
run_pytest_suite "4. Python Hardware Tests" "$REPO_ROOT/tests/hardware/" "$REPORT_DIR/pytest-hardware.json"
run_shell_syntax
run_html_validation

# ── Test-Ergebnisse in requirements.json aktualisieren ───────────────────────
section_header "7. Requirements Tracing aktualisieren"
if python3 "$REPO_ROOT/scripts/collect_results.py" \
    --workspace "$REPORT_DIR" \
    --requirements "$REPO_ROOT/reports/requirements.json" \
    --output "$REPORT_DIR/test_results.json"; then
    echo -e "  ${GREEN}✅${NC} requirements.json aktualisiert"
else
    echo -e "  ${YELLOW}⚠${NC}  collect_results.py fehlgeschlagen — requirements.json unverändert"
fi

generate_github_summary
print_summary

if $OPEN_HTML && [[ -f "$REPORT_DIR/go-coverage.html" ]]; then
    command -v xdg-open &>/dev/null && xdg-open "$REPORT_DIR/go-coverage.html" 2>/dev/null &
fi

echo ""
