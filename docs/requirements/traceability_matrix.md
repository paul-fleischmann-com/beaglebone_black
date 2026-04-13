# Traceability-Matrix — BeagleBone Black

**Generiert:** 2026-04-13  
**Tool:** `scripts/gen_traceability_matrix.py`  
**ASPICE:** SWE.1 BP3/BP4/BP5 Work Product

---

## Legende

| Symbol | Bedeutung |
|--------|-----------|
| ✅ | Traceability vollständig |
| ⚠️ | Teilweise (kein SDOC_LINK im Code) |
| ❌ | Keine Abdeckung |

---

## SYS → SWR → HW-DRV → Code

### ✅ `SYS-001` — ARM Cortex-A8 Zielplattform

| SWR | Titel | HW-DRV | Code-Link |
|-----|-------|--------|-----------|
| ✅ `SWR-009` | ARM v7 Architektur-Kompatibilität | — | `Makefile` |

### ✅ `SYS-002` — Betriebssystem

| SWR | Titel | HW-DRV | Code-Link |
|-----|-------|--------|-----------|
| ✅ `SWR-010` | Linux-Betriebssystem-Kompatibilität | — | `project/go-api/cmd/main.go` |

### ✅ `SYS-003` — REST API Erreichbarkeit

| SWR | Titel | HW-DRV | Code-Link |
|-----|-------|--------|-----------|
| ✅ `SWR-011` | HTTP-Server Port-Bindung | — | `project/go-api/cmd/main.go` |

### ✅ `SYS-004` — Hardware-Schnittstellen

| SWR | Titel | HW-DRV | Code-Link |
|-----|-------|--------|-----------|
| ✅ `SWR-001` | HAL Interface Definition | `HW-DRV-001` `HW-DRV-002` `HW-DRV-003` `HW-DRV-004` | `project/go-api/pkg/hal/interface.go` |
| ✅ `SWR-002` | Backend-Auswahl per Umgebungsvariable | — | `project/go-api/pkg/hal/loader/factory.go` |
| ✅ `SWR-004` | Hardware-Zugriff nur in C und Rust | — | `project/go-api/pkg/hal/interface.go` |
| ✅ `SWR-006` | HTTP-Server Timeouts | — | `project/go-api/pkg/api/server_test.go` |

### ✅ `SYS-005` — Cross-Compilation

| SWR | Titel | HW-DRV | Code-Link |
|-----|-------|--------|-----------|
| ✅ `SWR-012` | Cross-Compilation Toolchain | — | `Makefile` |

---

## SWR ohne SYS-Parent

| SWR | Titel | Code-Link |
|-----|-------|-----------|
| `SWR-003` | Mock Driver für Tests | `project/go-api/pkg/hal/hal_test.go` `project/go-api/pkg/hal/mock/driver.go` |
| `SWR-005` | Auto-Fallback Mechanismus | `project/go-api/pkg/hal/hal_test.go` `project/go-api/pkg/hal/loader/factory.go` |
| `SWR-007` | BME280 Stream Flusher-Prüfung | `project/go-api/pkg/api/handlers.go` |
| `SWR-008` | Keine flag.Parse() in Library-Packages | `project/go-api/pkg/hal/config/config_test.go` |

---

## Zusammenfassung

| Metrik | Wert |
|--------|------|
| SYS-Anforderungen | 5 |
| SWR-Anforderungen | 12 |
| SWR mit SDOC_LINK im Code | 12 / 12 |
| SWR ohne Code-Link | 0 |
| HW-DRV-Anforderungen | 4 |
| SYS vollständig abgedeckt | 5 / 5 |
