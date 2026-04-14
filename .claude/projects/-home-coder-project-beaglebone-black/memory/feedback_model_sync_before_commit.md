---
name: Bausteinsicht-Modell vor Commit synchronisieren
description: Vor jedem Commit mit Source-Änderungen beaglebone_black.jsonc auf Sync mit Code prüfen und ggf. aktualisieren
type: feedback
---

Vor jedem Commit der Source-Dateien ändert (`project/**`, `tools/**`) muss `arch/model/beaglebone_black.jsonc` geprüft und bei Bedarf aktualisiert werden.

**Why:** User hat explizit gefordert dass das Architekturmodell immer synchron mit dem Code-Stand bleibt.

**How to apply:** 
1. Nach Source-Änderungen: bausteinsicht-generator Agent aufrufen mit Auftrag, Modell gegen Code zu prüfen
2. Bei Abweichungen: Modell aktualisieren lassen
3. `arch/model/beaglebone_black.jsonc` in denselben Commit aufnehmen wie die Source-Änderungen
