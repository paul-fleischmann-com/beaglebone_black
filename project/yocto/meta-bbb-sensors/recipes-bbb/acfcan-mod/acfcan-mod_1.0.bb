SUMMARY = "Open1722 ACF-CAN Linux-Kernel-Modul (virtuelles SocketCAN-Interface über IEEE-1722/ACF-CAN)"
DESCRIPTION = "Baut das acfcan-Kernel-Modul aus COVESA/Open1722 \
(examples/acf-can/linux-kernel-mod) gegen den Yocto-Kernel-Quellbaum. Aus \
User-Space-Sicht verhält sich ein acfcan-Netzwerkinterface wie ein normales \
SocketCAN-Interface (cansend/candump funktionieren unverändert) — dahinter \
tunnelt das Modul die CAN-Frames als IEEE-1722-ACF_CAN-Nachrichten über ein \
Ethernet-Interface. Voraussetzung zur Laufzeit: CAN-Subsystem geladen \
(modprobe can) vor insmod, sonst fehlen beim ersten Laden Symbole. Siehe \
Issue #256, Doku-Quelle: \
website/site/content/autosar/IEEE1722Transport/ieee1722-teil-5-beaglebone-praxisprojekt.adoc."
HOMEPAGE = "https://github.com/COVESA/Open1722"
SECTION = "kernel/modules"

# Datei-Header ist dual-lizenziert: BSD-3-Clause-artige Klausel ODER GPLv2 als
# Alternative. Modul deklariert im Original kein MODULE_LICENSE() (siehe
# Patch 0001) — für das Kernel-Modul selbst wird hier bewusst die
# GPL-Alternative gewählt, da mehrere genutzte CAN-Subsystem-Funktionen
# (linux/can/dev.h) GPL-only exportiert sind.
LICENSE = "BSD-3-Clause | GPL-2.0-only"
LIC_FILES_CHKSUM = "file://acfcanmain.c;beginline=1;endline=38;md5=ed6f0e1a488c93a1b58b060ddc4b158f"

inherit module-base

SRC_URI = "git://github.com/COVESA/Open1722.git;branch=main;protocol=https;destsuffix=git \
           file://0001-add-module-license-gpl.patch"

# Gepinnt auf denselben Commit wie scripts/setup_open1722.sh (OPEN1722_REV),
# damit lokaler Build und Yocto-Recipe-Build identischen Code verwenden.
SRCREV = "8535cfd63da7a71ec1169d122b2c6d081b28e75b"

UPSTREAM_CHECK_COMMITS = "1"

S = "${WORKDIR}/git"
MOD_DIR = "${S}/examples/acf-can/linux-kernel-mod"

COMPATIBLE_MACHINE = "beaglebone-yocto"

EXTRA_OEMAKE = "CONFIG_ACF_CAN=m"

# Kein `inherit module` (voller module.bbclass), weil das Open1722-eigene
# Makefile keine KERNEL_SRC/KERNEL_PATH-Variable honoriert — die Upstream-
# `all:`-Regel baut immer hart gegen den *laufenden* Host-Kernel
# (/lib/modules/$(uname -r)/build). Stattdessen direkter Kbuild-Aufruf gegen
# den Yocto-Kernel-Baum, analog scripts/build_open1722_acfcan.sh.
do_compile() {
    unset CFLAGS CPPFLAGS CXXFLAGS LDFLAGS
    oe_runmake -C ${STAGING_KERNEL_DIR} M=${MOD_DIR} \
        O=${STAGING_KERNEL_BUILDDIR} \
        CC="${KERNEL_CC}" LD="${KERNEL_LD}" \
        ${EXTRA_OEMAKE} modules
}

do_install() {
    install -d ${D}${nonarch_base_libdir}/modules/${KERNEL_VERSION}/extra
    install -m 0644 ${MOD_DIR}/acfcan.ko \
        ${D}${nonarch_base_libdir}/modules/${KERNEL_VERSION}/extra/acfcan.ko
}

FILES:${PN} = "${nonarch_base_libdir}/modules/${KERNEL_VERSION}/extra/acfcan.ko"
RDEPENDS:${PN} += "kernel-module-can kernel-module-can-raw kernel-module-can-dev"

# Kernel-Modul, keine ARM-Userspace-Binärdatei im klassischen Sinn — dieselbe
# Begründung wie bei pru-fw_1.0.bb (dort PRU-ELF statt ARM) trifft hier auf
# den QA-Check für eingebettete Build-Pfade im generierten .ko zu.
INSANE_SKIP:${PN} = "buildpaths"
