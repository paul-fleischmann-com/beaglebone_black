---
name: VERSION file vor Erhöhung prüfen
description: Immer zuerst VERSION-Datei lesen bevor die Version erhöht wird
type: feedback
---

Vor jedem Bump einer VERSION-Datei (z.B. docker/bausteinsicht/VERSION) zuerst den aktuellen Inhalt mit Read lesen und dann um 1 erhöhen — nie blind einen fixen Wert schreiben.

**Why:** User hat explizit darauf hingewiesen, dass der aktuelle Stand geprüft werden soll bevor die Version erhöht wird.

**How to apply:** Bei jeder Änderung die eine VERSION-Datei betrifft: Read → aktuellen Wert ermitteln → um 1 erhöhen → schreiben.
