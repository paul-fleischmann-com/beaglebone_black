#!/bin/sh
# Generic step wrapper: schreibt Start-Timestamp, führt CMD aus, schreibt Dauer.
#
# Verwendung via Umgebungsvariablen (Drone environment: Block):
#   STEP  — Name des Steps (= Dateiname in .step-status/)
#   CMD   — Shell-Befehl der ausgeführt werden soll (wird via sh -c ausgeführt)
#
# Beispiel in .drone.yml:
#   environment:
#     STEP: test-hal-unit
#     CMD: (cd project/go-api && go test ./...)
#   commands:
#     - sh scripts/run-step.sh

set -e

if [ -z "$STEP" ]; then
  echo "ERROR: STEP env var nicht gesetzt" >&2
  exit 1
fi
if [ -z "$CMD" ]; then
  echo "ERROR: CMD env var nicht gesetzt" >&2
  exit 1
fi

mkdir -p .step-status
date +%s > .step-status/${STEP}.start

sh -c "$CMD"
EXIT=$?

echo $(($(date +%s) - $(cat .step-status/${STEP}.start 2>/dev/null || date +%s))) > .step-status/${STEP}
exit $EXIT
