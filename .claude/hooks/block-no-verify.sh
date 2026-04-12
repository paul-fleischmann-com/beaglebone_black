#!/usr/bin/env bash
# PreToolUse Hook: Blockiert 'git commit --no-verify'
# Exit 2 = blockieren, Exit 0 = erlauben

INPUT=$(cat 2>/dev/null || echo "")

COMMAND=$(echo "$INPUT" | python3 -c "
import json, sys
try:
    d = json.load(sys.stdin)
    print(d.get('tool_input', {}).get('command', ''))
except Exception:
    pass
" 2>/dev/null)

# Nur blockieren wenn EXAKT 'git commit' UND '--no-verify' im Kommando
case "$COMMAND" in
  *"git commit"*"--no-verify"*)
    echo "BLOCKED: 'git commit --no-verify' ist nicht erlaubt. Pre-commit Hooks dürfen nicht umgangen werden." >&2
    exit 2
    ;;
esac

exit 0
