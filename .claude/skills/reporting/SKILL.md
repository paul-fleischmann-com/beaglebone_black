---
description: Generiert alle Projekt-Reports — Traceability-Matrix, ASPICE Capability Level Report und Sprint-Velocity-Report. Aufrufen mit /reporting (alle Reports) oder /reporting aspice|traceability|velocity.
---

# /reporting

Aktueller Stand: !`python3 -c "import json; d=json.load(open('.claude/workflow-state.json')); print(f'Phase: {d[\"current_phase\"]} | Sprint: {d[\"current_sprint\"]} | ASPICE Target: Level {d[\"aspice_target_level\"]}')" 2>/dev/null`

Angefragter Report: $ARGUMENTS

## Reports

| Report | Befehl | Ausgabe |
|---|---|---|
| Traceability-Matrix | `make traceability` | `docs/requirements/traceability_matrix.md` |
| ASPICE Capability Level | `make aspice-report` | `docs/reports/aspice_report.md` |
| Sprint Velocity | `make velocity-report` | `docs/reports/velocity_report.md` |
| Alle zusammen | `make reports` | alle obigen |

## Vorgehen

Falls $ARGUMENTS leer ist oder "all": Führe `make reports` aus und zeige eine Zusammenfassung.

Falls $ARGUMENTS einen spezifischen Report enthält:
- `traceability` → `make traceability`
- `aspice` → `make aspice-report`
- `velocity` → `make velocity-report`

```bash
# Verzeichnis anlegen falls nicht vorhanden
mkdir -p docs/reports

# Reports generieren
make <report-target>
```

Nach der Generierung: Zeige den Inhalt der generierten Datei und hebe kritische Findings hervor:
- ASPICE Report: Prozesse mit Level < Target Level
- Traceability: SWR ohne SDOC_LINK
- Velocity: Trend (steigend/fallend/stabil)
