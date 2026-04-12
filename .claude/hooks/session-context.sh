#!/usr/bin/env sh
# SessionStart Hook: Lädt Workflow-Kontext in die Session
# Ausgabe wird als System-Message in Claude's Kontext injiziert

STATE_FILE=".claude/workflow-state.json"

if [ ! -f "$STATE_FILE" ]; then
  exit 0
fi

# Workflow-State parsen
PHASE=$(python3 -c "import json; d=json.load(open('$STATE_FILE')); print(d.get('current_phase','?'))" 2>/dev/null)
SPRINT=$(python3 -c "import json; d=json.load(open('$STATE_FILE')); print(d.get('current_sprint','?'))" 2>/dev/null)
LEVEL=$(python3 -c "import json; d=json.load(open('$STATE_FILE')); print(d.get('aspice_target_level','?'))" 2>/dev/null)
OPEN_WP=$(python3 -c "
import json
d = json.load(open('$STATE_FILE'))
wp = d.get('open_work_products', [])
print(', '.join(wp) if wp else 'keine')
" 2>/dev/null)

cat <<EOF
[Workflow-Kontext]
Waterfall-Phase: $PHASE | Sprint: $SPRINT | ASPICE Target: Level $LEVEL
Offene Work Products: $OPEN_WP
Tipp: /workflow-status für vollständigen Überblick | @workflow-manager für Details
EOF
