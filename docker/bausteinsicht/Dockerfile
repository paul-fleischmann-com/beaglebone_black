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
ARG VERSION=unknown

LABEL org.opencontainers.image.version=$VERSION
ENV APP_VERSION=$VERSION

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
RUN echo "=== Repo root ===" && ls -la /opt/bausteinsicht/ \
    && echo "=== Hidden files ===" && ls -la /opt/bausteinsicht/.* 2>/dev/null || true \
    && echo "=== package files ===" && find /opt/bausteinsicht -maxdepth 2 \
       \( -name "*.toml" -o -name "*.cfg" -o -name "setup.py" \
          -o -name "Makefile" -o -name "*.json" -o -name "requirements*.txt" \
          -o -name "install.sh" -o -name "gradlew" \) | sort

# drawio-export wrapper script from upstream repo
COPY drawio-export /usr/local/bin/drawio-export
RUN chmod +x /usr/local/bin/drawio-export

WORKDIR /workspace
CMD ["sh", "-c", "echo 'Container Version: $APP_VERSION'"]
ENTRYPOINT ["/bin/bash"]
