# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Embedded software project for the **BeagleBone Black** (ARM Cortex-A8, 512MB RAM). Provides hardware drivers (BME280, GPIO, UART, SPI) through a layered architecture: hardware access in C/Rust → HAL in Go → REST API on port 5000 → client tools (CLI, TUI, GUI, Web).

**Rule:** Hardware access is only implemented in C and Rust — never in Go directly.

## Build Commands

```bash
make all          # Build C lib + Rust lib + Go API
make c-lib        # Build C shared library (libhardware.so)
make rust-lib     # Build Rust shared library (libhardware_rs.so)
make go-api       # Build REST API server → bin/embedded
make cli          # Build CLI tool → bin/bbcli-*
make test         # Run Go unit tests
make deploy       # Deploy to BeagleBone (debian@192.168.7.2)
make yocto-image  # Build Yocto (Kirkstone) image incl. BME280 layer
make pru-fw       # Build PRU1-RPMsg-GPIO-Firmware → bin/pru/bbb-pru1-gpio-ctrl.elf
make acfcan-mod   # Build Open1722 ACF-CAN kernel module → bin/kernel/bbb-acfcan.ko
make open1722-userspace  # Build Open1722 ACF-CAN/CVF user-space tools → bin/open1722/
make clean        # Clean all artifacts
```

**Cross-compilation targets:**
- Go: `GOOS=linux GOARCH=arm GOARM=7 CGO_ENABLED=1`
- Rust: `armv7-unknown-linux-musleabihf`
- C: `arm-linux-gnueabihf` cross-compiler

## Testing

```bash
# Go unit tests (HAL with mock driver)
cd go-api && go test ./pkg/hal/... -v
cd go-api && go test ./pkg/hal/... -race -count=3

# API integration tests
pytest tests/api/ -v

# Hardware tests (requires real BeagleBone at 192.168.7.2)
BEAGLE_HOST=192.168.7.2 pytest tests/hardware/ -v

# Test all backends
for b in c rust auto; do HW_BACKEND=$b pytest tests/hardware/ -v; done

# PRU-Backend (nur GPIO, siehe Issue #252)
HW_BACKEND=pru pytest tests/hardware/test_pru.py -v

# Open1722-ACF-CAN-Kernel-Modul (kein HAL-Backend, siehe Issue #256)
BEAGLE_HOST=192.168.7.2 pytest tests/hardware/test_acfcan.py -v
```

Quality gates: ≥90% test success rate, ≥75% average coverage, ≥50% per file.

## Architecture

```
Client Tools (CLI/TUI/GUI/Web)
        ↓
REST API Server (project/go-api/cmd/main.go, :5000)
        ↓
HAL Interface (project/go-api/pkg/hal/interface.go)
    ↙        ↘         ↘            ↘
C Driver   Rust Driver  PRU Driver   Mock Driver (tests only)
(CGO)      (FFI)        (CGO, RPMsg)
    ↘        ↙            ↓
Hardware (BME280/GPIO/UART/SPI)   PRU-ICSS (R30/R31-GPIO, siehe #252)
```

