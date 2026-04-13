---
description: ASPICE Capability Level Check für einen Prozessbereich. Delegiert an @aspice-process-checker. Aufrufen mit /aspice-assessment SWE.1 oder /aspice-assessment (alle aktiven Prozesse).
---

# /aspice-assessment

Aktueller ASPICE-Status: !`python3 -c "import json; d=json.load(open('.claude/workflow-state.json')); [print(f'{k}: {v}') for k,v in d.get('process_status',{}).items()]" 2>/dev/null`

Angefragter Prozess: $ARGUMENTS

## Vorgehen

Falls $ARGUMENTS leer ist: Zeige alle Prozesse aus dem State und frage welchen der User prüfen möchte.

Falls $ARGUMENTS einen Prozess enthält (z.B. `SWE.1`): Starte direkt den @aspice-process-checker:

```
@aspice-process-checker $ARGUMENTS
```

Der @aspice-process-checker führt die vollständige Analyse durch und gibt:
- Base Practices Bewertung (BP1–BPn)
- Work Products Status
- Capability Level Einschätzung (0/1/2)
- Konkrete Gaps und Maßnahmen

## Nach dem Check

Frage den User ob der `workflow-state.json` aktualisiert werden soll:
```bash
# Bei Verbesserung des Status:
# @workflow-manager update process_status.<PROZESS> <neuer_status>
```
