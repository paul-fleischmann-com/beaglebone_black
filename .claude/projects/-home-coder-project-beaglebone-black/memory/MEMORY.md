# Memory Index

## Feedback
- [CI Python scripts as separate files](feedback_ci_python_scripts.md) — Python code gehört in `.py` files unter `scripts/`, nicht als Inline-Heredoc in GitHub Actions YAML
- [Kein Co-Author in Commits](feedback_no_coauthor_commits.md) — Keine `Co-Authored-By: Claude` Zeile in Commit-Messages
- [Issue-Auswahl per Nummer](feedback_issue_selection.md) — User gibt immer direkte Issue-Nummer an, nicht Listenposition
- [Drone: kein ${VAR} in Plain Skalaren](feedback_drone_plain_scalar_curly.md) — Drone's Parser lehnt ${} in unquotierten commands ab; fix: $VAR oder | block scalar
- [Podman login in CI](feedback_podman_login.md) — Verwende `-p "$TOKEN"` statt `echo | --password-stdin` (ioctl Fehler)
- [VERSION file vor Erhöhung prüfen](feedback_version_file_check.md) — Immer Read auf VERSION-Datei vor dem Bump, nie blind fixen Wert schreiben

## Project
- [Offener PR #152 — SonarCloud Quality Gate Fixes](project_sonar_open_pr.md) — PR #152 wartet auf CI-Ergebnis; enthält C/Shell-Fixes und sonar-project.properties-Konfiguration
