# =============================================
# Bausteinsicht CI Container
# Pre-installed: bausteinsicht, DrawIO, xvfb
# =============================================
FROM debian:bookworm

ARG DRAWIO_VERSION=26.0.4

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl wget jq git ca-certificates \
    xvfb libgbm1 dbus \
    libx11-xcb1 libxcb-dri3-0 \
    && rm -rf /var/lib/apt/lists/*

# Pre-install DrawIO (pinned version — update ARG to upgrade)
RUN wget -q "https://github.com/jgraph/drawio-desktop/releases/download/v${DRAWIO_VERSION}/drawio-amd64-${DRAWIO_VERSION}.deb" \
    && apt-get update && apt-get install -y ./drawio-amd64-${DRAWIO_VERSION}.deb \
    && rm -f drawio-amd64-${DRAWIO_VERSION}.deb \
    && rm -rf /var/lib/apt/lists/*

# Install bausteinsicht from GitHub releases
RUN BAUSTEINSICHT_VERSION=$(curl -sSf https://api.github.com/repos/docToolchain/Bausteinsicht/releases/latest \
        | jq -r '.tag_name') \
    && curl -sSfL "https://github.com/docToolchain/Bausteinsicht/releases/download/${BAUSTEINSICHT_VERSION}/bausteinsicht-linux-amd64.tar.gz" \
        | tar -xz -C /usr/local/bin \
    && chmod +x /usr/local/bin/bausteinsicht

WORKDIR /workspace
ENTRYPOINT ["/bin/bash"]
