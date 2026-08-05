#!/bin/sh
# Pusht den lokalen HEAD (i.d.R. der [skip ci]-Diagramm-Commit aus
# commit-exports) robust gegen Race Conditions mit anderen, zeitgleich
# laufenden architecture-export-Builds: mehrere Läufe kurz hintereinander
# committen/pushen alle auf denselben Branch — der erste Push gewinnt, jeder
# weitere schlägt mit "non-fast-forward" fehl, wenn er einfach nur
# blind pusht (siehe Issue-Diskussion zu Build 23, wo genau das passiert
# ist: zwei überlappende Läufe, der zweite fand main schon verschoben vor).
#
# Statt sofort aufzugeben: aktuellen Remote-Stand holen, den lokalen Commit
# per Rebase obendrauf setzen, erneut versuchen — mit ein paar
# Wiederholungen, falls sich das Rennen mehrfach wiederholt.
set -eu

BRANCH=${DRONE_BRANCH:-main}
REMOTE_URL="https://x-access-token:${GIT_TOKEN}@github.com/paul-fleischmann-com/beaglebone_black.git"
MAX_ATTEMPTS=5

attempt=1
while [ "$attempt" -le "$MAX_ATTEMPTS" ]; do
  if git push "$REMOTE_URL" "HEAD:$BRANCH"; then
    echo "Push erfolgreich (Versuch $attempt/$MAX_ATTEMPTS)."
    exit 0
  fi

  if [ "$attempt" -eq "$MAX_ATTEMPTS" ]; then
    break
  fi

  echo "Push fehlgeschlagen (Versuch $attempt/$MAX_ATTEMPTS) — vermutlich Race mit einem parallel laufenden architecture-export-Build. Hole aktuellen Stand und rebase..."
  git fetch "$REMOTE_URL" "$BRANCH"
  if ! git rebase FETCH_HEAD; then
    git rebase --abort
    echo "FEHLER: Rebase auf den aktuellen $BRANCH-Stand ergab einen echten Konflikt (nicht nur ein Timing-Race) — manuell prüfen." >&2
    exit 1
  fi
  sleep 2
  attempt=$((attempt + 1))
done

echo "FEHLER: Push nach $MAX_ATTEMPTS Versuchen weiterhin fehlgeschlagen." >&2
exit 1
