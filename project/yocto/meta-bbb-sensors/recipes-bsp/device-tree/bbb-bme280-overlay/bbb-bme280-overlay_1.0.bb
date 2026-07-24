SUMMARY = "Devicetree overlay enabling I2C1 + BME280@0x76 on the BeagleBone Black"
DESCRIPTION = "Compiles bbb-bme280.dts into a .dtbo cape overlay and installs it \
to /boot/overlays so u-boot can load it via the extlinux 'fdtoverlays' variable."
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COREBASE}/meta/COPYING.MIT;md5=3da9cfbcb788c80a0384361b4de20420"

SRC_URI = "file://bbb-bme280.dts"

S = "${WORKDIR}"

DEPENDS = "dtc-native"

COMPATIBLE_MACHINE = "beaglebone-yocto"

do_compile() {
    dtc -@ -I dts -O dtb -o ${S}/BBB-BME280-I2C1-00A0.dtbo ${S}/bbb-bme280.dts
}

do_install() {
    install -d ${D}/boot/overlays
    install -m 0644 ${S}/BBB-BME280-I2C1-00A0.dtbo ${D}/boot/overlays/
}

FILES:${PN} = "/boot/overlays/BBB-BME280-I2C1-00A0.dtbo"

INSANE_SKIP:${PN} = "arch"
