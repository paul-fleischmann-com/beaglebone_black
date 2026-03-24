# Implementationsplan: StrictDoc Requirements Management

**Issue:** [#28 — feat: Integrate StrictDoc as Requirements Management Tool](https://github.com/paulefl/beaglebone_black/issues/28)
**Datum:** 2026-03-18
**Status:** Offen

---

## Kontext & Ausgangslage

- `docs/` existiert bereits mit `API.md` und `SETUP.md`
- `CONTRIBUTING.md` existiert und muss erweitert werden
- `.drone.yml` Pipeline 7 ("Reports & Documentation") ist der natürliche Einhängepunkt für StrictDoc
- Quality-Gate in CI prüft bereits `Requirements implementation: ≥80%`
- `tests/requirements-dev.txt` enthält bereits Python-Testabhängigkeiten

---

## Phase 1 — Installation & Konfiguration

### 1.1 `strictdoc` zur Abhängigkeitsliste hinzufügen

- **Datei:** `tests/requirements-dev.txt`
- **Eintrag:** `strictdoc>=0.0.50`

### 1.2 `strictdoc.toml` im Repo-Root anlegen

```toml
[project]
title = "BeagleBone Black Embedded SW"
html_export_output_dir = "output/docs"

[features]
requirement_uid_alphabet = "SYS SWR HW-DRV"
```

---

## Phase 2 — Dokumentstruktur (`.sdoc`-Dateien)

Neues Verzeichnis: `docs/requirements/`

### 2.1 `system_requirements.sdoc` — Systemanforderungen (SYS-001 …)

- Zielplattform, Echtzeitanforderungen, Hardware-Schnittstellen
- Beispiel-UIDs:
  - `SYS-001` — ARM Cortex-A8 Zielplattform
  - `SYS-002` — REST API auf Port 5000

### 2.2 `software_requirements.sdoc` — Softwareanforderungen (SWR-001 …)

- HAL-Interface, Backend-Auswahl (`HW_BACKEND`), Treiber-Coverage
- Mindestens 3 Anforderungen mit eindeutigen UIDs

### 2.3 `hardware_driver_requirements.sdoc` — Treiberanforderungen (HW-DRV-001 …)

- BME280, GPIO, UART, SPI — jeweils eine Anforderung mit Traceability zu Tests

### UID-Konvention

| Präfix    | Scope                    |
|-----------|--------------------------|
| `SYS-`    | Systemanforderungen      |
| `SWR-`    | Softwareanforderungen    |
| `HW-DRV-` | Treiber-/Hardwareanforderungen |

---

## Phase 3 — Traceability zu Code & Tests

### 3.1 `RELATIONS` in `.sdoc`-Dateien

Anforderungen werden mit folgenden Dateien verknüpft:

| Anforderungstyp | Verknüpfte Dateien |
|-----------------|-------------------|
| Systemanforderungen | `go-api/cmd/main.go`, `go-api/pkg/hal/interface.go` |
| Softwareanforderungen | `go-api/pkg/hal/factory.go`, `go-api/pkg/hal/mock/driver.go` |
| Treiberanforderungen | `c-lib/include/`, `project/rust-lib/src/lib.rs`, `go-api/pkg/hal/hal_test.go` |

### 3.2 Beispiel-Relation (SWR-003 → HAL-Test)

```sdoc
[REQUIREMENT]
UID: SWR-003
TITLE: HAL Mock Driver must implement HardwareDriver interface
RELATIONS:
- TYPE: File
  VALUE: go-api/pkg/hal/hal_test.go
```

### 3.3 Vollständige Traceability-Kette (Mindestanforderung)

`SWR-003` → `go-api/pkg/hal/interface.go` → `go-api/pkg/hal/hal_test.go` (TestInterfaceCompliance)

---

## Phase 4 — CI/CD Integration (`.drone.yml`)

**Einhängepunkt:** Pipeline 7 — "Reports & Documentation"

Neuer Step `strictdoc-export`:

```yaml
- name: strictdoc-export
  image: python:3.11-slim
  commands:
    - pip install strictdoc --quiet
    - strictdoc export docs/requirements/ --output-dir output/strictdoc
    - strictdoc check docs/requirements/
  volumes:
    - name: artifacts
      path: /drone/src/output
```

> `strictdoc check` bricht den Build bei kaputten Referenzen ab (Lint/Validierung).

HTML-Output wird als CI-Artefakt hochgeladen — analog zu bestehenden Report-Artefakten in Pipeline 7.

---

## Phase 5 — CONTRIBUTING.md erweitern

Neuer Abschnitt: **Requirements Management**

Inhalte:
- Wie neue Anforderungen hinzugefügt werden
- UID-Konvention (Tabelle aus Phase 2)
- Wie `RELATIONS` zu Code und Tests gesetzt werden
- Lokaler Befehl zum Exportieren: `strictdoc export docs/requirements/`

---

## Betroffene Dateien

| Aktion   | Datei                                               |
|----------|-----------------------------------------------------|
| Neu      | `strictdoc.toml`                                    |
| Neu      | `docs/requirements/system_requirements.sdoc`        |
| Neu      | `docs/requirements/software_requirements.sdoc`      |
| Neu      | `docs/requirements/hardware_driver_requirements.sdoc` |
| Ändern   | `tests/requirements-dev.txt`                        |
| Ändern   | `.drone.yml` (+ Step in Pipeline 7)                 |
| Ändern   | `CONTRIBUTING.md` (+ Requirements-Abschnitt)        |

---

## Acceptance Criteria

| Kriterium | Phase |
|-----------|-------|
| `strictdoc export docs/` läuft erfolgreich lokal | 1 + 2 |
| Mindestens 5 Anforderungen mit eindeutigen UIDs definiert | 2 |
| CI-Pipeline publiziert generierte HTML-Dokumentation | 4 |
| Traceability von mindestens einer Anforderung zu einem Test hergestellt | 3 |
| `CONTRIBUTING.md` dokumentiert den Prozess zur Pflege von Anforderungen | 5 |

---

## Referenzen

- [StrictDoc Dokumentation](https://strictdoc.readthedocs.io/)
- [StrictDoc GitHub](https://github.com/strictdoc-project/strictdoc)
- [Issue #28](https://github.com/paulefl/beaglebone_black/issues/28)
