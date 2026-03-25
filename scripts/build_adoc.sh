#!/usr/bin/env bash
# =============================================================================
# build_adoc.sh — AsciiDoc Build Script
# Sucht alle .adoc Dateien wo ein .buildadoc Marker im selben Ordner liegt
# Baut PDF und HTML für jede gefundene Datei
# =============================================================================
set -euo pipefail

# ── Farben ────────────────────────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

log()     { echo -e "${BLUE}[BUILD]${NC}  $*"; }
success() { echo -e "${GREEN}[OK]${NC}    $*"; }
warn()    { echo -e "${YELLOW}[WARN]${NC}  $*"; }
error()   { echo -e "${RED}[ERROR]${NC} $*"; }
info()    { echo -e "${CYAN}[INFO]${NC}  $*"; }

# ── Konfiguration ─────────────────────────────────────────────────────────────
ROOT_DIR="${ROOT_DIR:-.}"
OUTPUT_DIR="${OUTPUT_DIR:-/workspace/docs}"
PLANTUML_JAR="${PLANTUML_JAR:-/usr/local/bin/plantuml.jar}"
ASCIIDOCTOR_EXTRA_ARGS="${ASCIIDOCTOR_EXTRA_ARGS:-}"

mkdir -p "$OUTPUT_DIR"

# ── Statistiken ───────────────────────────────────────────────────────────────
FOUND=0
BUILT=0
SKIPPED=0
FAILED=0
declare -a BUILT_FILES=()
declare -a FAILED_FILES=()

# ── .buildadoc Konfig parsen ──────────────────────────────────────────────────
parse_buildadoc() {
    local marker_file="$1"
    local key="$2"
    local default="$3"

    if [[ -f "$marker_file" ]]; then
        local val
        val=$(grep "^${key}:" "$marker_file" 2>/dev/null \
              | head -1 | cut -d: -f2 | xargs)
        echo "${val:-$default}"
    else
        echo "$default"
    fi
}

# ── AsciiDoc Datei bauen ──────────────────────────────────────────────────────
build_adoc() {
    local adoc_file="$1"
    local dir
    dir=$(dirname "$adoc_file")
    local base
    base=$(basename "$adoc_file" .adoc)
    local marker="${dir}/.buildadoc"

    # Konfiguration aus .buildadoc lesen
    local formats
    formats=$(parse_buildadoc "$marker" "formats" "html,pdf")
    local theme
    theme=$(parse_buildadoc   "$marker" "theme"   "dark")
    local plantuml_enabled
    plantuml_enabled=$(parse_buildadoc "$marker" "plantuml" "true")
    local toc
    toc=$(parse_buildadoc     "$marker" "toc"     "left")
    local numbered
    numbered=$(parse_buildadoc "$marker" "numbered" "true")
    local lang
    lang=$(parse_buildadoc    "$marker" "lang"    "de")
    local author
    author=$(parse_buildadoc  "$marker" "author"  "")

    # Ausgabe-Verzeichnis spiegelt Quell-Struktur
    local rel_dir
    rel_dir=$(realpath --relative-to="$ROOT_DIR" "$dir" 2>/dev/null || echo "$dir")
    local out_dir="${OUTPUT_DIR}/${rel_dir}"
    mkdir -p "$out_dir"

    log "Baue: ${adoc_file}"
    info "  Formate:  ${formats}"
    info "  Theme:    ${theme}"
    info "  PlantUML: ${plantuml_enabled}"
    info "  Ausgabe:  ${out_dir}"

    # ── Gemeinsame Asciidoctor Argumente ──────────────────────────────────────
    local common_args=(
        "-a" "lang=${lang}"
        "-a" "toc=${toc}"
        "-a" "revdate=$(date +%Y-%m-%d)"
        "-a" "imagesdir=images"
        "-a" "plantumldir=diagrams"
        "-a" "source-highlighter=rouge"
        "-a" "rouge-style=monokai"
        "--base-dir" "${dir}"
        "--destination-dir" "${out_dir}"
    )

    [[ "$numbered" == "true" ]] && common_args+=("-a" "sectnums")
    [[ -n "$author" ]] && common_args+=("-a" "author=${author}")

    # PlantUML Extension aktivieren
    if [[ "$plantuml_enabled" == "true" ]]; then
        common_args+=("-r" "asciidoctor-diagram")
        common_args+=("-a" "diagram-cachedir=${out_dir}/.cache")
    fi

    local build_ok=true

    # ── HTML Build ────────────────────────────────────────────────────────────
    if [[ "$formats" == *"html"* ]]; then
        log "  → HTML wird gebaut..."

        local html_args=(
            "${common_args[@]}"
            "-b" "html5"
            "-a" "stylesdir=."
            "-o" "${out_dir}/${base}.html"
        )

        if asciidoctor "${html_args[@]}" "$adoc_file" 2>&1; then
            success "  ✅ HTML: ${out_dir}/${base}.html ($(
                du -sh "${out_dir}/${base}.html" 2>/dev/null \
                | cut -f1 || echo "?"))"
        else
            error "  ❌ HTML Build fehlgeschlagen: ${adoc_file}"
            build_ok=false
        fi
    fi

    # ── PDF Build ─────────────────────────────────────────────────────────────
    if [[ "$formats" == *"pdf"* ]]; then
        log "  → PDF wird gebaut..."

        local pdf_args=(
            "${common_args[@]}"
            "-b" "pdf"
            "-r" "asciidoctor-pdf"
            "-a" "pdf-fontsdir=GEM_FONTS_DIR"
            "-o" "${out_dir}/${base}.pdf"
        )
        if [[ "$theme" == "dark" ]]; then
            pdf_args+=("-a" "pdf-theme=default-with-fallback-font")
        fi

        if asciidoctor-pdf "${pdf_args[@]}" "$adoc_file" 2>&1; then
            success "  ✅ PDF:  ${out_dir}/${base}.pdf ($(
                du -sh "${out_dir}/${base}.pdf" 2>/dev/null \
                | cut -f1 || echo "?"))"
        else
            error "  ❌ PDF Build fehlgeschlagen: ${adoc_file}"
            build_ok=false
        fi
    fi

    if $build_ok; then
        BUILT_FILES+=("$adoc_file")
        return 0
    else
        FAILED_FILES+=("$adoc_file")
        return 1
    fi
}

