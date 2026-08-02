SUMMARY = "MKA-Daemon (MACsec Key Agreement, IEEE 802.1X-2020) für die MACsec-Absicherung der ACF-CAN-Demo"
DESCRIPTION = "Baut mkad (Technica-Engineering/MKAdaemon, GPLv2) für die \
BeagleBone Black. Handelt über EAPOL-Frames auf einem physischen Ethernet-\
Interface einen Session Key (SAK) aus und konfiguriert dabei automatisch ein \
Linux-Kernel-MACsec-Interface (CONFIG_MACSEC, siehe bbb-macsec.cfg) — die \
ACF-CAN-Nutzdaten aus #256/#257/#259 laufen dann verschlüsselt statt über das \
rohe Ethernet-Interface. DBus-Steuerschnittstelle bewusst deaktiviert \
(DISABLE_DBUS=1) — für dieses Projekt reicht die feste YAML-Konfiguration \
(siehe mkad-board.conf.example), das spart glib/gio/libxml2 als \
Cross-Build-Abhängigkeiten. Siehe Issue #260."
HOMEPAGE = "https://github.com/Technica-Engineering/MKAdaemon"
SECTION = "network"

LICENSE = "GPL-2.0-or-later"
LIC_FILES_CHKSUM = "file://COPYING.txt;md5=75859989545e37968a99b631ef42722e"

DEPENDS = "openssl libyaml libbsd libnl"

inherit waf

SRC_URI = "git://github.com/Technica-Engineering/MKAdaemon.git;branch=main;protocol=https"
SRCREV = "23c987f9c3b531bf6912e2018269ced0b5189ecd"

S = "${WORKDIR}/git"

COMPATIBLE_MACHINE = "beaglebone-yocto"

do_configure:prepend() {
    export DISABLE_DBUS=1
}
do_compile:prepend() {
    export DISABLE_DBUS=1
}

do_install() {
    install -d ${D}${bindir}
    install -m 0755 ${B}/mkad ${D}${bindir}/mkad
    install -m 0755 ${B}/mkad_cli ${D}${bindir}/mkad_cli
}

FILES:${PN} = "${bindir}/mkad ${bindir}/mkad_cli"

# Dieselbe Begründung wie bei pru-fw_1.0.bb/acfcan-mod_1.0.bb: eingebettete
# Build-Pfade im Binary sind für diesen Anwendungsfall unkritisch.
INSANE_SKIP:${PN} = "buildpaths"
