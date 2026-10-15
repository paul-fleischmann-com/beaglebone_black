# =============================================
# Test-/Build-Container für die ACF-CAN-Pipelines (acfcan-module-build,
# e2e-demo-local-test; Issues #256, #271)
# =============================================
# debian:trixie (nicht bookworm wie generic-builder): netdev_get_by_name()
# gibt es erst ab Kernel 6.5, bookworms Header (6.1-LTS) kompilieren den
# acfcan-Code grundsätzlich nicht (Issue #276).
FROM debian:trixie

ARG VERSION=unknown

LABEL org.opencontainers.image.version=$VERSION
ENV APP_VERSION=$VERSION

# linux-headers-amd64: generische Header für den host-unabhängigen Compile-
# Check (scripts/ci_check_acfcan_compile.sh). Die Header zum exakt laufenden
# Runner-Host-Kernel (linux-headers-$(uname -r)) für build_acfcan_native.sh
# gehören bewusst NICHT ins Image — der Kernel des Hosts steht erst zur
# Laufzeit fest und ändert sich mit jedem Host-Update.
RUN apt-get update && apt-get install -y --no-install-recommends \
    bash \
    build-essential \
    ca-certificates \
    can-utils \
    curl \
    git \
    iproute2 \
    kmod \
    linux-headers-amd64 \
    python3 \
    python3-pip \
    tcpdump \
    && rm -rf /var/lib/apt/lists/*

# Go passend zu project/go-api/go.mod (toolchain go1.26.9), gleiche Quelle
# wie docker/builder/Dockerfile
RUN curl -fsSL https://go.dev/dl/go1.26.9.linux-amd64.tar.gz \
    | tar -C /usr/local -xz

ENV PATH="/usr/local/go/bin:${PATH}"

RUN pip install --no-cache-dir --break-system-packages pytest pytest-timeout
