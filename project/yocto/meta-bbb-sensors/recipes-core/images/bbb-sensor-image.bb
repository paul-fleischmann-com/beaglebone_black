SUMMARY = "core-image-minimal + BME280 sensor support for the BeagleBone Black"

require recipes-core/images/core-image-minimal.bb

IMAGE_INSTALL:append = " bme280-driver bbb-bme280-overlay i2c-tools"
