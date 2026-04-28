#!/usr/bin/env bash
# =============================================================================
# install.sh — BeagleBone Black Tools Installationsskript
# =============================================================================
set -euo pipefail

RED='\033[0;31m'; GREEN='\033[0;32m'; BLUE='\033[0;34m'
YELLOW='\033[1;33m'; NC='\033[0m'

log()     { echo -e "${BLUE}[INFO]${NC}  $*"; }
success() { echo -e "${GREEN}[OK]${NC}    $*"; }
warn()    { echo -e "${YELLOW}[WARN]${NC}  $*"; }
error()   { echo -e "${RED}[ERROR]${NC} $*"; exit 1; }

REPO_BASE="${REPO_BASE:-http://gitea.local:3000}"
REPO_USER="${REPO_USER:-admin}"
REPO_NAME="${REPO_NAME:-beaglebone}"
VERSION="${VERSION:-latest}"
INSTALL_DIR="${INSTALL_DIR:-/usr/local/bin}"
WEB_DIR="${WEB_DIR:-/opt/bbweb}"

detect_arch() {
    case $(uname -m) in
        x86_64)  echo "amd64"  ;;
        aarch64) echo "arm64"  ;;
        armv7l)  echo "armv7"  ;;
        *)       error "Architektur nicht unterstützt: $(uname -m)" ;;
    esac
}
detect_os() {
    case $(uname -s) in
        Linux)           echo "linux"   ;;
        Darwin)          echo "darwin"  ;;
        MINGW*|CYGWIN*)  echo "windows" ;;
        *)               error "OS nicht unterstützt" ;;
    esac
}

get_latest_version() {
    curl -sf "$REPO_BASE/api/v1/repos/$REPO_USER/$REPO_NAME/releases/latest" \
        | grep '"tag_name"' | cut -d'"' -f4
}

print_banner() {
    echo ""
    echo -e "${BLUE}╔══════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║   BeagleBone Black Tools Installer       ║${NC}"
    echo -e "${BLUE}║   CLI + TUI + Desktop GUI + Web GUI      ║${NC}"
    echo -e "${BLUE}╚══════════════════════════════════════════╝${NC}"
    echo ""
}

check_requirements() {
    log "Prüfe Voraussetzungen..."
    for cmd in curl sha256sum; do
        command -v "$cmd" &>/dev/null || error "$cmd nicht gefunden"
    done
    success "Voraussetzungen OK"
}

resolve_version() {
    if [[ "$VERSION" == "latest" ]]; then
        log "Ermittle neueste Version..."
        VERSION=$(get_latest_version)
        [[ -z "$VERSION" ]] && error "Version konnte nicht ermittelt werden"
    fi
    success "Version: $VERSION"
}

download_tools() {
    local os arch tmpdir
    os=$(detect_os); arch=$(detect_arch)
    tmpdir=$(mktemp -d); trap 'rm -rf '"$tmpdir" EXIT

    log "Plattform: $os/$arch"
    BASE_URL="$REPO_BASE/$REPO_USER/$REPO_NAME/releases/download/$VERSION"

    # Checksums
    curl -fsSL "$BASE_URL/checksums.sha256" -o "$tmpdir/checksums.sha256"

    # CLI
    local cli="bbcli-${os}-${arch}"
    [[ "$os" == "windows" ]] && cli+=".exe"
    log "Lade $cli..."
    curl -fsSL "$BASE_URL/$cli" -o "$tmpdir/bbcli"
    grep "$cli" "$tmpdir/checksums.sha256" | \
        (cd "$tmpdir" && sha256sum --check --status) && success "Checksum OK"

    # TUI
    local tui="bbtui-${os}-${arch}"
    [[ "$os" == "windows" ]] && tui+=".exe"
    log "Lade $tui..."
    curl -fsSL "$BASE_URL/$tui" -o "$tmpdir/bbtui"

    # Desktop GUI (Linux only)
    if [[ "$os" == "linux" ]]; then
        log "Lade bbgui..."
        curl -fsSL "$BASE_URL/bbgui-linux-${arch}" -o "$tmpdir/bbgui"
    fi

    # Web GUI
    log "Lade Web GUI..."
    curl -fsSL "$BASE_URL/bbweb-gui.zip" -o "$tmpdir/bbweb-gui.zip"

    # Installieren
    log "Installiere nach $INSTALL_DIR..."
    sudo mkdir -p "$INSTALL_DIR"
    sudo install -m 755 "$tmpdir/bbcli" "$INSTALL_DIR/bbcli"
    success "bbcli installiert"
    sudo install -m 755 "$tmpdir/bbtui" "$INSTALL_DIR/bbtui"
    success "bbtui installiert"
    if [[ "$os" == "linux" ]]; then
        sudo install -m 755 "$tmpdir/bbgui" "$INSTALL_DIR/bbgui"
        success "bbgui installiert"
    fi
    sudo mkdir -p "$WEB_DIR"
    sudo unzip -qo "$tmpdir/bbweb-gui.zip" -d "$WEB_DIR"
    success "Web GUI → $WEB_DIR"
}

