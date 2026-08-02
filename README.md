# 🤖 BeagleBone Black Embedded SW

[![CI Status](https://drone.example.com/api/badges/user/beaglebone/status.svg)](https://drone.example.com/user/beaglebone)
[![Go Version](https://img.shields.io/badge/Go-1.22-00ADD8?logo=go)](https://go.dev)
[![Rust Version](https://img.shields.io/badge/Rust-1.77-orange?logo=rust)](https://www.rust-lang.org)
[![License](https://img.shields.io/badge/License-MIT-blue)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-ARMv7%20Cortex--A8-green)](https://beagleboard.org/black)

Mehrschichtige Embedded-SW für den **BeagleBone Black (TI AM335x, ARMv7 Cortex-A8, 1GHz, 512MB RAM)**.  
Verbindet hardware-nahe **C** und **Rust** Bibliotheken über einen **HAL-Wrapper** mit einer **Go REST API** und mehreren Client-Tools.

---

## 📐 Architektur

```
┌─────────────────────────────────────────────────────┐
│              CLIENT LAYER                           │
│  Web GUI  │  Desktop GUI  │  TUI  │  CLI (bbcli)   │
└──────────────────┬──────────────────────────────────┘
                   │ HTTP/REST + SSE
┌──────────────────▼──────────────────────────────────┐
│              API LAYER  (Go :5000)                  │
│  BME280 │ GPIO │ UART │ SPI │ Backend │ Health      │
└──────────────────┬──────────────────────────────────┘
                   │ Go Interface
┌──────────────────▼──────────────────────────────────┐
│              HAL LAYER                              │
│  C Driver (CGO)  │  Rust Driver (FFI)  │  Auto      │
└────────┬─────────────────────┬──────────────────────┘
         │ CGO                 │ FFI
┌────────▼──────┐   ┌──────────▼──────────┐
│ C Libraries   │   │  Rust Libraries     │
│ libhardware   │   │  libhardware_rs     │
└────────┬──────┘   └──────────┬──────────┘
         └──────────┬───────────┘
                    │ sysfs / ioctl
┌───────────────────▼─────────────────────────────────┐
│              HARDWARE LAYER                         │
│  BME280 (I2C)  │  GPIO  │  UART  │  SPI            │
│       BeagleBone Black ARMv7 1GHz 512MB             │
└─────────────────────────────────────────────────────┘
```

Vollständige Architekturdokumentation: [`arch/architektur.adoc`](arch/architektur.adoc)

---

## 🚀 Schnellstart

```bash
# Repository klonen
git clone https://github.com/user/beaglebone-embedded.git
cd beaglebone-embedded

# Alles bauen (C + Rust + Go)
make all

# Auf BeagleBone deployen
make deploy

# API testen
curl http://192.168.7.2:5000/health
curl http://192.168.7.2:5000/api/v1/bme280
```

---

## 📦 Projektstruktur

```
beaglebone-embedded/
├── .github/                    # GitHub Konfiguration
│   ├── workflows/              # GitHub Actions (CI Mirror)
│   ├── ISSUE_TEMPLATE/         # Issue Templates
│   └── PULL_REQUEST_TEMPLATE/  # PR Template
│
├── c-lib/                      # C Hardware Library
│   ├── include/                # Header: bme280.h gpio.h uart.h spi.h
│   ├── src/                    # Implementierungen
│   └── Makefile
│
├── project/go-api/                     # Go REST API Server
│   ├── cmd/main.go             # Einstiegspunkt (:5000)
│   └── pkg/
│       ├── hal/                # Hardware Abstraction Layer
│       │   ├── interface.go    # HardwareDriver Interface
│       │   ├── factory.go      # C/Rust/Auto Driver Factory
│       │   ├── hal_test.go     # Unit Tests (Mock Driver)
│       │   ├── c/driver.go     # C Driver (CGO)
│       │   ├── rust/driver.go  # Rust Driver (FFI)
│       │   ├── mock/driver.go  # Mock Driver (Tests)
│       │   └── config/         # Konfiguration
│       └── api/                # HTTP Handler
│
├── project/
|   ├── c/                     # C Hardware Library
│   |   ├── include/                # Header: bme280.h gpio.h uart.h spi.h
│   |   ├── src/                    # Implementierungen
│   |   └── Makefile
|   ├── rust-lib/                   # Rust Hardware Library
|   │   ├── src/                    # lib.rs bme280.rs gpio.rs uart.rs spi.rs
|   │   └── Cargo.toml
|   └── go
|
├── tools/
│   ├── cli/                    # bbcli (Cobra CLI)
│   ├── tui/                    # bbtui (BubbleTea TUI)
│   ├── desktop-gui/            # bbgui (Fyne Desktop)
│   └── web-gui/                # Web Dashboard (HTML/JS)
│
├── tests/
│   ├── api/                    # API Integration Tests (pytest)
│   ├── hardware/               # Hardware Tests (pytest)
│   └── cli/                    # CLI Tests (pytest)
│
├── arch/                       # SW Architekturdokumentation
│   ├── architektur.adoc        # AsciiDoc Hauptdokument
│   ├── .buildadoc              # Build-Trigger
│   └── diagrams/               # 12× PlantUML Diagramme
│
├── reports/                    # Report Generator
│   ├── generate_reports.py     # HTML/PDF/MD/JSON Generator
│   └── requirements.json       # Requirements + Tracing
│
├── scripts/
│   ├── install.sh              # Installationsskript
│   └── build_adoc.sh           # AsciiDoc Build Script
│
├── .drone.yml                  # Drone CI (7 Pipelines)
├── .bbcli.yaml                 # CLI Konfiguration
├── Makefile                    # Globales Build System
└── README.md                   # Diese Datei
```

---

## 🔧 Hardware

| Eigenschaft | Wert |
|---|---|
| Board | BeagleBone Black Rev C |
| Prozessor | TI AM335x, ARM Cortex-A8, 1 GHz |
| Architektur | ARMv7-A (32-bit), Hard Float ABI |
| RAM | 512 MB DDR3L |
| Flash | 4 GB eMMC |
| Sensor | BME280 (I2C-1, Adresse 0x76) |
| OS | Debian Linux, Kernel 5.x |

### BME280 Verkabelung

```
BeagleBone Black    →    BME280
P9_19 (I2C2_SCL)   →    SCL
P9_20 (I2C2_SDA)   →    SDA
P9_3  (3.3V)       →    VCC
P9_1  (GND)        →    GND / SDO  (Adresse 0x76)
```

---

## 🛠 Build

### Voraussetzungen

```bash
# Cross-Compiler
sudo apt install gcc-arm-linux-gnueabihf

# Rust Cross-Compilation
cargo install cross cbindgen

# Go 1.22+
# https://go.dev/dl/
```

### Bauen

```bash
make c-lib        # C Library → libhardware.so
make rust-lib     # Rust Library → libhardware_rs.so
make go-api       # Go REST API → bin/embedded-armv7
make cli          # CLI Tools → bin/bbcli-*
make test         # Unit Tests ausführen
```

### Yocto-Image

```bash
make yocto-image                    # bbb-sensor-image (BME280-Layer, Default)
IMAGE=bbb-full-image make yocto-image  # + Go-REST-API/HAL-Libs (bbb-embedded)
```

`scripts/build_yocto.sh` klont Poky/meta-openembedded/meta-arm/meta-ti (idempotent)
und bindet den eigenen Layer `project/yocto/meta-bbb-sensors` ein:

| Recipe | Inhalt |
|---|---|
| `bme280-driver` | BME280-C-Treiber (Shared-Lib + Smoke-Test) |
| `bbb-embedded` | Prebuilt Go-REST-API + HAL-Libraries + systemd-Unit (nur `bbb-full-image`) |
| `linux-yocto_%.bbappend` | Kernel-Konfig (`CONFIG_BMP280`/`_I2C`) |
| `bbb-bme280-overlay` | Devicetree-Overlay I2C1 + BME280@0x76 |
| `bbb-sensor-image` | `core-image-minimal` + BME280-Pakete (Default) |
| `bbb-full-image` | `bbb-sensor-image` + `bbb-embedded` (baut vorab `make all`, falls Artefakte fehlen) |

Env-Vars: `YOCTO_DIR`, `BUILD_DIR`, `DL_DIR`, `SSTATE_DIR`, `MACHINE`, `IMAGE`
(Details siehe `project/yocto/meta-bbb-sensors/README.md`). In Drone-CI läuft der
Build als Pipeline `build-yocto-image` (`cron: nightly` + manueller `custom`-Trigger,
kein Push/PR — ein voller Bitbake-Build dauert Stunden).

---

## 🌐 REST API

| Endpoint | Methode | Beschreibung |
|---|---|---|
| `/health` | GET | Status, Backend, Driver |
| `/api/v1/bme280` | GET | Temperatur, Luftfeuchtigkeit, Druck, Höhe |
| `/api/v1/bme280/stream` | GET (SSE) | Echtzeit-Stream |
| `/api/v1/gpio/{pin}` | GET/POST | GPIO lesen/setzen |
| `/api/v1/uart/send` | POST | UART senden |
| `/api/v1/uart/receive` | GET | UART empfangen |
| `/api/v1/spi/transfer` | POST | SPI Transfer |
| `/api/v1/backend` | POST | Backend wechseln (c/rust/auto) |

```bash
# Beispiele
curl http://192.168.7.2:5000/api/v1/bme280
curl -X POST http://192.168.7.2:5000/api/v1/gpio/60 \
     -d '{"value":1}' -H "Content-Type: application/json"
curl -X POST http://192.168.7.2:5000/api/v1/backend \
     -d '{"backend":"rust"}' -H "Content-Type: application/json"
```

---

## 🔌 HAL Backend

Das System unterstützt vier Backends:

| Backend | Beschreibung |
|---|---|
| `c` | C Library via CGO — maximale Performance |
| `rust` | Rust Library via FFI — Memory Safety |
| `auto` | Automatischer Fallback: C primär → Rust bei Fehler |
| `pru` | PRU1 via RPMsg — deterministisches GPIO (R30/R31-Bit 0-15), kein Sensor/UART/SPI (siehe Issue #252) |

```bash
# Backend wechseln
./bin/embedded-armv7 --backend=rust
HW_BACKEND=auto ./bin/embedded-armv7

# Zur Laufzeit
bbcli backend set rust
curl -X POST http://192.168.7.2:5000/api/v1/backend \
     -d '{"backend":"auto"}'
```

---

## 🚗 IEEE 1722 / ACF-CAN

Zusätzlich zur HAL gibt es ein eigenständiges Linux-Kernel-Modul (`acfcan`,
[Open1722](https://github.com/COVESA/Open1722), Issue #256): tunnelt
SocketCAN-Frames transparent als IEEE-1722-ACF_CAN-Nachrichten über Ethernet.
Kein HAL-Backend — `cansend`/`candump` funktionieren gegen ein
`acfcan`-Interface wie gegen einen echten CAN-Bus, angesprochen wird es über
`ip link ... type acfcan` + sysfs, nicht über `:5000/api/v1/*`.

```bash
make acfcan-mod   # KERNEL_SRC muss auf einen Yocto-Kernel-Quellbaum zeigen
```

---

## 🖥 Client Tools

### CLI (bbcli)

```bash
# Installation
curl -fsSL https://github.com/user/beaglebone/releases/latest/install.sh | bash

# Verwendung
bbcli --host 192.168.7.2 bme280 read
bbcli gpio write 60 1
bbcli backend set rust
bbcli system status

# Shell Completion
bbcli completion bash >> ~/.bashrc
bbcli completion zsh  >> ~/.zshrc
```

### Terminal TUI (bbtui)

```bash
bbtui --host 192.168.7.2
# Tab:Wechseln  r:Refresh  c:C-Backend  R:Rust  a:Auto  q:Beenden
```

### Desktop GUI (bbgui)

```bash
bbgui  # Fyne Desktop GUI für Linux
```

### Web GUI

```bash
# Öffne tools/web-gui/index.html im Browser
# oder: python3 -m http.server 8090 --directory tools/web-gui/
```

---

## 🧪 Tests

```bash
# Go Unit Tests (Mock — kein Hardware nötig)
cd go-api && go test ./pkg/hal/... -v

# Mit Race Condition Check
go test ./pkg/hal/... -race -count=3

# API Integration Tests
pytest tests/api/ -v

# Hardware Tests (BeagleBone nötig)
BEAGLE_HOST=192.168.7.2 pytest tests/hardware/ -v

# Alle Backends testen
for b in c rust auto; do
  HW_BACKEND=$b pytest tests/hardware/ -v
done
```

---

## 📊 CI/CD

7 Drone CI Pipelines + Nightly:

| Pipeline | Trigger | Beschreibung |
|---|---|---|
| `1-libraries` | push/PR/tag | C + Rust bauen & testen |
| `2-embedded-sw` | push/PR/tag | HAL Tests, Go API, QEMU ARMv7, HW Deploy |
| `3-tools` | push/PR/tag | CLI/TUI/GUI für 4 Plattformen |
| `4-webapp` | push/PR/tag | Web Frontend |
| `5-release` | tag only | Docker, Gitea Release |
| `6-nightly` | cron 02:00 | HW Tests C+Rust+Auto |
| `7-reports` | push/PR/tag | Test Reports, Architektur, Docs |

### Quality Gates

| Gate | Schwellenwert |
|---|---|
| Test Erfolgsrate | ≥ 90% |
| Ø Code Coverage | ≥ 75% |
| Min Code Coverage | ≥ 50% |
| Requirements impl. | ≥ 80% |

---

## 📚 Dokumentation

| Dokument | Beschreibung |
|---|---|
| [`arch/architektur.adoc`](arch/architektur.adoc) | SW Architektur (AsciiDoc) |
| [`arch/diagrams/`](arch/diagrams/) | 12× PlantUML Diagramme |
| [`reports/`](reports/) | Test & Requirements Reports |
| [Wiki](../../wiki) | Auto-generierte Reports (CI) |

---

## 🤝 Contributing

1. Fork erstellen
2. Feature Branch: `git checkout -b feature/mein-feature`
3. Änderungen committen: `git commit -m 'feat: Mein Feature'`
4. Push: `git push origin feature/mein-feature`
5. Pull Request öffnen

Bitte [CONTRIBUTING.md](CONTRIBUTING.md) lesen.

---

## 📄 Lizenz

MIT License — siehe [LICENSE](LICENSE)

---

## 🏷 Technologie Stack

![Go](https://img.shields.io/badge/Go-00ADD8?logo=go&logoColor=white)
![Rust](https://img.shields.io/badge/Rust-000000?logo=rust&logoColor=white)
![C](https://img.shields.io/badge/C-A8B9CC?logo=c&logoColor=black)
![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![Drone CI](https://img.shields.io/badge/Drone_CI-212121?logo=drone&logoColor=white)
![Podman](https://img.shields.io/badge/Podman-892CA0?logo=podman&logoColor=white)
