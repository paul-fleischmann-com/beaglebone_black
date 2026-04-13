# Definition of Done — BeagleBone Black Projekt

Stand: 2026-04-13 | ASPICE Target: Level 2

Ein Issue gilt als **Done** wenn alle zutreffenden Kriterien erfüllt sind.

## Code-Qualität

- [ ] Code formatiert (`gofmt -w` für Go, `shellcheck` für Shell-Skripte)
- [ ] Alle Unit Tests grün (`cd project/go-api && go test ./...`)
- [ ] Test-Coverage ≥ 75% gesamt, ≥ 50% je Datei
- [ ] Kein neuer SonarQube BLOCKER oder CRITICAL

## ASPICE-Traceability (SWE.1/SWE.4)

- [ ] `SDOC_LINK`-Kommentare für neue/geänderte Funktionalität im Code
- [ ] Requirements in SDoc aktualisiert falls neue Funktionalität
- [ ] Traceability-Matrix aktuell (`make traceability` grün)

## Prozess (SUP.8/SUP.10)

- [ ] Branch von `main` erstellt (`<issue>-<titel>`)
- [ ] PR erstellt mit Issue-Referenz (`Closes #<nr>`)
- [ ] PR reviewed (Code-Review via `@pr-reviewer` oder manuell)
- [ ] CI-Pipeline grün (alle relevanten Drone-Pipelines)
- [ ] PR gemergt und Branch gelöscht
- [ ] Issue geschlossen

## Dokumentation (SWE.3)

- [ ] CHANGELOG.md aktualisiert bei user-facing Änderungen
- [ ] API-Dokumentation aktualisiert bei Schnittstellen-Änderungen

## Hardware-spezifisch (bei HAL-Änderungen, SWE.2/SWE.4)

- [ ] Mock-Driver (`project/go-api/pkg/hal/mock/driver.go`) aktualisiert
- [ ] C-Driver (`project/go-api/pkg/hal/c/driver.go`) aktualisiert
- [ ] Rust-Driver (`project/go-api/pkg/hal/rust/driver.go`) aktualisiert
- [ ] HAL-Interface (`project/go-api/pkg/hal/interface.go`) konsistent
- [ ] C-Header (`project/c/include/`) aktualisiert
- [ ] Rust-FFI (`project/rust-lib/src/lib.rs`) aktualisiert

## ASPICE Work Products (bei phasenrelevanten Issues)

- [ ] Work Product in `workflow-state.json` `open_work_products` entfernt
- [ ] Work Product-Dokument erstellt/aktualisiert

---

*Prüfbar über: `/work-product-check` | `@sprint-manager dod <issue-nr>`*
