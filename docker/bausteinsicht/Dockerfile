# =============================================
# Bausteinsicht CI Container
# Base: Bausteinsicht .devcontainer/Dockerfile
# Extra: DrawIO (headless export), xvfb, dbus
# =============================================
# NOTE: This Dockerfile is NOT used directly.
# Pipeline 9 clones the Bausteinsicht repo and
# builds from .devcontainer/Dockerfile as base,
# then extends it with this file.
# =============================================

ARG BASE_IMAGE=bausteinsicht-base:latest
FROM ${BASE_IMAGE}

ARG DRAWIO_VERSION=26.0.4

# Add DrawIO + headless display dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget xvfb libgbm1 dbus libx11-xcb1 libxcb-dri3-0 \
    && wget -q "https://github.com/jgraph/drawio-desktop/releases/download/v${DRAWIO_VERSION}/drawio-amd64-${DRAWIO_VERSION}.deb" \
    && apt-get install -y ./drawio-amd64-${DRAWIO_VERSION}.deb \
    && rm -f drawio-amd64-${DRAWIO_VERSION}.deb \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace
ENTRYPOINT ["/bin/bash"]
