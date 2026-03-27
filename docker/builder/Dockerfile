# =============================================
# BBB Cross-Compile & Test Builder Container
# Supports C, Rust, Go, Python
# =============================================
# previous : debian:12-slim
FROM debian:bookworm

ARG VERSION=unknown

LABEL org.opencontainers.image.version=$VERSION
ENV APP_VERSION=$VERSION

# ----------------------------
# Install basic packages
# ----------------------------
RUN dpkg --add-architecture armhf

RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    curl \
    git \
    bash \
    ca-certificates \
    pkg-config \
    python3 \
    python3-pip \
    python3-setuptools \
    python3-venv \
    unzip \
    gcc-arm-linux-gnueabihf \
    g++-arm-linux-gnueabihf \
    libc6-dev-armhf-cross \
    libudev-dev \
    libudev-dev:armhf \
    lcov \
    && rm -rf /var/lib/apt/lists/*

# ----------------------------
# Install Go (official binary)
# ----------------------------
RUN curl -fsSL https://go.dev/dl/go1.24.1.linux-amd64.tar.gz \
    | tar -C /usr/local -xz

ENV PATH="/usr/local/go/bin:${PATH}"

# Install gotestsum for JUnit XML test output + gocover-cobertura for coverage reports
RUN GOPATH=/usr/local go install gotest.tools/gotestsum@latest && \
    GOPATH=/usr/local go install github.com/boumenot/gocover-cobertura@latest
# ----------------------------
# Install Rust + ARM Target
# ----------------------------
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

# Add ARMv7 target
RUN rustup target add armv7-unknown-linux-gnueabihf

# Create Cargo config for cross-linker
RUN mkdir -p /root/.cargo && \
    echo '[target.armv7-unknown-linux-gnueabihf]' > /root/.cargo/config.toml && \
    echo 'linker = "arm-linux-gnueabihf-gcc"' >> /root/.cargo/config.toml

# --- Python Test Tools ---
# Erstelle venv
RUN python3 -m venv /opt/venv

# Aktivieren der venv und pytest installieren
RUN /opt/venv/bin/pip install --upgrade pip && \
    /opt/venv/bin/pip install pytest coverage gcovr

# PATH anpassen
ENV PATH="/opt/venv/bin:$PATH"



# ----------------------------
# Set working directory
# ----------------------------
WORKDIR /workspace

CMD ["sh", "-c", "echo 'Container Version: $APP_VERSION'"]
ENTRYPOINT ["/bin/bash"]