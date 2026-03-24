#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MODEL="$SCRIPT_DIR/../arch/model/beaglebone_black.jsonc"
CMD="${1:-}"

if [[ -z "$CMD" ]]; then
  echo "Usage: $0 <command> [args...]"
  echo "Example: $0 validate"
  echo "         $0 sync"
  echo "         $0 export --output ./arch/model/export"
  exit 1
fi

# export braucht Xvfb + dbus (draw.io headless)
if [[ "$CMD" == "export" ]]; then
  sudo mkdir -p /run/dbus
  sudo dbus-daemon --system --fork 2>/dev/null || true
  shift
  xvfb-run -a "$SCRIPT_DIR/bausteinsicht" export --model "$MODEL" "$@"
else
  shift
  "$SCRIPT_DIR/bausteinsicht" "$CMD" --model "$MODEL" "$@"
fi
