---
name: VERSION file vor Erhöhung prüfen
description: Vor dem Bump zuerst latest-Version aus der Registry abfragen, dann VERSION file erhöhen
type: feedback
---

Vor jedem Bump von `docker/bausteinsicht/VERSION`:
1. **Registry abfragen**: `gh api /users/paulefl/packages/container/bausteinsicht/versions --jq '.[].metadata.container.tags'` — die `latest`-Version ermitteln
2. **VERSION file lesen**: aktuellen lokalen Wert mit Read prüfen
3. **Neue Version** = max(registry-latest, local-version) + patch — schreiben

**Why:** Lokale VERSION-Datei kann veraltet sein (fehlgeschlagene Builds pushen keine neue Version). Die Registry-latest ist die einzig zuverlässige Quelle was tatsächlich deployed wurde.

**How to apply:** Immer beide Quellen prüfen, nie blind inkrementieren.
