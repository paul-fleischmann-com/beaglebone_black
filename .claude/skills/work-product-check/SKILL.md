---
description: Prüft ob alle ASPICE Work Products für die aktuelle Waterfall-Phase vorhanden und vollständig sind. Gibt eine Checkliste mit Status und fehlenden Artefakten aus.
---

# /work-product-check

Aktueller Workflow-State: !`cat .claude/workflow-state.json 2>/dev/null`

## Work Products je Phase

Bestimme die aktuelle Phase aus dem State und prüfe die zugehörigen Work Products:

### Requirements
| Work Product | Pfad | Prüfung |
|---|---|---|
| System Requirements Spec | `docs/requirements/system_requirements.sdoc` | Existiert, ≥1 aktives Req |
| SW Requirements Spec | `docs/requirements/software_requirements.sdoc` | Existiert, alle mit REQUIREMENT_TYPE |
| HW Requirements Spec | `docs/requirements/hardware_driver_requirements.sdoc` | Existiert |
| Traceability Matrix | `docs/requirements/traceability_matrix.md` | Existiert, aktuell |
| Review-Protokoll | `docs/requirements/review_*.md` | Mind. ein Review vorhanden |

### Design
| Work Product | Pfad | Prüfung |
|---|---|---|
| HAL Interface | `project/go-api/pkg/hal/interface.go` | Existiert |
| C Headers | `project/c/include/*.h` | Mindestens 4 Header |
| Rust FFI | `project/rust-lib/src/lib.rs` | Existiert |
| API Routen | `project/go-api/cmd/main.go` | Existiert |

### Implementation
| Work Product | Pfad | Prüfung |
|---|---|---|
| Unit Tests | `project/go-api/pkg/hal/hal_test.go` | Existiert, ≥4 Test-Funktionen |
| Coverage Report | `reports/coverage/` | Vorhanden (nach CI-Run) |
| SDOC_LINK Coverage | Code | Alle SWR-* gelinkt |
| CI-Pipeline | `.drone.yml` | Existiert, traceability-check-Step vorhanden |

### Integration
| Work Product | Pfad | Prüfung |
|---|---|---|
| Integrationstests | `tests/api/` | Existiert |
| Test-Report | `reports/` | CI-Reports vorhanden |

### Verification
| Work Product | Pfad | Prüfung |
|---|---|---|
| Hardware-Tests | `tests/hardware/` | Existiert |
| Test-Protokoll | `reports/hardware/` | Vorhanden |

### Validation
| Work Product | Pfad | Prüfung |
|---|---|---|
| SonarQube Report | SonarCloud | Quality Gate grün |
| CHANGELOG | `CHANGELOG.md` | Existiert |
| Vollständige Traceability | Traceability-Matrix | Alle User Stories gelinkt |

## Prüfung ausführen

Für jedes Work Product der aktuellen Phase:

```bash
# Existenz prüfen
ls -la <pfad> 2>/dev/null && echo "✅" || echo "❌"

# Qualität prüfen (spezifisch je Work Product)
```

Konkrete Bash-Checks:
```bash
# Requirements-Phase
[ -f docs/requirements/system_requirements.sdoc ] && echo "SRS: ✅" || echo "SRS: ❌"
[ -f docs/requirements/software_requirements.sdoc ] && echo "SWS: ✅" || echo "SWS: ❌"
grep -c "REQUIREMENT_TYPE:" docs/requirements/software_requirements.sdoc 2>/dev/null
ls docs/requirements/review_*.md 2>/dev/null && echo "Review: ✅" || echo "Review: ❌"

# Implementation-Phase
grep -c "^func Test" project/go-api/pkg/hal/hal_test.go 2>/dev/null
python3 scripts/gen_traceability_matrix.py --check 2>&1 | tail -3
grep "traceability-check" .drone.yml 2>/dev/null && echo "CI-Step: ✅" || echo "CI-Step: ❌"
```

## Ausgabe-Format

```
# Work Product Check: <Phase>
Stand: <heute>

## Pflicht-Work-Products

| # | Work Product | Status | Befund |
|---|---|---|---|
| 1 | System Requirements Spec | ✅ | 5 aktive Requirements |
| 2 | Traceability Matrix | ✅ | Aktuell (2026-04-12) |
| 3 | Review-Protokoll | ✅ | review_swr_2026-04-12.md |
...

## Fehlende Work Products

- ❌ <Name>: <Was fehlt und wie erstellen>

## Empfehlung

Alle Work Products vorhanden: Phase-Gate kann geprüft werden → `/phase-gate`
Fehlende Work Products: <Konkrete Schritte>
```

## Nach dem Check

Falls Work Products fehlen: Schlage konkrete Befehle vor um sie zu erstellen.
Falls alle vorhanden: Empfehle `@phase-gate-reviewer` für das formale Gate-Review.
