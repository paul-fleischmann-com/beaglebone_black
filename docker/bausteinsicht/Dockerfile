# =============================================
# Bausteinsicht CI Container (multi-stage)
# Stage 1: compile Go binary from repo source
# Stage 2: slim runtime + DrawIO headless
# =============================================
# Build context must contain:
#   repo-src/     — cloned Bausteinsicht repo
#   drawio-export — wrapper script from .devcontainer/

# ── Stage 1: Build ────────────────────────────────
FROM golang:1.24 AS builder

WORKDIR /src
COPY repo-src/ .
RUN go build -o /usr/local/bin/bausteinsicht ./cmd/...

# ── Stage 2: Runtime ──────────────────────────────
FROM debian:bookworm

ARG DRAWIO_VERSION=29.5.2
ARG VERSION=unknown

LABEL org.opencontainers.image.version=$VERSION
ENV APP_VERSION=$VERSION

# Copy compiled binary from builder
COPY --from=builder /usr/local/bin/bausteinsicht /usr/local/bin/bausteinsicht

# DrawIO + headless display dependencies
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget xvfb xauth libgbm1 dbus libx11-xcb1 libxcb-dri3-0 \
    libxkbcommon0 libxcomposite1 libxrandr2 libxdamage1 \
    libasound2 libpangocairo-1.0-0 libatk1.0-0 libcups2

ARG DRAWIO_VERSION=29.5.2
RUN wget -q "https://github.com/jgraph/drawio-desktop/releases/download/v${DRAWIO_VERSION}/drawio-amd64-${DRAWIO_VERSION}.deb" -O /tmp/drawio.deb \
    && apt-get install -y --no-install-recommends /tmp/drawio.deb \
    && rm -f /tmp/drawio.deb && rm -rf /var/lib/apt/lists/*

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
