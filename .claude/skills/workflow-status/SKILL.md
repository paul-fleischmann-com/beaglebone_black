---
name: workflow-status
description: Zeigt den vollständigen Entwicklungsprozess-Status: aktuelle Waterfall-Phase, ASPICE-Prozessstatus, laufender Sprint und offene Work Products. Aufrufen mit /workflow-status.
allowed-tools: Bash(cat *) Bash(python3 *) Bash(gh *)
---

# Workflow Status

Aktueller Stand: !`cat .claude/workflow-state.json`
Offene GitHub Issues (Top 10): !`gh issue list --state open --limit 10 --json number,title,labels 2>/dev/null || echo "[]"`

Zeige einen vollständigen Workflow-Status-Überblick für das BeagleBone Black Projekt.

## Ausgabe-Format

```
# Entwicklungsprozess-Status — BeagleBone Black
Stand: <last_updated>

## Waterfall-Phase: <current_phase>
[Tabelle aller Phasen mit Status-Icons]
Nächstes Phase-Gate: <next_phase_gate oder "nicht gesetzt">

## ASPICE Status (Target Level <aspice_target_level>)
[Tabelle aller Prozesse: SWE.1–SWE.6, MAN.3, SUP.1–SUP.10]

## Agile Sprint <current_sprint>
[Offene Issues aus obigem gh-Output]

## Offene Work Products
[open_work_products Liste, oder "Keine offenen Work Products ✅"]

## Empfohlene nächste Schritte
[Basierend auf aktuellem Status: was als nächstes angehen?]
```

Für Details zu einem spezifischen Prozess: `@workflow-manager aspice SWE.1`
Für Phasen-Gate Review: `/phase-gate`
