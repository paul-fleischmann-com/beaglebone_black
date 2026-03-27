# =============================================
# Bausteinsicht CI Container
# Installs bausteinsicht from cloned repo source
# + DrawIO headless export
# =============================================
# Build context must contain:
#   repo-src/   — cloned Bausteinsicht repo
#   drawio-export — wrapper script from repo

FROM python:3.12-slim

ARG DRAWIO_VERSION=26.0.4

# System deps: drawio headless + build tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget xvfb libgbm1 dbus libx11-xcb1 libxcb-dri3-0 \
    libxkbcommon0 libxcomposite1 libxrandr2 libxdamage1 \
    libasound2 libpangocairo-1.0-0 libatk1.0-0 libcups2 \
    gcc python3-dev \
    && wget -q "https://github.com/jgraph/drawio-desktop/releases/download/v${DRAWIO_VERSION}/drawio-amd64-${DRAWIO_VERSION}.deb" \
    && apt-get install -y ./drawio-amd64-${DRAWIO_VERSION}.deb \
    && rm -f drawio-amd64-${DRAWIO_VERSION}.deb \
    && rm -rf /var/lib/apt/lists/*

# Install bausteinsicht from cloned repo source
COPY repo-src/ /opt/bausteinsicht/
RUN pip install --no-cache-dir /opt/bausteinsicht/ \
    && rm -rf /opt/bausteinsicht/

# drawio-export wrapper script from upstream repo
COPY drawio-export /usr/local/bin/drawio-export
RUN chmod +x /usr/local/bin/drawio-export

WORKDIR /workspace
ENTRYPOINT ["/bin/bash"]