setup_config() {
    if [[ -f ~/.bbcli.yaml ]]; then
        warn "Konfiguration existiert: ~/.bbcli.yaml"
        read -p "Überschreiben? [y/N]: " answer
        [[ "$answer" =~ ^[Yy]$ ]] || return 0
    fi
    log "Erstelle Konfiguration..."
    bbcli config init
    read -p "BeagleBone Host [192.168.7.2]: " host
    bbcli config set host "${host:-192.168.7.2}"
    success "Konfiguration gespeichert"
}

setup_completion() {
    local shell_type
    shell_type=$(basename "$SHELL")
    log "Installiere $shell_type Completion..."
    case "$shell_type" in
        bash)
            mkdir -p ~/.local/share/bash-completion/completions
            bbcli completion bash > ~/.local/share/bash-completion/completions/bbcli
            grep -q "bbcli" ~/.bashrc 2>/dev/null || \
                echo 'source ~/.local/share/bash-completion/completions/bbcli' >> ~/.bashrc
            success "Bash Completion installiert"
            ;;
        zsh)
            mkdir -p ~/.zsh/completions
            bbcli completion zsh > ~/.zsh/completions/_bbcli
            grep -q "bbcli" ~/.zshrc 2>/dev/null || \
                echo 'fpath=(~/.zsh/completions $fpath) && autoload -U compinit && compinit' >> ~/.zshrc
            success "Zsh Completion installiert"
            ;;
        fish)
            mkdir -p ~/.config/fish/completions
            bbcli completion fish > ~/.config/fish/completions/bbcli.fish
            success "Fish Completion installiert"
            ;;
        *) warn "Shell '$shell_type' nicht unterstützt" ;;
    esac
}

print_summary() {
    echo ""
    echo -e "${GREEN}╔══════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║   Installation abgeschlossen! 🎉         ║${NC}"
    echo -e "${GREEN}╠══════════════════════════════════════════╣${NC}"
    echo -e "${GREEN}║  bbcli  → CLI Tool                       ║${NC}"
    echo -e "${GREEN}║  bbtui  → Terminal TUI                   ║${NC}"
    echo -e "${GREEN}║  bbgui  → Desktop GUI                    ║${NC}"
    echo -e "${GREEN}║  Web GUI → $WEB_DIR          ║${NC}"
    echo -e "${GREEN}╠══════════════════════════════════════════╣${NC}"
    echo -e "${GREEN}║  Schnellstart:                           ║${NC}"
    echo -e "${GREEN}║  \$ bbcli system status                   ║${NC}"
    echo -e "${GREEN}║  \$ bbtui                                 ║${NC}"
    echo -e "${GREEN}║  \$ bbgui                                 ║${NC}"
    echo -e "${GREEN}╚══════════════════════════════════════════╝${NC}"
    echo ""
}

uninstall() {
    read -p "⚠️  Deinstallieren? [y/N]: " answer
    [[ "$answer" =~ ^[Yy]$ ]] || exit 0
    sudo rm -f "$INSTALL_DIR/bbcli" "$INSTALL_DIR/bbtui" "$INSTALL_DIR/bbgui"
    sudo rm -rf "$WEB_DIR"
    rm -f ~/.local/share/bash-completion/completions/bbcli
    rm -f ~/.zsh/completions/_bbcli
    rm -f ~/.config/fish/completions/bbcli.fish
    success "Deinstallation abgeschlossen"
    warn "Config ~/.bbcli.yaml wurde NICHT gelöscht"
}

main() {
    print_banner
    case "${1:-install}" in
        install)
            check_requirements
            resolve_version
            download_tools
            setup_config
            setup_completion
            print_summary
            ;;
        uninstall) uninstall ;;
        update)
            VERSION="latest"
            resolve_version
            download_tools
            success "Update auf $VERSION abgeschlossen"
            ;;
        completion) setup_completion ;;
        *)
            echo "Verwendung: $0 [install|uninstall|update|completion]"
            exit 1
            ;;
    esac
}

main "$@"
