#!/usr/bin/env bash
# Validiert .drone.yml auf Syntax-Fehler und bekannte Anti-Pattern
# Usage: validate-drone-yml.sh [path/to/.drone.yml]

FILE="${1:-.drone.yml}"
ERRORS=0
WARNINGS=0

if [ ! -f "$FILE" ]; then
  echo "[drone-lint] Datei nicht gefunden: $FILE" >&2
  exit 1
fi

# 1. YAML-Syntaxprüfung
if command -v python3 >/dev/null 2>&1; then
  YAML_ERR=$(python3 -c "import yaml; list(yaml.safe_load_all(open('$FILE')))" 2>&1)
  if [ $? -ne 0 ]; then
    echo "[drone-lint] FEHLER: YAML-Syntaxfehler in $FILE:" >&2
    echo "$YAML_ERR" >&2
    ERRORS=$((ERRORS + 1))
  fi
fi

# 2. Anti-Pattern: ${VAR} in unquotierten Plain-Skalaren
if grep -nP '^\s+command:\s+[^'\''"]\S*\$\{' "$FILE" 2>/dev/null | grep -q .; then
  echo "[drone-lint] WARNUNG: \${VAR} in unquotiertem command-Feld gefunden (Drone-Parser-Problem). Verwende \$VAR oder Block-Scalar |" >&2
  grep -nP '^\s+command:\s+[^'\''"]\S*\$\{' "$FILE" 2>/dev/null >&2
  WARNINGS=$((WARNINGS + 1))
fi

# 3. Anti-Pattern: --password-stdin via echo/pipe (ioctl-Fehler mit Podman rootless)
if grep -n 'echo.*|.*--password-stdin\|password-stdin.*echo' "$FILE" 2>/dev/null | grep -q .; then
  echo "[drone-lint] WARNUNG: 'echo | --password-stdin' gefunden — verursacht ioctl-Fehler mit Podman. Verwende '-p \"\$TOKEN\"'" >&2
  WARNINGS=$((WARNINGS + 1))
fi

# Ergebnis
if [ $ERRORS -gt 0 ]; then
  echo "[drone-lint] $FILE: $ERRORS Fehler, $WARNINGS Warnungen" >&2
  exit 1
elif [ $WARNINGS -gt 0 ]; then
  echo "[drone-lint] $FILE: OK ($WARNINGS Warnungen)"
else
  echo "[drone-lint] $FILE: OK"
fi

exit 0
