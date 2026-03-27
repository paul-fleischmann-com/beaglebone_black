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

ARG DRAWIO_VERSION=26.0.4
ARG VERSION=unknown

LABEL org.opencontainers.image.version=$VERSION
ENV APP_VERSION=$VERSION

# Copy compiled binary from builder
COPY --from=builder /usr/local/bin/bausteinsicht /usr/local/bin/bausteinsicht

# DrawIO + headless display dependencies
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget xvfb libgbm1 dbus libx11-xcb1 libxcb-dri3-0 \
    libxkbcommon0 libxcomposite1 libxrandr2 libxdamage1 \
    libasound2 libpangocairo-1.0-0 libatk1.0-0 libcups2 \
    && wget -q "https://github.com/jgraph/drawio-desktop/releases/download/v${DRAWIO_VERSION}/drawio-amd64-${DRAWIO_VERSION}.deb" \
    && dpkg --ignore-scripts -i ./drawio-amd64-${DRAWIO_VERSION}.deb || true \
    && apt-get install -f -y \
    && rm -f drawio-amd64-${DRAWIO_VERSION}.deb \
    && rm -rf /var/lib/apt/lists/*

# drawio-export wrapper script from upstream repo
COPY drawio-export /usr/local/bin/drawio-export
RUN chmod +x /usr/local/bin/drawio-export

WORKDIR /workspace
CMD ["sh", "-c", "echo 'Container Version: $APP_VERSION'"]
ENTRYPOINT ["/bin/bash"]
