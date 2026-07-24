#!/usr/bin/env bash
# Builds a Yocto (Kirkstone) image for the BeagleBone Black, including the
# project's own meta-bbb-sensors layer (BME280 driver + kernel/DT support).
# Idempotent: re-running skips already-cloned layers and already-registered
# bblayers.conf entries, so it can be used both locally and in CI.
# See issue #250.

set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

YOCTO_DIR=${YOCTO_DIR:-$REPO_ROOT/yocto}
BUILD_DIR=${BUILD_DIR:-$YOCTO_DIR/build-bbb}
DL_DIR=${DL_DIR:-$YOCTO_DIR/downloads}
SSTATE_DIR=${SSTATE_DIR:-$YOCTO_DIR/sstate-cache}
MACHINE=${MACHINE:-beaglebone-yocto}
IMAGE=${IMAGE:-bbb-sensor-image}
YOCTO_BRANCH=${YOCTO_BRANCH:-kirkstone}
META_BBB_SENSORS_DIR="$REPO_ROOT/project/yocto/meta-bbb-sensors"
BBB_BIN_DIR="$REPO_ROOT/bin"
BBB_LIBS_DIR="$REPO_ROOT/project/go-api/libs"

mkdir -p "$YOCTO_DIR"

if [ -f "$BBB_BIN_DIR/embedded" ] && [ -f "$BBB_LIBS_DIR/libhardware.so" ] && [ -f "$BBB_LIBS_DIR/libhardware_rs.so" ]; then
  echo "=== Go/Rust/C-Artefakte bereits vorhanden, überspringe 'make all' ==="
else
  echo "=== Baue Go/Rust/C-Artefakte (make all) ==="
  command -v arm-linux-gnueabihf-gcc >/dev/null 2>&1 || {
    echo "FEHLER: arm-linux-gnueabihf-gcc nicht gefunden (siehe CLAUDE.md Prerequisites)." >&2
    exit 1
  }
  make -C "$REPO_ROOT" all
fi

clone_layer() {
  local name=$1 url=$2
  if [ -d "$YOCTO_DIR/$name" ]; then
    echo "=== $name bereits vorhanden, überspringe Clone ==="
  else
    echo "=== Klone $name ($YOCTO_BRANCH) ==="
    git clone -b "$YOCTO_BRANCH" "$url" "$YOCTO_DIR/$name"
  fi
}

clone_layer poky https://git.yoctoproject.org/poky
clone_layer meta-openembedded https://git.openembedded.org/meta-openembedded
clone_layer meta-arm https://git.yoctoproject.org/meta-arm
clone_layer meta-ti https://git.yoctoproject.org/meta-ti

# shellcheck disable=SC1091
source "$YOCTO_DIR/poky/oe-init-build-env" "$BUILD_DIR"

LOCAL_CONF=conf/local.conf
if ! grep -q "^MACHINE = \"$MACHINE\"" "$LOCAL_CONF" 2>/dev/null; then
  {
    echo "MACHINE = \"$MACHINE\""
    echo "DL_DIR = \"$DL_DIR\""
    echo "SSTATE_DIR = \"$SSTATE_DIR\""
    echo 'INHERIT += "rm_work"'
    echo "BBB_BIN_DIR = \"$BBB_BIN_DIR\""
    echo "BBB_LIBS_DIR = \"$BBB_LIBS_DIR\""
    # bbb-embedded.service (systemd unit) requires systemd as init manager,
    # Poky defaults to sysvinit.
    echo 'DISTRO_FEATURES:append = " systemd"'
    echo 'VIRTUAL-RUNTIME_init_manager = "systemd"'
    echo 'VIRTUAL-RUNTIME_initscripts = ""'
    echo 'VIRTUAL-RUNTIME_syslog = "systemd"'
  } >> "$LOCAL_CONF"
fi

add_layer_once() {
  local layer_path=$1
  if grep -qF "$layer_path" conf/bblayers.conf 2>/dev/null; then
    echo "=== Layer bereits registriert: $layer_path ==="
  else
    bitbake-layers add-layer "$layer_path"
  fi
}

add_layer_once "$YOCTO_DIR/meta-openembedded/meta-oe"
add_layer_once "$YOCTO_DIR/meta-openembedded/meta-python"
add_layer_once "$YOCTO_DIR/meta-openembedded/meta-networking"
add_layer_once "$YOCTO_DIR/meta-arm/meta-arm-toolchain"
add_layer_once "$YOCTO_DIR/meta-arm/meta-arm"
add_layer_once "$YOCTO_DIR/meta-ti/meta-ti-bsp"
add_layer_once "$META_BBB_SENSORS_DIR"

echo "=== Baue $IMAGE für $MACHINE ==="
bitbake "$IMAGE"

echo "=== Fertig. Images unter $BUILD_DIR/tmp/deploy/images/$MACHINE/ ==="
