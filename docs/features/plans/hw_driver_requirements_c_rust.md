# Implementationsplan: C & Rust Hardware-Treiber Anforderungen

**Issue:** feat: Add detailed C & Rust implementation requirements to StrictDoc
**Datum:** 2026-03-18
**Status:** Offen

---

## Motivation

Die bestehende `docs/requirements/hardware_driver_requirements.sdoc` enthält nur high-level Anforderungen (HW-DRV-001 bis HW-DRV-004). Basierend auf den C-Header-Dateien (`c-lib/include/`) und den Rust-Sourcen (`project/rust-lib/src/`) fehlen konkrete Implementierungsanforderungen für beide Backends sowie die Anforderung, dass C und Rust funktional äquivalent sein müssen.

---

## Fehlende Anforderungen

### BME280

| UID | Titel | Quelle |
|-----|-------|--------|
| `HW-DRV-005` | BME280 I2C-Bus und Adresse | `c-lib/include/bme280.h` — `BME280_I2C_BUS=/dev/i2c-1`, `BME280_ADDR=0x76` |
| `HW-DRV-006` | BME280 Höhenberechnung | `bme280_data_t.altitude` via `SEA_LEVEL_PA=101325.0` |
| `HW-DRV-007` | BME280 Kalibrierungsdaten | `bme280_calib_t` muss beim Init ausgelesen werden |

### GPIO

| UID | Titel | Quelle |
|-----|-------|--------|
| `HW-DRV-008` | GPIO Export / Unexport | `gpio_export()` / `gpio_unexport()` in `c-lib/include/gpio.h` |

### UART

| UID | Titel | Quelle |
|-----|-------|--------|
| `HW-DRV-009` | UART Flush | `uart_flush()` in `c-lib/include/uart.h` |
| `HW-DRV-010` | UART Read Timeout | `timeout_ms` Parameter in `uart_read()` |

### SPI

| UID | Titel | Quelle |
|-----|-------|--------|
| `HW-DRV-011` | SPI Mode und Bits-per-Word | `spi_dev_t.mode`, `spi_dev_t.bits` in `c-lib/include/spi.h` |

### C & Rust Parität

| UID | Titel | Quelle |
|-----|-------|--------|
| `HW-DRV-012` | C/Rust Funktionale Äquivalenz | Beide Backends müssen identische Funktionssignaturen über FFI exportieren |

---

## Umsetzung

### Schritt 1 — `hardware_driver_requirements.sdoc` erweitern

Datei: `docs/requirements/hardware_driver_requirements.sdoc`

Neue Anforderungen mit `RELATIONS` zu den jeweiligen Quelldateien hinzufügen:

