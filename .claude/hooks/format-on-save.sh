#!/usr/bin/env bash
# PostToolUse Hook: Formatierung und Linting nach Edit/Write
# - .go  → gofmt -w
# - .sh  → shellcheck
# - .drone.yml → validate-drone-yml.sh

INPUT=$(cat)
FILE=$(echo "$INPUT" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('tool_input',{}).get('file_path',''))" 2>/dev/null)

[ -z "$FILE" ] && exit 0
[ ! -f "$FILE" ] && exit 0

BASENAME=$(basename "$FILE")
EXT="${FILE##*.}"

case "$EXT" in
  go)
    if command -v gofmt >/dev/null 2>&1; then
      gofmt -w "$FILE"
      echo "[format-on-save] gofmt: $FILE"
    fi
    ;;
  sh)
    if command -v shellcheck >/dev/null 2>&1; then
      shellcheck "$FILE" && echo "[format-on-save] shellcheck OK: $FILE"
    fi
    ;;
esac

if [ "$BASENAME" = ".drone.yml" ]; then
  SCRIPT="$(dirname "$0")/../../scripts/validate-drone-yml.sh"
  if [ -x "$SCRIPT" ]; then
    bash "$SCRIPT" "$FILE"
  fi
fi

exit 0
