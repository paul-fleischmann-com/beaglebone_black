#!/usr/bin/env bash
# PreToolUse Hook: Blockiert 'git commit --no-verify'
# Exit 2 = blockieren, Exit 0 = erlauben

INPUT=$(cat 2>/dev/null || echo "")

echo "$INPUT" | python3 -c "
import json, sys, re

try:
    d = json.load(sys.stdin)
    cmd = d.get('tool_input', {}).get('command', '')
except Exception:
    sys.exit(0)

# Teile den Command in Subcommands auf (&&, ||, ;)
parts = re.split(r'\s*(?:&&|\|\||;)\s*', cmd)

for part in parts:
    part = part.strip()
    # Prüfe ob dieser Subcommand ein 'git commit' ist
    if not re.match(r'git\s+commit\b', part):
        continue
    # Schneide alles nach dem ersten -m / --message ab (Commit-Nachricht)
    msg_match = re.search(r'\s(?:-m|--message)\b', part)
    args_part = part[:msg_match.start()] if msg_match else part
    # Prüfe ob --no-verify als Flag in den Argumenten vorkommt
    if re.search(r'(?:^|\s)--no-verify(?:\s|$)', args_part):
        sys.exit(2)

sys.exit(0)
" 2>/dev/null

EXIT=$?
if [ $EXIT -eq 2 ]; then
    echo "BLOCKED: 'git commit --no-verify' ist nicht erlaubt. Pre-commit Hooks duerfen nicht umgangen werden." >&2
    exit 2
fi

exit 0
