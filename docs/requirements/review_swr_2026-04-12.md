# Software Requirements Review — SWR Walkthrough

**Datum:** 2026-04-12
**Dokument:** `docs/requirements/software_requirements.sdoc`
**Reviewer:** paulefl
**Methode:** Walkthrough (informelles Review nach ASPICE SUP.1)
**Status:** Abgeschlossen

---

## Geprüfte Anforderungen

| UID | Titel | Ergebnis | Anmerkung |
|-----|-------|----------|-----------|
| SWR-001 | HAL Interface Definition | OK | Vollständig, Parent SYS-004 korrekt |
| SWR-002 | Backend-Auswahl per Umgebungsvariable | OK | HW_BACKEND env var korrekt beschrieben |
| SWR-003 | Mock Driver für Tests | OK | Parent SWR-001 korrekt |
| SWR-004 | Hardware-Zugriff nur in C und Rust | OK | Architektur-Constraint korrekt |
| SWR-005 | Auto-Fallback Mechanismus | OK | C→Rust Fallback korrekt spezifiziert |
| SWR-006 | HTTP-Server Timeouts | OK | Konkrete Mindestwerte angegeben |
| SWR-007 | BME280 Stream Flusher-Prüfung | OK | HTTP 500 bei fehlendem Flusher |
| SWR-008 | Keine flag.Parse() in Library-Packages | OK | DI-Prinzip korrekt beschrieben |
| SWR-009 | ARM v7 Architektur-Kompatibilität | OK | Neu — alle drei Toolchains abgedeckt |
| SWR-010 | Linux-Betriebssystem-Kompatibilität | OK | Neu — POSIX-Anforderung korrekt |
| SWR-011 | HTTP-Server Port-Bindung | OK | Neu — Port 5000, konfigurierbar |
| SWR-012 | Cross-Compilation Toolchain | OK | Neu — alle drei Sprachen abgedeckt |

---

## Traceability-Prüfung

| SYS-Req | Abgedeckt durch SWR | Status |
|---------|---------------------|--------|
| SYS-001 | SWR-009 | ✅ |
| SYS-002 | SWR-010 | ✅ |
| SYS-003 | SWR-011 | ✅ |
| SYS-004 | SWR-001, SWR-002, SWR-004, SWR-006 | ✅ |
| SYS-005 | SWR-012 | ✅ |

---

## Feststellungen

- **F-001 (Minor):** Anforderungsklassifikation (funktional/nicht-funktional) fehlt als explizites SDoc-Feld. Akzeptiert für Level 2 — Prioritätsfeld wird als Proxy verwendet.
- **F-002 (Minor):** HW-DRV-001..004 referenzierten bisher SYS-004 direkt statt SWR-001. Wurde im Zuge dieses Reviews korrigiert.

---

## Entscheidung

Alle SWR-Anforderungen sind vollständig, eindeutig und zur Implementierung freigegeben.

**Reviewer-Signatur:** paulefl, 2026-04-12
