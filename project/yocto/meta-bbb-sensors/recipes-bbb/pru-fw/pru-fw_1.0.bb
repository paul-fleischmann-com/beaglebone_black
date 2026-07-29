SUMMARY = "PRU1 RPMsg-GPIO-Kommandofirmware für die BeagleBone-Black-PRU-ICSS"
DESCRIPTION = "Cross-baut project/pru/fw/pru1_gpio_ctrl mit der GNU-PRU-Toolchain \
(dinuxbg/gnupru) gegen die GCC-portierte pru-software-support-package und \
installiert die resultierende ELF-Firmware nach /lib/firmware, damit remoteproc \
sie laden kann (project/c/src/pru.c setzt den Dateinamen zur Laufzeit über \
Sysfs). Toolchain und PSSP werden als SRC_URI zur Fetch-Zeit geladen — kein \
Netzwerkzugriff in do_compile (Yocto-Netzwerk-Sandbox-konform). Voraussetzung: \
x86_64-Build-Host (nur dafür liefert dinuxbg/gnupru ein Prebuilt-Release). \
Siehe Issue #252."
HOMEPAGE = "https://github.com/paul-fleischmann-com/beaglebone_black"
SECTION = "kernel"

LICENSE = "BSD-3-Clause"
LIC_FILES_CHKSUM = "file://main.c;beginline=1;endline=30;md5=3c3cb8a6c1066a27e8d54b11a1f16093"

GNUPRU_VERSION = "2026.05"

SRC_URI = "git://github.com/paul-fleischmann-com/beaglebone_black.git;branch=main;protocol=https;name=repo;destsuffix=git \
           git://github.com/dinuxbg/pru-software-support-package.git;branch=master;protocol=https;name=pssp;destsuffix=pssp \
           https://github.com/dinuxbg/gnupru/releases/download/${GNUPRU_VERSION}/pru-elf-${GNUPRU_VERSION}.amd64.tar.xz;name=toolchain"

SRCREV_repo = "${AUTOREV}"
SRCREV_pssp = "f7f23b449532bbe6c464347e4d2e26df374e0a9a"
SRC_URI[toolchain.sha256sum] = "6437678b635428fad58813ed7df8defd121efbfec746468755516c58074a7fad"

UPSTREAM_CHECK_COMMITS = "1"

S = "${WORKDIR}/git/project/pru/fw/pru1_gpio_ctrl"
PSSP_DIR = "${WORKDIR}/pssp"
PRU_GCC_BIN = "${WORKDIR}/pru-elf/bin"

COMPATIBLE_MACHINE = "beaglebone-yocto"

do_compile() {
    ${PRU_GCC_BIN}/pru-gcc -g -Os -Wall -Wextra -Wno-array-bounds \
        -I${PSSP_DIR}/include -I${PSSP_DIR}/include/am335x \
        -I${S}/../../../c/include \
        -minrt -mmcu=am335x.pru1 \
        ${S}/main.c \
        ${PSSP_DIR}/lib/src/rpmsg_lib/pru_rpmsg.c \
        ${PSSP_DIR}/lib/src/rpmsg_lib/pru_virtqueue.c \
        -o ${B}/bbb-pru1-gpio-ctrl.elf
}

do_install() {
    install -d ${D}${nonarch_base_libdir}/firmware
    install -m 0644 ${B}/bbb-pru1-gpio-ctrl.elf ${D}${nonarch_base_libdir}/firmware/
}

FILES:${PN} = "${nonarch_base_libdir}/firmware/bbb-pru1-gpio-ctrl.elf"

# PRU-ELF ist keine ARM-Zielarchitektur — QA-Checks für Zielarchitektur/
# Hardening-Flags/eingebettete Build-Pfade greifen hier nicht.
INSANE_SKIP:${PN} = "arch ldflags buildpaths"