```sdoc
[REQUIREMENT]
UID: HW-DRV-005
TITLE: BME280 I2C-Bus und Adresse
STATEMENT: Der BME280-Treiber muss über den I2C-Bus /dev/i2c-1 mit der Geräteadresse 0x76 kommunizieren.
RELATIONS:
- TYPE: File
  VALUE: c-lib/include/bme280.h
- TYPE: File
  VALUE: project/rust-lib/src/bme280.rs

[REQUIREMENT]
UID: HW-DRV-006
TITLE: BME280 Höhenberechnung
STATEMENT: Der BME280-Treiber muss aus dem gemessenen Luftdruck und dem Meeresspiegel-Referenzdruck (101325 Pa) die Höhe in Metern berechnen.
RELATIONS:
- TYPE: File
  VALUE: c-lib/include/bme280.h
- TYPE: File
  VALUE: project/rust-lib/src/bme280.rs

[REQUIREMENT]
UID: HW-DRV-007
TITLE: BME280 Kalibrierungsdaten
STATEMENT: Der BME280-Treiber muss beim Initialisieren die Kalibrierungsregister des Sensors auslesen und für alle nachfolgenden Messungen verwenden.
RELATIONS:
- TYPE: File
  VALUE: c-lib/include/bme280.h
- TYPE: File
  VALUE: project/rust-lib/src/bme280.rs

[REQUIREMENT]
UID: HW-DRV-008
TITLE: GPIO Export und Unexport
STATEMENT: Der GPIO-Treiber muss Pins über das sysfs-Interface exportieren (gpio_export) und nach Verwendung wieder freigeben (gpio_unexport).
RELATIONS:
- TYPE: File
  VALUE: c-lib/include/gpio.h
- TYPE: File
  VALUE: project/rust-lib/src/gpio.rs

[REQUIREMENT]
UID: HW-DRV-009
TITLE: UART Flush
STATEMENT: Der UART-Treiber muss den Sende- und Empfangspuffer auf Anforderung leeren können (uart_flush).
RELATIONS:
- TYPE: File
  VALUE: c-lib/include/uart.h
- TYPE: File
  VALUE: project/rust-lib/src/uart.rs

[REQUIREMENT]
UID: HW-DRV-010
TITLE: UART Read Timeout
STATEMENT: Der UART-Treiber muss beim Lesen einen Timeout in Millisekunden unterstützen. Bei Ablauf des Timeouts ohne Daten muss ein Fehlercode zurückgegeben werden.
RELATIONS:
- TYPE: File
  VALUE: c-lib/include/uart.h
- TYPE: File
  VALUE: project/rust-lib/src/uart.rs

[REQUIREMENT]
UID: HW-DRV-011
TITLE: SPI Mode und Bits-per-Word
STATEMENT: Der SPI-Treiber muss bei der Initialisierung den SPI-Mode (0–3) und die Bits-per-Word konfigurieren können.
RELATIONS:
- TYPE: File
  VALUE: c-lib/include/spi.h
- TYPE: File
  VALUE: project/rust-lib/src/spi.rs

[REQUIREMENT]
UID: HW-DRV-012
TITLE: C und Rust funktionale Äquivalenz
STATEMENT: Das C-Backend und das Rust-Backend müssen für alle Hardware-Operationen (BME280, GPIO, UART, SPI) funktional äquivalente Ergebnisse liefern. Beide Backends müssen dieselben FFI-Funktionssignaturen exportieren.
RELATIONS:
- TYPE: File
  VALUE: project/go-api/pkg/hal/c/driver.go
- TYPE: File
  VALUE: project/go-api/pkg/hal/rust/driver.go
```

### Schritt 2 — Traceability zu Tests erweitern

Für HW-DRV-005 bis HW-DRV-012 jeweils `RELATIONS` zu relevanten Tests ergänzen sobald entsprechende Testfälle in `project/go-api/pkg/hal/hal_test.go` oder `tests/hardware/test_hardware.py` existieren.

---

## Betroffene Dateien

| Aktion  | Datei |
|---------|-------|
| Ändern  | `docs/requirements/hardware_driver_requirements.sdoc` |

---

## Acceptance Criteria

- [ ] HW-DRV-005 bis HW-DRV-012 in `hardware_driver_requirements.sdoc` eingetragen
- [ ] Alle neuen Anforderungen haben `RELATIONS` zu C-Header und Rust-Source
- [ ] `strictdoc export docs/requirements/` läuft fehlerfrei durch
- [ ] C/Rust Äquivalenz-Anforderung (HW-DRV-012) ist mit beiden Driver-Dateien verknüpft

---

## Referenzen

- `c-lib/include/bme280.h`
- `c-lib/include/gpio.h`
- `c-lib/include/uart.h`
- `c-lib/include/spi.h`
- `project/rust-lib/src/bme280.rs`
- `project/rust-lib/src/gpio.rs`
- `project/rust-lib/src/uart.rs`
- `project/rust-lib/src/spi.rs`
- [Issue #28 — StrictDoc Integration](https://github.com/paulefl/beaglebone_black/issues/28)
