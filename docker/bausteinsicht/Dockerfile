# =============================================
# Bausteinsicht CI Container (multi-stage)
# Stage 1: compile Go binary from upstream repo
# Stage 2: slim runtime + DrawIO headless
# =============================================
# Build context must contain:
#   drawio-export — wrapper script from docker/bausteinsicht/

# ── Stage 1: Build ────────────────────────────────
# GO_VERSION muss >= der go.mod-Anforderung von Bausteinsicht sein (aktuell
# "go 1.25.8" bei BAUSTEINSICHT_REV unten), sonst laedt Go automatisch ein
# passendes Toolchain nach (GOTOOLCHAIN=auto) statt das Image-Go zu nutzen.
ARG GO_VERSION=1.25
FROM golang:${GO_VERSION} AS builder

RUN apt-get update && apt-get install -y --no-install-recommends git && rm -rf /var/lib/apt/lists/*

WORKDIR /src
# Gepinnt auf einen bekannt guten Release-Tag statt des unveränderten
# Default-Branch-HEAD — Upstream ist in aktiver Entwicklung (siehe
# scripts/setup_open1722.sh für dasselbe Muster/dieselbe Begründung), ein
# unbemerkter Breaking-Change hat hier bereits den Build zerschossen: Upstream
# hat cmd/ um ein zweites main-Package (bausteinsicht-lsp) erweitert, wodurch
# `go build -o <Datei> ./cmd/...` mit "cannot write multiple packages to
# non-directory" fehlschlug.
ARG BAUSTEINSICHT_REV=v1.2.1
RUN --mount=type=secret,id=Bau_token \
    git clone --depth 1 --branch ${BAUSTEINSICHT_REV} \
      https://oauth2:$(cat /run/secrets/Bau_token)@github.com/docToolchain/Bausteinsicht.git .
# Nur das CLI-Binary bauen (./cmd/bausteinsicht) — die .drone.yml ruft
# ausschließlich `bausteinsicht validate/sync/export-*` auf, nie den
# LSP-Server (./cmd/bausteinsicht-lsp).
RUN go build -o /usr/local/bin/bausteinsicht ./cmd/bausteinsicht

# ── Stage 2: Runtime ──────────────────────────────
FROM debian:bookworm

ARG DRAWIO_VERSION=29.5.2
ARG VERSION=unknown

LABEL org.opencontainers.image.version=$VERSION
ENV APP_VERSION=$VERSION

# Copy compiled binary from builder
COPY --from=builder /usr/local/bin/bausteinsicht /usr/local/bin/bausteinsicht

# DrawIO + headless display dependencies + drawio itself in one layer
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates wget xvfb xauth libgbm1 dbus dbus-x11 libx11-xcb1 libxcb-dri3-0 \
    libxkbcommon0 libxcomposite1 libxrandr2 libxdamage1 libxss1 libxtst6 \
    libpangocairo-1.0-0 libatk1.0-0 libatk-bridge2.0-0 libgtk-3-0 libnss3 libasound2 libdrm2

RUN wget "https://github.com/jgraph/drawio-desktop/releases/download/v${DRAWIO_VERSION}/drawio-amd64-${DRAWIO_VERSION}.deb" -O /tmp/drawio.deb \
 && apt-get update \
 && apt-get install -y /tmp/drawio.deb \
 && rm -f /tmp/drawio.deb && rm -rf /var/lib/apt/lists/* \
 && DRAWIO_BIN=$(find /opt /usr/lib /usr/bin -name "drawio" -executable -type f 2>/dev/null | head -1) \
 && echo "drawio binary found at: ${DRAWIO_BIN:-NOT FOUND}" \
 && [ -n "$DRAWIO_BIN" ] && ln -sf "$DRAWIO_BIN" /usr/local/bin/drawio

# Wrapper script so `drawio` runs headless via xvfb with dbus
# -a: auto-pick a free display number (avoids conflicts with existing Xvfb)
# --no-sandbox: required in container environments without user namespaces
# --disable-gpu: required in containers without GPU/rendering backend
# dbus: Electron requires a running system bus for IPC
COPY drawio-export /usr/local/bin/drawio-export
RUN chmod +x /usr/local/bin/drawio-export

WORKDIR /workspace
CMD ["sh", "-c", "echo 'Container Version von bausteinsicht : $APP_VERSION'"]
ENTRYPOINT ["/bin/bash"]
