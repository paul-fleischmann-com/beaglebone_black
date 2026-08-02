SUMMARY = "bbb-sensor-image + the prebuilt Go REST API / HAL stack (bbb-embedded)"
DESCRIPTION = "Requires bin/embedded, libhardware.so and libhardware_rs.so to \
already exist (see scripts/build_yocto.sh, which runs 'make all' first). Used \
by the Drone CI pipeline build-yocto-image; the lighter bbb-sensor-image is \
the default for local/GH-Actions builds that only need the BME280 layer."

require recipes-core/images/bbb-sensor-image.bb

IMAGE_INSTALL:append = " bbb-embedded pru-fw bbb-pruss-overlay acfcan-mod kernel-module-can kernel-module-can-raw"
