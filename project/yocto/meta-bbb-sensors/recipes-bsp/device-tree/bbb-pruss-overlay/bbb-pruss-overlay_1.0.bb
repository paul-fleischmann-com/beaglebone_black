SUMMARY = "Devicetree overlay enabling PRUSS/PRU0/PRU1 remoteproc cores on the BeagleBone Black"
DESCRIPTION = "Compiles bbb-pruss.dts into a .dtbo cape overlay and installs it \
to /boot/overlays so u-boot can load it via the extlinux 'fdtoverlays' variable. \
Enables the ti,am3356-pruss/ti,am3356-pru remoteproc nodes needed by \
project/pru/fw/pru1_gpio_ctrl (see Issue #252)."
LICENSE = "GPL-2.0-only"
LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/GPL-2.0-only;md5=801f80980d171dd6425610833a22dbe6"

SRC_URI = "file://bbb-pruss.dts"

S = "${WORKDIR}"

DEPENDS = "dtc-native"

COMPATIBLE_MACHINE = "beaglebone-yocto"

do_compile() {
    dtc -@ -I dts -O dtb -o ${S}/BBB-PRUSS-00A0.dtbo ${S}/bbb-pruss.dts
}

do_install() {
    install -d ${D}/boot/overlays
    install -m 0644 ${S}/BBB-PRUSS-00A0.dtbo ${D}/boot/overlays/
}

FILES:${PN} = "/boot/overlays/BBB-PRUSS-00A0.dtbo"

INSANE_SKIP:${PN} = "arch"
