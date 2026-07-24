SUMMARY = "BeagleBone Black embedded stack (Go REST API + C/Rust HAL libraries)"
DESCRIPTION = "Installs the ARM binaries already cross-compiled by this repo's own \
'make all' pipeline (bin/embedded, libhardware.so, libhardware_rs.so) into the \
Yocto image, plus a systemd unit that starts the REST API on boot. \
Go and Rust are intentionally NOT rebuilt inside bitbake: project/rust-lib \
targets armv7-unknown-linux-musleabihf via 'cross', and project/go-api CGO-links \
against both HAL libraries with the project's own arm-linux-gnueabihf toolchain. \
Re-implementing that in Yocto's rust/go bbclasses (which default to the machine's \
glibc toolchain) would mean maintaining two divergent cross-toolchains for the \
same ABI contract, so the already-verified prebuilt artifacts are packaged as-is."
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COREBASE}/meta/COPYING.MIT;md5=3da9cfbcb788c80a0384361b4de20420"

# Absolute paths to the prebuilt artifacts, set by scripts/build_yocto.sh
# (which runs `make all` before invoking bitbake) via local.conf.
BBB_BIN_DIR ?= ""
BBB_LIBS_DIR ?= ""

SRC_URI = "file://${BBB_BIN_DIR}/embedded;subdir=bbb-bin \
           file://${BBB_LIBS_DIR}/libhardware.so;subdir=bbb-libs \
           file://${BBB_LIBS_DIR}/libhardware_rs.so;subdir=bbb-libs \
           file://bbb-embedded.service"

S = "${WORKDIR}"

INHIBIT_PACKAGE_STRIP = "1"
INSANE_SKIP:${PN} = "already-stripped ldflags file-rdeps"

inherit systemd

SYSTEMD_SERVICE:${PN} = "bbb-embedded.service"
SYSTEMD_AUTO_ENABLE = "enable"

do_install() {
    install -d ${D}${bindir}
    install -m 0755 ${WORKDIR}/bbb-bin/embedded ${D}${bindir}/bbb-embedded

    install -d ${D}${libdir}
    install -m 0755 ${WORKDIR}/bbb-libs/libhardware.so ${D}${libdir}/
    install -m 0755 ${WORKDIR}/bbb-libs/libhardware_rs.so ${D}${libdir}/

    install -d ${D}${systemd_unitdir}/system
    install -m 0644 ${WORKDIR}/bbb-embedded.service ${D}${systemd_unitdir}/system/
}

FILES:${PN} = "${bindir}/bbb-embedded \
               ${libdir}/libhardware.so \
               ${libdir}/libhardware_rs.so \
               ${systemd_unitdir}/system/bbb-embedded.service"
