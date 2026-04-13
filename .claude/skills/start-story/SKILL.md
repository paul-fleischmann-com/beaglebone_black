---
description: User Story eingeben, auf Korrektheit und Umsetzbarkeit prüfen, dann SYS/SW-Requirements ableiten und Workflow starten
---

# /start-story — User Story Einstiegspunkt

Aktueller Workflow-State: !`cat .claude/workflow-state.json 2>/dev/null || echo "{}"`
Bestehende SYS-Requirements: !`grep -E "^UID:|^TITLE:" docs/requirements/system_requirements.sdoc 2>/dev/null | paste - - | sed 's/UID: //;s/TITLE: / — /' | head -20`
Bestehende SWR-Requirements: !`grep -E "^UID:|^TITLE:" docs/requirements/software_requirements.sdoc 2>/dev/null | paste - - | sed 's/UID: //;s/TITLE: / — /' | head -20`

Die User Story: $ARGUMENTS

## Schritt 1 — User Story erfassen

Falls $ARGUMENTS leer ist, bitte den User die Story im folgenden Format einzugeben:

```
Als <Rolle> möchte ich <Funktion>, damit <Nutzen>.

Akzeptanzkriterien:
- [ ] ...
- [ ] ...
```

Warte auf die Eingabe, dann weiter mit Schritt 2.

Falls $ARGUMENTS nicht leer ist, verwende die angegebene Story direkt.

## Schritt 2 — Validierung (INVEST + Umsetzbarkeit)

Prüfe die Story gegen alle Kriterien. Zeige das Ergebnis als Tabelle:

| Kriterium | Prüfung | Status |
|---|---|---|
| **I**ndependent | Ist die Story unabhängig von anderen Stories umsetzbar? | ✅/⚠️/❌ |
| **N**egotiable | Sind Implementierungsdetails noch offen (kein Micromanagement)? | ✅/⚠️/❌ |
| **V**aluable | Liefert die Story klaren Nutzen für den Anwender? | ✅/⚠️/❌ |
| **E**stimable | Ist der Umfang abschätzbar? | ✅/⚠️/❌ |
| **S**mall | Passt die Story in einen Sprint? | ✅/⚠️/❌ |
| **T**estable | Sind Akzeptanzkriterien messbar/testbar? | ✅/⚠️/❌ |
| **Korrektheit** | Story verständlich, widerspruchsfrei, vollständig? | ✅/⚠️/❌ |
| **Umsetzbarkeit** | Technisch realisierbar auf BeagleBone Black (ARM Cortex-A8, vorhandene Treiber: BME280/GPIO/UART/SPI)? | ✅/⚠️/❌ |
| **Scope** | Passt zur aktuellen Waterfall-Phase? | ✅/⚠️/❌ |

**Bei ❌ in einem Kriterium:**
- Erkläre konkret warum das Kriterium nicht erfüllt ist
- Schlage eine überarbeitete Formulierung vor
- Frage den User ob er die Story anpassen möchte
- Starte dann Schritt 2 erneut mit der überarbeiteten Story

**Erst nach ✅ oder ⚠️ in ALLEN Kriterien** (keine ❌) → weiter mit Schritt 3.

## Schritt 3 — Requirements ableiten

Leite aus der validierten Story Requirements ab. Zeige dem User die vorgeschlagenen Requirements zur Freigabe bevor du sie in SDoc schreibst:

### SYS-Requirements (system_requirements.sdoc)

Bestimme die nächste freie SYS-Nummer aus den bestehenden Requirements oben.

Schlage 1–3 SYS-Requirements vor:
```
[SYS_REQUIREMENT]
UID: SYS-XXX
TITLE: <systemseitige Anforderung>
STATEMENT: <Was das System leisten muss>
STATUS: Active
```

### SW-Requirements (software_requirements.sdoc)

Bestimme die nächste freie SWR-Nummer.

Schlage 1–5 SWR-Requirements vor (mit REQUIREMENT_TYPE):
```
[SW_REQUIREMENT]
UID: SWR-XXX
TITLE: <softwareseitige Anforderung>
STATEMENT: <Was die Software leisten muss>
STATUS: Active
REQUIREMENT_TYPE: functional|non-functional|constraint
PRIORITY: High|Medium|Low
RELATIONS:
- TYPE: Parent
  VALUE: SYS-XXX
```

Frage den User: "Sollen diese Requirements so in die SDoc-Dateien eingetragen werden? (ja/anpassen)"

## Schritt 4 — Requirements eintragen (nach Freigabe)

Trage die freigegebenen Requirements in die jeweiligen SDoc-Dateien ein:
- `docs/requirements/system_requirements.sdoc` — SYS-Requirements
- `docs/requirements/software_requirements.sdoc` — SWR-Requirements

Beachte dabei die bestehende Dateistruktur und das Grammar-Schema aus `docs/requirements/grammar.sgra`.

## Schritt 5 — GitHub Issue anlegen

Lege ein GitHub Issue für die Implementierung an:

```bash
gh issue create \
  --title "<Story-Titel kurz>" \
  --body "## User Story\n\n<Story-Text>\n\n## Akzeptanzkriterien\n<Liste>\n\n## Requirements\n- <SYS-XXX>: <Titel>\n- <SWR-XXX>: <Titel>" \
  --label "enhancement"
```

## Schritt 6 — Workflow starten

Frage den User ob er direkt mit `/start_ticket <issue-nummer>` starten möchte, um Branch anlegen, Implementierung und CI-Run zu starten.

Zeige eine Zusammenfassung:
```
✅ User Story validiert
✅ Requirements abgeleitet: <SYS-XXX>, <SWR-XXX>, ...
✅ GitHub Issue #<nr> angelegt
→ Nächster Schritt: /start_ticket <nr>
```
