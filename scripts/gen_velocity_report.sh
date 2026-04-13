#!/usr/bin/env bash
# Sprint Velocity Report Generator
# Wertet GitHub Issues/Milestones aus und erstellt einen Velocity-Report
#
# Usage:
#   ./scripts/gen_velocity_report.sh
#   ./scripts/gen_velocity_report.sh --output docs/reports/velocity_report.md

set -euo pipefail

OUTPUT=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --output|-o) OUTPUT="$2"; shift 2 ;;
    *) shift ;;
  esac
done

TODAY=$(date +%Y-%m-%d)

generate_report() {
cat <<HEADER
# Sprint Velocity Report — BeagleBone Black

**Generiert:** $TODAY
**Tool:** \`scripts/gen_velocity_report.sh\`

---

HEADER

# Sprint-State aus workflow-state.json
CURRENT_SPRINT=$(python3 -c "import json; print(json.load(open('.claude/workflow-state.json'))['current_sprint'])" 2>/dev/null || echo "1")

echo "## Aktueller Sprint: Sprint $CURRENT_SPRINT"
echo ""

# Offene Issues im aktuellen Sprint
echo "### Offene Issues"
echo ""
OPEN_ISSUES=$(gh issue list --state open --limit 50 --json number,title,labels \
  --jq '.[] | "| #\(.number) | \(.title[:60]) | \(.labels | map(.name) | join(", ")) |"' 2>/dev/null || echo "")

if [ -n "$OPEN_ISSUES" ]; then
  echo "| Nr | Titel | Labels |"
  echo "|---|---|---|"
  echo "$OPEN_ISSUES"
  OPEN_COUNT=$(echo "$OPEN_ISSUES" | wc -l)
  echo ""
  echo "**Gesamt offen:** $OPEN_COUNT"
else
  echo "_Keine offenen Issues_"
fi

echo ""
echo "---"
echo ""

# Geschlossene Issues der letzten 4 Wochen
echo "## Velocity — Letzte 4 Wochen"
echo ""

CLOSED_ISSUES=$(gh issue list --state closed --limit 100 \
  --json number,title,closedAt,labels \
  --jq 'sort_by(.closedAt) | reverse | .[] | select(.closedAt >= (now - 2419200 | todate))' 2>/dev/null || echo "")

if [ -n "$CLOSED_ISSUES" ]; then
  # Gruppierung nach Woche via Python
  python3 - <<'PYEOF'
import json, sys
from datetime import datetime, timedelta

try:
    issues = json.loads(sys.stdin.read() or "[]")
except Exception:
    issues = []

# Nach Woche gruppieren
weeks = {}
for issue in issues:
    if not issue.get('closedAt'):
        continue
    dt = datetime.fromisoformat(issue['closedAt'].replace('Z', '+00:00'))
    week_start = (dt - timedelta(days=dt.weekday())).strftime('%Y-%m-%d')
    weeks.setdefault(week_start, []).append(issue)

if not weeks:
    print("_Keine Issues in den letzten 4 Wochen geschlossen_")
    sys.exit(0)

print("| Woche | Issues geschlossen | Bugs | Features |")
print("|---|---|---|---|")
total = 0
for week in sorted(weeks.keys(), reverse=True):
    items = weeks[week]
    bugs = sum(1 for i in items if any(l['name'] == 'bug' for l in i.get('labels', [])))
    features = sum(1 for i in items if any(l['name'] == 'enhancement' for l in i.get('labels', [])))
    print(f"| {week} | {len(items)} | {bugs} | {features} |")
    total += len(items)
print(f"")
print(f"**Gesamt geschlossen:** {total}")
print(f"**Ø pro Woche:** {total/max(len(weeks),1):.1f}")
PYEOF

else
  gh issue list --state closed --limit 100 \
    --json number,title,closedAt,labels 2>/dev/null | python3 - <<'PYEOF'
import json, sys
from datetime import datetime, timedelta

try:
    issues = json.load(sys.stdin)
except Exception:
    issues = []

cutoff = datetime.now().astimezone() - timedelta(weeks=4)
recent = [i for i in issues if i.get('closedAt') and
          datetime.fromisoformat(i['closedAt'].replace('Z','+00:00')) > cutoff]

weeks = {}
for issue in recent:
    dt = datetime.fromisoformat(issue['closedAt'].replace('Z', '+00:00'))
    week_start = (dt - timedelta(days=dt.weekday())).strftime('%Y-%m-%d')
    weeks.setdefault(week_start, []).append(issue)

if not weeks:
    print("_Keine Issues in den letzten 4 Wochen geschlossen_")
    sys.exit(0)

print("| Woche | Issues geschlossen | Bugs | Features |")
print("|---|---|---|---|")
total = 0
for week in sorted(weeks.keys(), reverse=True):
    items = weeks[week]
    bugs = sum(1 for i in items if any(l['name'] == 'bug' for l in i.get('labels', [])))
    features = sum(1 for i in items if any(l['name'] == 'enhancement' for l in i.get('labels', [])))
    print(f"| {week} | {len(items)} | {bugs} | {features} |")
    total += len(items)
print(f"")
print(f"**Gesamt geschlossen:** {total}")
print(f"**Ø pro Woche:** {total/max(len(weeks),1):.1f}")
PYEOF
fi

echo ""
echo "---"
echo ""

# GitHub Milestones
echo "## Milestones"
echo ""
MILESTONES=$(gh milestone list --json title,openIssues,closedIssues,dueOn \
  --jq '.[] | "| \(.title) | \(.openIssues) | \(.closedIssues) | \(.dueOn // "-") |"' 2>/dev/null || echo "")

if [ -n "$MILESTONES" ]; then
  echo "| Milestone | Offen | Geschlossen | Fällig |"
  echo "|---|---|---|---|"
  echo "$MILESTONES"
else
  echo "_Keine Milestones vorhanden_"
fi

echo ""
echo "---"
echo ""
echo "*Erstellt mit \`make velocity-report\` | Aktualisieren: \`make velocity-report\`*"
}

if [ -n "$OUTPUT" ]; then
  mkdir -p "$(dirname "$OUTPUT")"
  generate_report > "$OUTPUT"
  echo "Velocity Report geschrieben: $OUTPUT"
else
  generate_report
fi
