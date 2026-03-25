# Contributing Guide

Danke für dein Interesse am BeagleBone Black Embedded SW Projekt!

## 🚀 Entwicklungsumgebung

```bash
git clone https://github.com/user/beaglebone-embedded.git
cd beaglebone-embedded

# Voraussetzungen
sudo apt install gcc-arm-linux-gnueabihf make
cargo install cross cbindgen
go install golang.org/x/tools/cmd/goimports@latest

# Unit Tests (kein Hardware nötig)
cd go-api && go test ./pkg/hal/... -v
```

## 📐 Commit Konventionen

Format: `type(scope): Beschreibung`

| Type | Beschreibung |
|---|---|
| `feat` | Neue Funktion |
| `fix` | Bugfix |
| `docs` | Dokumentation |
| `test` | Tests hinzugefügt |
| `refactor` | Code Refactoring |
| `ci` | CI/CD Änderungen |

Beispiele:
```
feat(hal): Rust SPI Transfer implementiert
fix(bme280): Kalibrierung für Luftdruck korrigiert
docs(arch): PlantUML Sequenzdiagramm ergänzt
test(gpio): Tabellen-Tests für Mock Driver
```

## 🔀 Pull Request Prozess

1. Tests müssen bestehen: `go test ./...`
2. Code formatiert: `gofmt -w .`
3. Coverage ≥ 75%
4. Beschreibung ausfüllen (PR Template)

## 📋 Requirements Management

Anforderungen werden mit [StrictDoc](https://strictdoc.readthedocs.io/) verwaltet und liegen unter `docs/requirements/`.

### Struktur

| Datei | UID-Präfix | Inhalt |
|-------|-----------|--------|
| `docs/requirements/system_requirements.sdoc` | `SYS-` | Systemanforderungen (Plattform, Schnittstellen) |
| `docs/requirements/software_requirements.sdoc` | `SWR-` | Softwareanforderungen (HAL, Architektur) |
| `docs/requirements/hardware_driver_requirements.sdoc` | `HW-DRV-` | Treiber-Anforderungen (BME280, GPIO, UART, SPI) |

### Neue Anforderung hinzufügen

```sdoc
[REQUIREMENT]
UID: SWR-006
TITLE: Kurzer Titel
STATEMENT: Die vollständige Anforderungsbeschreibung.
RELATIONS:
- TYPE: File
  VALUE: project/go-api/pkg/hal/interface.go
```

**UID-Konvention:** Nächste freie Nummer je Präfix verwenden (`SYS-`, `SWR-`, `HW-DRV-`).

### Traceability zu Code und Tests

Quelldateien, die eine Anforderung implementieren oder testen, erhalten einen Marker-Kommentar:

```go
// [SDOC_LINK: SWR-006]
func MyFunction() { ... }
```

Sowohl die `.sdoc`-Datei (via `RELATIONS`) als auch die Quelldatei (via `[SDOC_LINK]`) müssen aktualisiert werden.

### Lokal exportieren und validieren

```bash
# Abhängigkeiten installieren (inkl. PDF-Support via WeasyPrint)
pip install "strictdoc[pdf]"

# HTML-Dokumentation generieren (validiert automatisch beim Export)
strictdoc export . --formats html --output-dir output/strictdoc
# PDF-Dokumentation generieren
strictdoc export . --formats html2pdf --output-dir output/strictdoc```

> Für PDF (`html2pdf`) wird Chromium benötigt: `sudo apt install chromium-driver` (nur falls `chromedriver` nicht verfügbar ist)

### CI/CD

- **GitHub Actions:** Job `StrictDoc Export & Validation` läuft bei jedem Push
- **Drone CI:** Step `strictdoc-export` in Pipeline 7 parallel zu `build-docs`
- Bei kaputten Referenzen (`strictdoc check`) schlägt der Build fehl

## 🏗 Architektur-Regeln

- Hardware-Zugriff **nur** in C oder Rust — **nicht** in Go
- Go ist **nur** für API, HAL Interface und Tools
- Neuer Hardware-Support → beide Libraries (C + Rust) implementieren
- Jede neue Funktion im HAL Interface → Mock Driver aktualisieren
