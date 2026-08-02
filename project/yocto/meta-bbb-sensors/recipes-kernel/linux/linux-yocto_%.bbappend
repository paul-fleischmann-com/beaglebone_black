FILESEXTRAPATHS:prepend := "${THISDIR}/files:"

SRC_URI:append = " file://bbb-bme280.cfg file://bbb-pruss.cfg file://bbb-can.cfg file://bbb-macsec.cfg"
