# =============================================
# BBB Cross-Compile & Test Builder Container
# Supports C, Rust, Go, Python
# =============================================
FROM debian:12-slim

# ----------------------------
# Install basic packages
# ----------------------------
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
    unzip \
    gcc-arm-linux-gnueabihf \
    g++-arm-linux-gnueabihf \
    libc6-dev-armhf-cross \
    golang \
    && rm -rf /var/lib/apt/lists/*

    

ENV PATH="/usr/local/go/bin:${PATH}"
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
# Installiere venv falls noch nicht vorhanden
RUN apt-get update && apt-get install -y python3-venv python3-pip

# Erstelle venv
RUN python3 -m venv /opt/venv

# Aktivieren der venv und pytest installieren
RUN /opt/venv/bin/pip install --upgrade pip && \
    /opt/venv/bin/pip install pytest

# PATH anpassen
ENV PATH="/opt/venv/bin:$PATH"



# ----------------------------
# Set working directory
# ----------------------------
WORKDIR /workspace

# ----------------------------
# Entrypoint to allow arbitrary commands
# ----------------------------
ENTRYPOINT ["/bin/bash"]