**HAL Backends** — selected via `HW_BACKEND` env var:
- `c` — calls C shared library via CGO
- `rust` — calls Rust shared library via FFI
- `auto` — tries C first, falls back to Rust on error (default in production)
- `pru` — PRU1 via RPMsg (deterministisches GPIO, R30/R31-Bit 0-15 statt Linux-Sysfs-GPIO-Nummer; BME280/UART/SPI nicht unterstützt, siehe Issue #252)

**Open1722-ACF-CAN-Kernel-Modul** (`acfcan`, Issue #256) — kein HAL-Backend,
sondern ein eigenständiges Linux-Kernel-Netzwerkmodul unterhalb von
HAL/REST-API: tunnelt SocketCAN-Frames transparent als
IEEE-1722-ACF_CAN-Nachrichten über Ethernet (`cansend`/`candump` funktionieren
unverändert). Wird per `ip link ... type acfcan` + sysfs unter
`/sys/class/net/<dev>/acfcan/` angesprochen, nicht über `:5000/api/v1/*`.

The `HardwareDriver` interface in `project/go-api/pkg/hal/interface.go` defines all hardware operations. New hardware features must be added to all backend drivers (C, Rust, Mock; PRU nur soweit PRU-seitig sinnvoll, sonst "nicht unterstützt"-Fehler) plus the interface.

## Key Files

| File | Purpose |
|------|---------|
| `project/go-api/cmd/main.go` | HTTP server entry, routes, middleware |
| `project/go-api/pkg/hal/interface.go` | `HardwareDriver` interface definition |
| `project/go-api/pkg/hal/factory.go` | Backend selection logic (c/rust/auto) |
| `project/go-api/pkg/hal/hal_test.go` | Unit tests using mock driver |
| `project/go-api/pkg/hal/c/driver.go` | CGO bindings to C library |
| `project/go-api/pkg/hal/rust/driver.go` | FFI bindings to Rust library |
| `project/go-api/pkg/hal/mock/driver.go` | Test mock — no hardware needed |
| `project/c/include/` | C headers for all hardware interfaces |
| `project/c/test/` | C unit tests (CI-compatible error-path tests) |
| `project/rust-lib/src/lib.rs` | Rust FFI exports |
| `project/go-api/pkg/hal/pru/driver.go` | CGO bindings to PRU RPMsg comm layer (GPIO only) |
| `project/c/src/pru.c` | remoteproc-sysfs load/stop + rpmsg-chardev discovery/command |
| `project/pru/fw/pru1_gpio_ctrl/` | PRU1 firmware (RPMsg GPIO SET/GET on R30/R31), built with the GNU-PRU toolchain |
| `scripts/setup_pru_toolchain.sh` / `scripts/build_pru_firmware.sh` | Fetch GNU-PRU toolchain + PSSP, build the PRU1 firmware |
| `scripts/setup_open1722.sh` / `scripts/build_open1722_acfcan.sh` | Fetch COVESA/Open1722, cross-build the `acfcan` ACF-CAN kernel module (Issue #256) |
| `project/yocto/meta-bbb-sensors/recipes-bbb/acfcan-mod/` | Yocto recipe for the `acfcan` kernel module |
| `tests/hardware/test_acfcan.py` | ACF-CAN tunneling test (SSH-driven, single-board `veth` setup) |
| `scripts/build_open1722_userspace.sh` | Cross-builds Open1722 user-space demo tools (acf-can-talker/-listener/-bridge, cvf-talker/-listener), Issue #257 |
| `tools/cli/cmd/acfcan.go` | `bbcli acf-can bridge start/stop/status` — manages the local acf-can-bridge process (no REST API involved) |
| `scripts/setup_acfcan_vcan_demo.sh` | BBB-side of the vcan→Eth→container demo (Issue #259): vcan0 + frame generator + acf-can-talker |
| `tools/acfcan-viewer/` | Container: Open1722 ETH-node receiver (acf-can-listener) + live web dashboard (Issue #259) |
| `project/macsec/mkad-board.conf` / `scripts/setup_macsec_mka.sh` | mkad (MACsec Key Agreement) config + BBB-side startup script (Issue #260) |
| `project/yocto/meta-bbb-sensors/recipes-bbb/mkad/` | Yocto recipe for mkad (Technica-Engineering/MKAdaemon, waf-based) |
| `project/go-api/pkg/e2edemo/` | Minimal CAN request/response protocol + CGO-free SocketCAN wrapper for the E2E demo (Issue #270) |
| `project/go-api/cmd/rest-can-gateway/` | D2: `GET /temperature` REST↔CAN gateway of the E2E demo (Issue #270) |
| `project/go-api/cmd/can-hal-bridge/` | D5: CAN→HAL bridge of the E2E demo — mock HAL default, real hardware via `-tags hwreal` (Issue #270) |
| `scripts/setup_e2e_demo.sh` | Builds the 5-namespace REST→CAN→ACF-CAN→CAN→BME280 demo topology in one go (Issue #270) |
| `tests/hardware/test_e2e_demo.py` | End-to-end round-trip test for the Issue #270 demo (SSH-driven, single-board namespace setup) |
| `.drone.yml` | 21 CI/CD pipelines |
| `scripts/build_yocto.sh` | Builds Yocto (Kirkstone) image for BBB incl. `meta-bbb-sensors` layer |
| `project/yocto/meta-bbb-sensors/` | Yocto layer: BME280 driver, PRUSS DT overlay + firmware recipe, kernel/DT enablement, prebuilt Go/Rust/C stack |

## Dependencies

**Go** (`project/go-api/go.mod`): `gorilla/mux`, `spf13/cobra`, `spf13/viper`, `charmbracelet/bubbletea`, `fyne.io/fyne/v2`

**Rust** (`project/rust-lib/Cargo.toml`): `linux-embedded-hal`, `bme280`, `serialport`, `spidev`, `cbindgen`

## Prerequisites

```bash
# ARM cross-compiler
sudo apt install gcc-arm-linux-gnueabihf make

# Rust cross-compilation
cargo install cross cbindgen

# Python tests
pip3 install pytest requests pytest-json-report
```

## Code Style

- Go formatting: `gofmt -w .`
- Commit format: `type(scope): description` (feat, fix, docs, test, refactor, ci)
