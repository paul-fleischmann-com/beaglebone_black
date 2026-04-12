#!/usr/bin/env bash
# PreToolUse Hook: Schützt .env*-Dateien vor Edits
# Exit 2 = blockieren, Exit 0 = erlauben

INPUT=$(cat)
FILE=$(echo "$INPUT" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('tool_input',{}).get('file_path',''))" 2>/dev/null)
BASENAME=$(basename "$FILE")

case "$BASENAME" in
  .env|.env.*|*.env|.envrc)
    echo "BLOCKED: '$FILE' enthält möglicherweise Secrets und darf nicht editiert werden." >&2
    exit 2
    ;;
esac

exit 0
