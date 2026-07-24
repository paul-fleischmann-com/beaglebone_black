SUMMARY = "BME280 sensor driver + smoke-test binary for the BeagleBone Black"
DESCRIPTION = "Cross-builds the project's own C BME280 driver (project/c) as a \
target shared library plus a smoke-test binary, so BME280 support (I2C-1, \
address 0x76) is available in the Yocto image without duplicating driver code."
HOMEPAGE = "https://github.com/paul-fleischmann-com/beaglebone_black"
SECTION = "libs"

LICENSE = "BSD-3-Clause"
LIC_FILES_CHKSUM = "file://include/bme280.h;beginline=1;endline=37;md5=acdc1390c5df5a01e4ece0ccd5673751"

SRC_URI = "git://github.com/paul-fleischmann-com/beaglebone_black.git;branch=main;protocol=https"
SRCREV = "${AUTOREV}"

S = "${WORKDIR}/git/project/c"

DEPENDS = ""
INSANE_SKIP:${PN} = "ldflags"

do_compile() {
    ${CC} ${CFLAGS} -shared -fPIC \
        -o ${B}/libhardware_bme280.so \
        src/bme280.c \
        -I include ${LDFLAGS} -lm

    ${CC} ${CFLAGS} \
        -o ${B}/bme280_smoke \
        test/bbb_smoke.c \
        -I include \
        -L ${B} -lhardware_bme280 ${LDFLAGS} -lm
}

do_install() {
    install -d ${D}${libdir}
    install -m 0755 ${B}/libhardware_bme280.so ${D}${libdir}/

    install -d ${D}${bindir}
    install -m 0755 ${B}/bme280_smoke ${D}${bindir}/

    install -d ${D}${includedir}/bbb
    install -m 0644 include/bme280.h include/bme280_defs.h include/common.h ${D}${includedir}/bbb/
}

FILES:${PN} = "${libdir}/libhardware_bme280.so ${bindir}/bme280_smoke"
FILES:${PN}-dev = "${includedir}/bbb"

RDEPENDS:${PN} = "i2c-tools"
