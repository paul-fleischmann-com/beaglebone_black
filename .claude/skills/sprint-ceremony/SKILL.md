---
description: Agile Sprint-Ceremony starten — Planning, Review, Retrospektive oder Daily Standup. Aufrufen mit /sprint-ceremony planning, /sprint-ceremony review, /sprint-ceremony retro oder /sprint-ceremony standup.
---

# /sprint-ceremony

Aktueller Sprint: !`python3 -c "import json; print(json.load(open('.claude/workflow-state.json'))['current_sprint'])" 2>/dev/null`
Sprint-Issues: !`gh issue list --state open --limit 20 --json number,title,labels --jq '[.[] | "#\(.number) \(.title) [\(.labels | map(.name) | join(","))]"] | .[]' 2>/dev/null | head -15`

Ceremony-Typ: $ARGUMENTS

## Ceremony bestimmen

Falls $ARGUMENTS leer ist, zeige die verfügbaren Ceremonies:
```
Verfügbare Ceremonies:
  planning  — Sprint-Planung: Backlog priorisieren, Sprint füllen
  review    — Sprint-Review: Was wurde fertig? Demo-Vorbereitung
  retro     — Retrospektive: Was lief gut/schlecht? Verbesserungen
  standup   — Daily Standup: Kurzer Status (gestern/heute/Blocker)
```

---

## planning — Sprint-Planung

Delegiere an `@sprint-manager plan` für die vollständige Planung.

Zusätzlich: Erstelle GitHub Milestone für neuen Sprint falls noch nicht vorhanden:
```bash
NEXT_SPRINT=$(python3 -c "import json; print(json.load(open('.claude/workflow-state.json'))['current_sprint'] + 1)")
gh milestone create "Sprint $NEXT_SPRINT" --description "Sprint $NEXT_SPRINT Planning" 2>/dev/null
```

---

## review — Sprint-Review

### Was wurde fertig?
```bash
SPRINT=$(python3 -c "import json; print(json.load(open('.claude/workflow-state.json'))['current_sprint'])")
# Issues die seit Sprint-Start geschlossen wurden
gh issue list --state closed --limit 20 \
  --json number,title,labels,closedAt \
  --jq 'sort_by(.closedAt) | reverse | .[:10] | .[] | "#\(.number) \(.title) — \(.closedAt[:10])"'
```

### ASPICE Work Products dieses Sprints:
Prüfe welche Work Products in diesem Sprint erstellt/aktualisiert wurden:
```bash
git log --oneline --since="2 weeks ago" --name-only | grep -E "\.sdoc|traceability|review_" | sort -u
```

### Review-Vorlage ausgeben:
```
## Sprint <N> Review

### Fertig gestellt
<Liste geschlossener Issues>

### Demo-Punkte
<Was kann demonstriert werden?>

### ASPICE Work Products erstellt
<Liste neuer Work Products>

### Nicht fertig (Carry-over)
<Issues die in nächsten Sprint gehen>

### Velocity
<Issues geschlossen / Punkte>
```

---

## retro — Retrospektive

### Daten sammeln:
```bash
# CI-Erfolgsrate letzte 2 Wochen
gh run list --limit 20 --json status,conclusion,createdAt \
  --jq '[.[] | .conclusion] | group_by(.) | map({(.[0]): length}) | add' 2>/dev/null

# Offene Bugs
gh issue list --label "bug" --state open --json number,title | python3 -c "import json,sys; print(f'Offene Bugs: {len(json.load(sys.stdin))}')"

# Durchschnittliche PR-Merge-Zeit
gh pr list --state closed --limit 10 --json createdAt,mergedAt \
  --jq '[.[] | ((.mergedAt // .createdAt) | fromdateiso8601) - (.createdAt | fromdateiso8601)] | add/length/86400 | "Ø PR-Merge-Zeit: \(. | round) Tage"' 2>/dev/null
```

### Retro-Vorlage:
```
## Sprint <N> Retrospektive

### Was lief gut? ✅
- CI-Pipeline stabil: <X>% Erfolgsrate
- <weitere Punkte>

### Was lief schlecht? ❌
- <Probleme>

### Was verbessern? 🔧
- [ ] Maßnahme 1
- [ ] Maßnahme 2

### ASPICE-Prozess-Feedback
- SWE.1 Traceability: <Bewertung>
- SWE.4 Testing: <Coverage-Trend>
- SUP.1 Quality: <SonarQube-Trend>
```

---

## standup — Daily Standup

Kurzer Status-Check:
```bash
# Heutige git-Aktivität
git log --oneline --since="yesterday" --author="$(git config user.email)" 2>/dev/null | head -5

# Meine offenen Issues
gh issue list --assignee "@me" --state open --json number,title,labels \
  --jq '.[] | "#\(.number) \(.title)"' 2>/dev/null | head -5

# Offene PRs
gh pr list --author "@me" --state open --json number,title,isDraft \
  --jq '.[] | "#\(.number) \(.title)\(if .isDraft then " [DRAFT]" else "" end)"' 2>/dev/null
```

### Standup-Format:
```
## Daily Standup — <heute>

**Gestern:**
<Commits/PRs von gestern>

**Heute:**
<Aktuelle offene Issues>

**Blocker:**
<Offene PRs die Review brauchen / CI-Failures>
```
