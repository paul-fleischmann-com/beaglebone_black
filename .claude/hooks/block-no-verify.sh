#!/usr/bin/env bash
# PreToolUse Hook: Blockiert 'git commit --no-verify'
# Exit 2 = blockieren, Exit 0 = erlauben

INPUT=$(cat 2>/dev/null || echo "")

# Robust: direkt nach --no-verify im command-Feld suchen
# Nutze python3 falls vorhanden, sonst raw grep als Fallback
COMMAND=$(echo "$INPUT" | python3 -c "
import json, sys
try:
    d = json.load(sys.stdin)
    cmd = d.get('tool_input', d).get('command', '')
    print(cmd)
except Exception:
    pass
" 2>/dev/null)

# Nur blockieren wenn git commit UND --no-verify explizit im Kommando
case "$COMMAND" in
  *"git commit"*"--no-verify"*)
    echo "BLOCKED: 'git commit --no-verify' ist nicht erlaubt. Pre-commit Hooks dürfen nicht umgangen werden." >&2
    exit 2
    ;;
esac

exit 0
