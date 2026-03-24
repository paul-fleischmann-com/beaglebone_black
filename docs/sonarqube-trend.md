# SonarQube Quality Metrics Trend — Einrichtung und Nutzung

SonarQube bietet eingebautes Trend-Tracking für Quality Metrics — jeder CI-Lauf erzeugt automatisch einen Snapshot, der in der SonarQube-Oberfläche als Zeitreihe sichtbar ist.

## Was SonarQube automatisch trackt (pro CI-Run)

| Metrik | Wo sichtbar |
|--------|-------------|
| Code Coverage % | Project Overview → Activity |
| Neue Bugs / Code Smells / Vulnerabilities | Measures → Zeitachse |
| Technical Debt (Stunden) | Measures → Maintainability |
| Duplications % | Measures → Duplications |
| Quality Gate Status (pass/fail) | Project Overview → History |

> Jeder `sonar-scanner`-Lauf in CI erzeugt automatisch einen Snapshot.

## Voraussetzung: Automatic Analysis deaktivieren

**Wichtig:** SonarQube muss auf CI-basierte Analyse umgestellt werden, sonst schlägt der CI-Scanner mit Exit Code 3 fehl.

**Einmalige Einrichtung:**

1. SonarQube UI öffnen → Projekt auswählen
2. **Administration → Analysis Method**
3. **Automatic Analysis: Off** stellen

Solange Automatic Analysis aktiv ist, wird jede CI-Analyse abgewiesen.

## Was bereits aktiv ist (im beaglebone_black Projekt)

| Komponente | Konfiguration |
|------------|---------------|
| Go Coverage (Cobertura XML) | `sonar.go.coverage.reportPaths` |
| Python Coverage (coverage.xml) | `sonar.python.coverage.reportPaths` |
| Go + Python Test Results (JUnit XML) | `sonar.testExecutionReportPaths` |
| SonarQube CI Job | `.github/workflows/ci.yml` → `sonarcloud` Job |

## Branch-Vergleich bei Pull Requests (kostenlos, automatisch)

SonarQube zeigt bei jedem PR automatisch:

- Anzahl **neuer Issues** des Branches (vs. main)
- Ob der **Quality Gate** für den PR besteht
- **Coverage-Delta** des PRs

Kein Extra-Setup nötig — funktioniert sobald Automatic Analysis deaktiviert ist.

## SARIF-Reports für statische Analyse (geplant)

Sobald folgende Issues implementiert sind, zeigt der Trend auch statische Analyse Findings über Zeit:

| Issue | Tool | Sprache |
|-------|------|---------|
| #5 | bandit | Python |
| #6 | cargo clippy | Rust |
| #7 | clang-tidy | C |
| #8 | golangci-lint | Go |
| #3 | junit2sarif | Test-Failures |
| #4 | StrictDoc → SARIF | Requirements |

## Weiterführende Links

- [SonarQube Dokumentation — CI-basierte Analyse](https://docs.sonarsource.com/sonarcloud/advanced-setup/ci-based-analysis/)
- [SonarQube GitHub Action](https://github.com/SonarSource/sonarcloud-github-action)
