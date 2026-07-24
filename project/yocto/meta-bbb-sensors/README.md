# meta-bbb-sensors

Yocto (Kirkstone) BSP layer providing BME280 sensor support for the
BeagleBone Black embedded project. Built by `scripts/build_yocto.sh`
(see issue #250).

## Contents

| Recipe | Purpose |
|---|---|
| `recipes-bbb/bme280-driver` | Cross-builds `project/c` BME280 driver as `libhardware_bme280.so` + `bme280_smoke` binary |
| `recipes-bbb/bbb-embedded` | Packages the prebuilt `bin/embedded` Go REST API + `libhardware.so`/`libhardware_rs.so` (built by `make all`) and a systemd unit that starts it on boot |
| `recipes-kernel/linux/linux-yocto_%.bbappend` | Kernel config fragment enabling `CONFIG_BMP280`/`CONFIG_BMP280_I2C` (covers BME280) |
| `recipes-bsp/device-tree/bbb-bme280-overlay` | Devicetree overlay enabling I2C1 + BME280@0x76 (`/boot/overlays/BBB-BME280-I2C1-00A0.dtbo`) |
| `recipes-core/images/bbb-sensor-image.bb` | `core-image-minimal` + the packages above |

### Why `bbb-embedded` ships prebuilt binaries instead of a Yocto-native Go/Rust build

`project/rust-lib` cross-compiles for `armv7-unknown-linux-musleabihf` via `cross`, and
`project/go-api` CGO-links against both HAL libraries using the project's own
`arm-linux-gnueabihf-gcc` toolchain (see `Makefile`). Rebuilding the same crate/module
inside bitbake's `cargo`/`go` classes would target the machine's glibc toolchain instead —
a second, divergent cross-toolchain building the same ABI contract. `scripts/build_yocto.sh`
therefore runs `make all` first and the `bbb-embedded` recipe just installs the resulting,
already-verified artifacts.

## Usage

The layer is added automatically by `scripts/build_yocto.sh`. To add it
manually to an existing Yocto build:

```bash
bitbake-layers add-layer /path/to/project/yocto/meta-bbb-sensors
bitbake bbb-sensor-image
```

To activate the overlay at boot, add to `/boot/uEnv.txt` (or the
extlinux config, depending on u-boot version):

```
fdtoverlays /boot/overlays/BBB-BME280-I2C1-00A0.dtbo
```