# ── Alle .adoc Dateien suchen ─────────────────────────────────────────────────
echo ""
echo -e "${BLUE}╔══════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║         AsciiDoc Build System                        ║${NC}"
echo -e "${BLUE}║  Suche nach .adoc + .buildadoc Paaren...             ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════╝${NC}"
echo ""

log "Suche in: ${ROOT_DIR}"
log "Ausgabe:  ${OUTPUT_DIR}"
echo ""

# Alle .adoc Dateien finden
while IFS= read -r -d '' adoc_file; do
    dir=$(dirname "$adoc_file")
    marker="${dir}/.buildadoc"

    ((FOUND++)) || true

    # Prüfen ob .buildadoc im selben Ordner liegt
    if [[ -f "$marker" ]]; then
        info "✅ Marker gefunden: ${marker}"
        info "   Datei:  ${adoc_file}"

        if build_adoc "$adoc_file"; then
            ((BUILT++)) || true
        else
            ((FAILED++)) || true
        fi
        echo ""
    else
        warn "⏭  Übersprungen (kein .buildadoc): ${adoc_file}"
        ((SKIPPED++)) || true
    fi

done < <(find "$ROOT_DIR" \
    -name "*.adoc" \
    -not -path "*/node_modules/*" \
    -not -path "*/.git/*" \
    -not -path "*/vendor/*" \
    -not -path "*/.cache/*" \
    -print0 | sort -z)

# ── Zusammenfassung ───────────────────────────────────────────────────────────
echo ""
echo -e "${BLUE}╔══════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                 Build Zusammenfassung                ║${NC}"
echo -e "${BLUE}╠══════════════════════════════════════════════════════╣${NC}"
echo -e "${BLUE}║${NC}  Gefunden:      ${CYAN}${FOUND}${NC} .adoc Dateien                     ${BLUE}║${NC}"
echo -e "${BLUE}║${NC}  Gebaut:        ${GREEN}${BUILT}${NC} Dateien                           ${BLUE}║${NC}"
echo -e "${BLUE}║${NC}  Übersprungen:  ${YELLOW}${SKIPPED}${NC} Dateien (kein .buildadoc)       ${BLUE}║${NC}"
echo -e "${BLUE}║${NC}  Fehlgeschlagen:${RED}${FAILED}${NC} Dateien                           ${BLUE}║${NC}"
echo -e "${BLUE}╠══════════════════════════════════════════════════════╣${NC}"

if [[ ${#BUILT_FILES[@]} -gt 0 ]]; then
    echo -e "${BLUE}║${NC}  ${GREEN}Erfolgreich gebaut:${NC}                                  ${BLUE}║${NC}"
    for f in "${BUILT_FILES[@]}"; do
        echo -e "${BLUE}║${NC}    ${GREEN}✅${NC} $(basename "$f")                              ${BLUE}║${NC}"
    done
fi

if [[ ${#FAILED_FILES[@]} -gt 0 ]]; then
    echo -e "${BLUE}║${NC}  ${RED}Fehlgeschlagen:${NC}                                      ${BLUE}║${NC}"
    for f in "${FAILED_FILES[@]}"; do
        echo -e "${BLUE}║${NC}    ${RED}❌${NC} $(basename "$f")                              ${BLUE}║${NC}"
    done
fi

echo -e "${BLUE}╠══════════════════════════════════════════════════════╣${NC}"

# Generierte Dateien auflisten
if [[ -d "$OUTPUT_DIR" ]]; then
    echo -e "${BLUE}║${NC}  ${CYAN}Generierte Ausgabedateien:${NC}                          ${BLUE}║${NC}"
    while IFS= read -r -d '' f; do
        local_size=$(du -sh "$f" 2>/dev/null | cut -f1 || echo "?")
        rel=$(realpath --relative-to="$OUTPUT_DIR" "$f" \
              2>/dev/null || basename "$f")
        echo -e "${BLUE}║${NC}    ${CYAN}📄${NC} ${rel} (${local_size})          ${BLUE}║${NC}"
    done < <(find "$OUTPUT_DIR" \
        \( -name "*.html" -o -name "*.pdf" \) \
        -not -path "*/.cache/*" \
        -print0 | sort -z)
fi

echo -e "${BLUE}╚══════════════════════════════════════════════════════╝${NC}"

# Exit Code basierend auf Fehlern
if [[ $FAILED -gt 0 ]]; then
    error "Build mit ${FAILED} Fehlern abgeschlossen!"
    exit 1
fi

success "Build erfolgreich abgeschlossen!"
exit 0
