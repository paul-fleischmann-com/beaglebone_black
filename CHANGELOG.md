# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Infrastruktur & Tooling

- Use container script instead of inline podman commands 
- Separate build step from run commands 
- Add export-diagram, export-table and export-png steps 
- Commit export changes back to repo if files changed 
- Update exported diagrams [skip ci] 
- Update exported diagrams [skip ci] 
- Trigger only on beaglebone_black.jsonc changes 
- Trigger SonarCloud verification 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Gruppierung nach Software-Änderungen und Infrastruktur & Tooling (#65) (#65)
- Erstelle PR statt direktem Push auf main (branch protection fix) (#66) (#66)
- Update unreleased section [skip ci] (#67) (#67)
- Update unreleased section [skip ci] (#69) (#69)
- Update unreleased section [skip ci] (#71) (#71)
- Update unreleased section [skip ci] (#73) (#73)
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] (#76) (#76)
- Add entry for Issue #31 fix (#75) [skip ci] 
- Update unreleased section [skip ci] (#78) (#78)
- Add entry for Issue #21 fix (#77) [skip ci] 
- Update unreleased section [skip ci] (#80) (#80)
- Add entry for Issue #27 fix (#79) [skip ci] 
- Update unreleased section [skip ci] (#82) (#82)
- Update unreleased section [skip ci] (#89) (#89)
- Beaglebone-tooling auf v1.1.0 aktualisieren (#90) (#90)
- Update unreleased section [skip ci] (#91) (#91)
- Bump beaglebone-tooling actions to v1.1.1 
- Update unreleased section [skip ci] (#92) (#92)
- Bump beaglebone-tooling actions to v1.1.2 
- Update unreleased section [skip ci] (#93) (#93)
- Update unreleased section [skip ci] (#94) (#94)
- Bump beaglebone-tooling actions to v1.1.3 
- Update unreleased section [skip ci] (#95) (#95)
- Bump beaglebone-tooling actions to v1.1.4 
- Update unreleased section [skip ci] (#96) (#96)
- Bump beaglebone-tooling actions to v1.1.5 
- Update unreleased section [skip ci] (#97) (#97)
- Bump beaglebone-tooling actions to v1.1.6 
- Update unreleased section [skip ci] (#98) (#98)
- Replace all inline steps with beaglebone-tooling composite actions @v1.1.7 
- Update unreleased section [skip ci] (#99) (#99)
- Bump beaglebone-tooling actions to v1.1.8 
- Update unreleased section [skip ci] (#100) (#100)
- Bump beaglebone-tooling actions to v1.1.10 (fix junit_to_sarif) 
- Update unreleased section [skip ci] (#102) (#102)
- Update unreleased section [skip ci] (#103) (#103)
- Bump beaglebone-tooling to v1.1.12 
- Update unreleased section [skip ci] (#104) (#104)
- Bump beaglebone-tooling to v1.1.13 
- Update unreleased section [skip ci] (#105) (#105)
- Update unreleased section [skip ci] (#106) (#106)
- Bump beaglebone-tooling to v1.1.14 (#107)
- Update unreleased section [skip ci] (#108) (#108)
- Update unreleased section [skip ci] (#109) (#109)
- Bump beaglebone-tooling to v1.1.15 (#110)
- Update unreleased section [skip ci] (#111) (#111)
- Bump beaglebone-tooling to v1.1.16 (#123)
- Update unreleased section [skip ci] (#124) (#124)
- Update unreleased section [skip ci] (#125) (#125)
- Download-tooling auf v1.1.16 aktualisieren (konsistent mit anderen Actions) 
- Update unreleased section [skip ci] (#126) (#126)
- Update unreleased section [skip ci] (#128) (#128)
- Bump beaglebone-tooling auf v1.1.17 (alle Actions konsistent) 
- Update unreleased section [skip ci] (#129) (#129)
- Bump beaglebone-tooling to v1.1.18, rename shellcheck-sarif → shellcheck 
- Update unreleased section [skip ci] (#131) (#131)
- Update unreleased section [skip ci] (#133) (#133)
- Bump beaglebone-tooling to v1.1.19 (#134)
- Update unreleased section [skip ci] (#135) (#135)
- Update unreleased section [skip ci] (#137) (#137)
- Update unreleased section [skip ci] (#145) (#145)
- Bump beaglebone-tooling to v1.1.20 (#146)
- Update unreleased section [skip ci] (#147) (#147)
- Bump beaglebone-tooling to v1.1.21 (#149)
- Update unreleased section [skip ci] (#148) (#148)
- Update unreleased section [skip ci] (#154) (#154)

### Software-Änderungen

- Podman container script and CI workflow (#45) (#46) (#46)
- Mount model dir rw, fix export paths, add export dirs step 
- Disable git credential prompt for public repo clone 
- Bypass git credential helper for public repo clone 
- Move git clone to workflow step, script only builds image 
- Use actions/checkout to clone Bausteinsicht repo 
- Drop container approach, run binary directly in CI 
- Install draw.io CLI and use xvfb-run for PNG export 
- SonarCloud Integration für Quality Monitoring (#47) (#48) (#48)
- Remove duplicate OUTPUT env for git-cliff, increase Pages smoke-test sleep to 30s 
- Replace fixed sleep with retry loop for Pages smoke-test (max 3min) 
- Git-cliff write to temp file then prepend to CHANGELOG.md 
- Copy bb_dashboard.html to index.html for GitHub Pages 
- Start_ticket zeigt automatisch Issue-Liste bei leerem Argument (#61) (#61)
- Automatisches PR-Review mit Bot-Token-Support in start_ticket (#64) (#64)
- ShellCheck SARIF Report für SonarCloud (#55) (#68) (#68)
- Deaktiviere C/C++ SonarCloud-Analyse + verbessertes Error Reporting (#70) (#70)
- POST /api/v1/backend wechselt jetzt tatsächlich den HAL-Backend (#72) (#72)
- Trend-Cache Git-Fallback via reports-Branch (#74) (#74)
- POST-Handler geben 400 bei ungültigem JSON zurück (#75) (#75)
- HTTP-Server mit ReadTimeout/WriteTimeout/IdleTimeout (Issue #21) (#77) (#77)
- Regression Test für BME280StreamHandler Flusher nil-Check (Issue #27) (#79) (#79)
- Flag.Parse() aus Library-Package entfernt (Issue #26) (#81) (#81)
- CORS OPTIONS Preflight-Requests behandeln (Issue #22) (#83) (#83)
- Collect_results.py + statisch/dynamisch Trennung (Issue #15) (#84) (#84)
- Phase 1 — Tooling in tooling/ Ordner gruppieren (Issue #85) (#86) (#86)
- Phase 3 — tooling/ aus Repo entfernen, via Release-Download (Issue #85) (#87) (#87)
- C Code Coverage CI-Integration (#88) (#88)
- Use download-tooling composite action 
- Use go-test composite action 
- Use shellcheck-sarif and c-test composite actions 
- Add explicit download-tooling step before go-test 
- Git worktree --orphan syntax für git 2.40+ 
- Use strictdoc and test-report composite actions 
- Use sonarcloud composite action 
- Remove download-tooling steps — scripts via GITHUB_ACTION_PATH 
- Add security-events:write for SARIF upload, bump to v1.1.9 
- Add strictdoc SARIF + requirements coverage, bump to v1.1.11 
- Alle SARIF- und Rust-Coverage-Pfade in sonar-project.properties ergänzen 
- SonarQube Issues Report in CI einbinden 
- Default case (*) in report.sh + tooling-Scan im CI (Issue #115) (#117) (#117)
- Download-tooling Step durch shellcheck-sarif include-tooling ersetzen 
- Duplicate string literals durch Konstanten ersetzen (S1192 CRITICAL) (#132) (#132)
- If-Statement auf neue Zeile, else ergänzt in bme280.c (S3972 CRITICAL) (#136) (#136)
- Explizite Casts für integer precision conversions in bme280.c und spi.c (S5276 MAJOR) (#144) (#144)
- SonarCloud Quality Gate Wait aktivieren — PR-Merge bei neuen Issues blockieren 
- Changelog race condition — rebase auf origin/main vor Branch-Erstellung 
- ShellCheck-Findings SC2034/SC2188/SC2069/SC2064 beheben (#143) (#150) (#150)
- Add scripts/ to sonar.sources for SARIF path resolution (#151) (#151)
- Resolve Quality Gate issues and SARIF path resolution (#152) (#152)


# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixes

- fix(shell): ShellCheck-Findings SC2034/SC2188/SC2069/SC2064 in Tooling-Scripts und `scripts/install.sh` behoben (#143)

### Infrastruktur & Tooling

- Use container script instead of inline podman commands 
- Separate build step from run commands 
- Add export-diagram, export-table and export-png steps 
- Commit export changes back to repo if files changed 
- Update exported diagrams [skip ci] 
- Update exported diagrams [skip ci] 
- Trigger only on beaglebone_black.jsonc changes 
- Trigger SonarCloud verification 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Gruppierung nach Software-Änderungen und Infrastruktur & Tooling (#65) (#65)
- Erstelle PR statt direktem Push auf main (branch protection fix) (#66) (#66)
- Update unreleased section [skip ci] (#67) (#67)
- Update unreleased section [skip ci] (#69) (#69)
- Update unreleased section [skip ci] (#71) (#71)
- Update unreleased section [skip ci] (#73) (#73)
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] (#76) (#76)
- Add entry for Issue #31 fix (#75) [skip ci] 
- Update unreleased section [skip ci] (#78) (#78)
- Add entry for Issue #21 fix (#77) [skip ci] 
- Update unreleased section [skip ci] (#80) (#80)
- Add entry for Issue #27 fix (#79) [skip ci] 
- Update unreleased section [skip ci] (#82) (#82)
- Update unreleased section [skip ci] (#89) (#89)
- Beaglebone-tooling auf v1.1.0 aktualisieren (#90) (#90)
- Update unreleased section [skip ci] (#91) (#91)
- Bump beaglebone-tooling actions to v1.1.1 
- Update unreleased section [skip ci] (#92) (#92)
- Bump beaglebone-tooling actions to v1.1.2 
- Update unreleased section [skip ci] (#93) (#93)
- Update unreleased section [skip ci] (#94) (#94)
- Bump beaglebone-tooling actions to v1.1.3 
- Update unreleased section [skip ci] (#95) (#95)
- Bump beaglebone-tooling actions to v1.1.4 
- Update unreleased section [skip ci] (#96) (#96)
- Bump beaglebone-tooling actions to v1.1.5 
- Update unreleased section [skip ci] (#97) (#97)
- Bump beaglebone-tooling actions to v1.1.6 
- Update unreleased section [skip ci] (#98) (#98)
- Replace all inline steps with beaglebone-tooling composite actions @v1.1.7 
- Update unreleased section [skip ci] (#99) (#99)
- Bump beaglebone-tooling actions to v1.1.8 
- Update unreleased section [skip ci] (#100) (#100)
- Bump beaglebone-tooling actions to v1.1.10 (fix junit_to_sarif) 
- Update unreleased section [skip ci] (#102) (#102)
- Update unreleased section [skip ci] (#103) (#103)
- Bump beaglebone-tooling to v1.1.12 
- Update unreleased section [skip ci] (#104) (#104)
- Bump beaglebone-tooling to v1.1.13 
- Update unreleased section [skip ci] (#105) (#105)
- Update unreleased section [skip ci] (#106) (#106)
- Bump beaglebone-tooling to v1.1.14 (#107)
- Update unreleased section [skip ci] (#108) (#108)
- Update unreleased section [skip ci] (#109) (#109)
- Bump beaglebone-tooling to v1.1.15 (#110)
- Update unreleased section [skip ci] (#111) (#111)
- Bump beaglebone-tooling to v1.1.16 (#123)
- Update unreleased section [skip ci] (#124) (#124)
- Update unreleased section [skip ci] (#125) (#125)
- Download-tooling auf v1.1.16 aktualisieren (konsistent mit anderen Actions) 
- Update unreleased section [skip ci] (#126) (#126)
- Update unreleased section [skip ci] (#128) (#128)
- Bump beaglebone-tooling auf v1.1.17 (alle Actions konsistent) 
- Update unreleased section [skip ci] (#129) (#129)
- Bump beaglebone-tooling to v1.1.18, rename shellcheck-sarif → shellcheck 
- Update unreleased section [skip ci] (#131) (#131)
- Update unreleased section [skip ci] (#133) (#133)
- Bump beaglebone-tooling to v1.1.19 (#134)
- Update unreleased section [skip ci] (#135) (#135)
- Update unreleased section [skip ci] (#137) (#137)
- Update unreleased section [skip ci] (#145) (#145)

### Software-Änderungen

- Podman container script and CI workflow (#45) (#46) (#46)
- Mount model dir rw, fix export paths, add export dirs step 
- Disable git credential prompt for public repo clone 
- Bypass git credential helper for public repo clone 
- Move git clone to workflow step, script only builds image 
- Use actions/checkout to clone Bausteinsicht repo 
- Drop container approach, run binary directly in CI 
- Install draw.io CLI and use xvfb-run for PNG export 
- SonarCloud Integration für Quality Monitoring (#47) (#48) (#48)
- Remove duplicate OUTPUT env for git-cliff, increase Pages smoke-test sleep to 30s 
- Replace fixed sleep with retry loop for Pages smoke-test (max 3min) 
- Git-cliff write to temp file then prepend to CHANGELOG.md 
- Copy bb_dashboard.html to index.html for GitHub Pages 
- Start_ticket zeigt automatisch Issue-Liste bei leerem Argument (#61) (#61)
- Automatisches PR-Review mit Bot-Token-Support in start_ticket (#64) (#64)
- ShellCheck SARIF Report für SonarCloud (#55) (#68) (#68)
- Deaktiviere C/C++ SonarCloud-Analyse + verbessertes Error Reporting (#70) (#70)
- POST /api/v1/backend wechselt jetzt tatsächlich den HAL-Backend (#72) (#72)
- Trend-Cache Git-Fallback via reports-Branch (#74) (#74)
- POST-Handler geben 400 bei ungültigem JSON zurück (#75) (#75)
- HTTP-Server mit ReadTimeout/WriteTimeout/IdleTimeout (Issue #21) (#77) (#77)
- Regression Test für BME280StreamHandler Flusher nil-Check (Issue #27) (#79) (#79)
- Flag.Parse() aus Library-Package entfernt (Issue #26) (#81) (#81)
- CORS OPTIONS Preflight-Requests behandeln (Issue #22) (#83) (#83)
- Collect_results.py + statisch/dynamisch Trennung (Issue #15) (#84) (#84)
- Phase 1 — Tooling in tooling/ Ordner gruppieren (Issue #85) (#86) (#86)
- Phase 3 — tooling/ aus Repo entfernen, via Release-Download (Issue #85) (#87) (#87)
- C Code Coverage CI-Integration (#88) (#88)
- Use download-tooling composite action 
- Use go-test composite action 
- Use shellcheck-sarif and c-test composite actions 
- Add explicit download-tooling step before go-test 
- Git worktree --orphan syntax für git 2.40+ 
- Use strictdoc and test-report composite actions 
- Use sonarcloud composite action 
- Remove download-tooling steps — scripts via GITHUB_ACTION_PATH 
- Add security-events:write for SARIF upload, bump to v1.1.9 
- Add strictdoc SARIF + requirements coverage, bump to v1.1.11 
- Alle SARIF- und Rust-Coverage-Pfade in sonar-project.properties ergänzen 
- SonarQube Issues Report in CI einbinden 
- Default case (*) in report.sh + tooling-Scan im CI (Issue #115) (#117) (#117)
- Download-tooling Step durch shellcheck-sarif include-tooling ersetzen 
- Duplicate string literals durch Konstanten ersetzen (S1192 CRITICAL) (#132) (#132)
- If-Statement auf neue Zeile, else ergänzt in bme280.c (S3972 CRITICAL) (#136) (#136)
- Explizite Casts für integer precision conversions in bme280.c und spi.c (S5276 MAJOR) (#144) (#144)
- SonarCloud Quality Gate Wait aktivieren — PR-Merge bei neuen Issues blockieren 


# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Infrastruktur & Tooling

- Use container script instead of inline podman commands 
- Separate build step from run commands 
- Add export-diagram, export-table and export-png steps 
- Commit export changes back to repo if files changed 
- Update exported diagrams [skip ci] 
- Update exported diagrams [skip ci] 
- Trigger only on beaglebone_black.jsonc changes 
- Trigger SonarCloud verification 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Gruppierung nach Software-Änderungen und Infrastruktur & Tooling (#65) (#65)
- Erstelle PR statt direktem Push auf main (branch protection fix) (#66) (#66)
- Update unreleased section [skip ci] (#67) (#67)
- Update unreleased section [skip ci] (#69) (#69)
- Update unreleased section [skip ci] (#71) (#71)
- Update unreleased section [skip ci] (#73) (#73)
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] (#76) (#76)
- Add entry for Issue #31 fix (#75) [skip ci] 
- Update unreleased section [skip ci] (#78) (#78)
- Add entry for Issue #21 fix (#77) [skip ci] 
- Update unreleased section [skip ci] (#80) (#80)
- Add entry for Issue #27 fix (#79) [skip ci] 
- Update unreleased section [skip ci] (#82) (#82)
- Update unreleased section [skip ci] (#89) (#89)
- Beaglebone-tooling auf v1.1.0 aktualisieren (#90) (#90)
- Update unreleased section [skip ci] (#91) (#91)
- Bump beaglebone-tooling actions to v1.1.1 
- Update unreleased section [skip ci] (#92) (#92)
- Bump beaglebone-tooling actions to v1.1.2 
- Update unreleased section [skip ci] (#93) (#93)
- Update unreleased section [skip ci] (#94) (#94)
- Bump beaglebone-tooling actions to v1.1.3 
- Update unreleased section [skip ci] (#95) (#95)
- Bump beaglebone-tooling actions to v1.1.4 
- Update unreleased section [skip ci] (#96) (#96)
- Bump beaglebone-tooling actions to v1.1.5 
- Update unreleased section [skip ci] (#97) (#97)
- Bump beaglebone-tooling actions to v1.1.6 
- Update unreleased section [skip ci] (#98) (#98)
- Replace all inline steps with beaglebone-tooling composite actions @v1.1.7 
- Update unreleased section [skip ci] (#99) (#99)
- Bump beaglebone-tooling actions to v1.1.8 
- Update unreleased section [skip ci] (#100) (#100)
- Bump beaglebone-tooling actions to v1.1.10 (fix junit_to_sarif) 
- Update unreleased section [skip ci] (#102) (#102)
- Update unreleased section [skip ci] (#103) (#103)
- Bump beaglebone-tooling to v1.1.12 
- Update unreleased section [skip ci] (#104) (#104)
- Bump beaglebone-tooling to v1.1.13 
- Update unreleased section [skip ci] (#105) (#105)
- Update unreleased section [skip ci] (#106) (#106)
- Bump beaglebone-tooling to v1.1.14 (#107)
- Update unreleased section [skip ci] (#108) (#108)
- Update unreleased section [skip ci] (#109) (#109)
- Bump beaglebone-tooling to v1.1.15 (#110)
- Update unreleased section [skip ci] (#111) (#111)
- Bump beaglebone-tooling to v1.1.16 (#123)
- Update unreleased section [skip ci] (#124) (#124)
- Update unreleased section [skip ci] (#125) (#125)
- Download-tooling auf v1.1.16 aktualisieren (konsistent mit anderen Actions) 
- Update unreleased section [skip ci] (#126) (#126)
- Update unreleased section [skip ci] (#128) (#128)
- Bump beaglebone-tooling auf v1.1.17 (alle Actions konsistent) 
- Update unreleased section [skip ci] (#129) (#129)
- Bump beaglebone-tooling to v1.1.18, rename shellcheck-sarif → shellcheck 
- Update unreleased section [skip ci] (#131) (#131)
- Update unreleased section [skip ci] (#133) (#133)
- Bump beaglebone-tooling to v1.1.19 (#134)
- Update unreleased section [skip ci] (#135) (#135)
- Update unreleased section [skip ci] (#137) (#137)
- Update unreleased section [skip ci] (#145) (#145)
- Bump beaglebone-tooling to v1.1.20 (#146)

### Software-Änderungen

- Podman container script and CI workflow (#45) (#46) (#46)
- Mount model dir rw, fix export paths, add export dirs step 
- Disable git credential prompt for public repo clone 
- Bypass git credential helper for public repo clone 
- Move git clone to workflow step, script only builds image 
- Use actions/checkout to clone Bausteinsicht repo 
- Drop container approach, run binary directly in CI 
- Install draw.io CLI and use xvfb-run for PNG export 
- SonarCloud Integration für Quality Monitoring (#47) (#48) (#48)
- Remove duplicate OUTPUT env for git-cliff, increase Pages smoke-test sleep to 30s 
- Replace fixed sleep with retry loop for Pages smoke-test (max 3min) 
- Git-cliff write to temp file then prepend to CHANGELOG.md 
- Copy bb_dashboard.html to index.html for GitHub Pages 
- Start_ticket zeigt automatisch Issue-Liste bei leerem Argument (#61) (#61)
- Automatisches PR-Review mit Bot-Token-Support in start_ticket (#64) (#64)
- ShellCheck SARIF Report für SonarCloud (#55) (#68) (#68)
- Deaktiviere C/C++ SonarCloud-Analyse + verbessertes Error Reporting (#70) (#70)
- POST /api/v1/backend wechselt jetzt tatsächlich den HAL-Backend (#72) (#72)
- Trend-Cache Git-Fallback via reports-Branch (#74) (#74)
- POST-Handler geben 400 bei ungültigem JSON zurück (#75) (#75)
- HTTP-Server mit ReadTimeout/WriteTimeout/IdleTimeout (Issue #21) (#77) (#77)
- Regression Test für BME280StreamHandler Flusher nil-Check (Issue #27) (#79) (#79)
- Flag.Parse() aus Library-Package entfernt (Issue #26) (#81) (#81)
- CORS OPTIONS Preflight-Requests behandeln (Issue #22) (#83) (#83)
- Collect_results.py + statisch/dynamisch Trennung (Issue #15) (#84) (#84)
- Phase 1 — Tooling in tooling/ Ordner gruppieren (Issue #85) (#86) (#86)
- Phase 3 — tooling/ aus Repo entfernen, via Release-Download (Issue #85) (#87) (#87)
- C Code Coverage CI-Integration (#88) (#88)
- Use download-tooling composite action 
- Use go-test composite action 
- Use shellcheck-sarif and c-test composite actions 
- Add explicit download-tooling step before go-test 
- Git worktree --orphan syntax für git 2.40+ 
- Use strictdoc and test-report composite actions 
- Use sonarcloud composite action 
- Remove download-tooling steps — scripts via GITHUB_ACTION_PATH 
- Add security-events:write for SARIF upload, bump to v1.1.9 
- Add strictdoc SARIF + requirements coverage, bump to v1.1.11 
- Alle SARIF- und Rust-Coverage-Pfade in sonar-project.properties ergänzen 
- SonarQube Issues Report in CI einbinden 
- Default case (*) in report.sh + tooling-Scan im CI (Issue #115) (#117) (#117)
- Download-tooling Step durch shellcheck-sarif include-tooling ersetzen 
- Duplicate string literals durch Konstanten ersetzen (S1192 CRITICAL) (#132) (#132)
- If-Statement auf neue Zeile, else ergänzt in bme280.c (S3972 CRITICAL) (#136) (#136)
- Explizite Casts für integer precision conversions in bme280.c und spi.c (S5276 MAJOR) (#144) (#144)
- SonarCloud Quality Gate Wait aktivieren — PR-Merge bei neuen Issues blockieren 


# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Infrastruktur & Tooling

- Use container script instead of inline podman commands 
- Separate build step from run commands 
- Add export-diagram, export-table and export-png steps 
- Commit export changes back to repo if files changed 
- Update exported diagrams [skip ci] 
- Update exported diagrams [skip ci] 
- Trigger only on beaglebone_black.jsonc changes 
- Trigger SonarCloud verification 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Gruppierung nach Software-Änderungen und Infrastruktur & Tooling (#65) (#65)
- Erstelle PR statt direktem Push auf main (branch protection fix) (#66) (#66)
- Update unreleased section [skip ci] (#67) (#67)
- Update unreleased section [skip ci] (#69) (#69)
- Update unreleased section [skip ci] (#71) (#71)
- Update unreleased section [skip ci] (#73) (#73)
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] (#76) (#76)
- Add entry for Issue #31 fix (#75) [skip ci] 
- Update unreleased section [skip ci] (#78) (#78)
- Add entry for Issue #21 fix (#77) [skip ci] 
- Update unreleased section [skip ci] (#80) (#80)
- Add entry for Issue #27 fix (#79) [skip ci] 
- Update unreleased section [skip ci] (#82) (#82)
- Update unreleased section [skip ci] (#89) (#89)
- Beaglebone-tooling auf v1.1.0 aktualisieren (#90) (#90)
- Update unreleased section [skip ci] (#91) (#91)
- Bump beaglebone-tooling actions to v1.1.1 
- Update unreleased section [skip ci] (#92) (#92)
- Bump beaglebone-tooling actions to v1.1.2 
- Update unreleased section [skip ci] (#93) (#93)
- Update unreleased section [skip ci] (#94) (#94)
- Bump beaglebone-tooling actions to v1.1.3 
- Update unreleased section [skip ci] (#95) (#95)
- Bump beaglebone-tooling actions to v1.1.4 
- Update unreleased section [skip ci] (#96) (#96)
- Bump beaglebone-tooling actions to v1.1.5 
- Update unreleased section [skip ci] (#97) (#97)
- Bump beaglebone-tooling actions to v1.1.6 
- Update unreleased section [skip ci] (#98) (#98)
- Replace all inline steps with beaglebone-tooling composite actions @v1.1.7 
- Update unreleased section [skip ci] (#99) (#99)
- Bump beaglebone-tooling actions to v1.1.8 
- Update unreleased section [skip ci] (#100) (#100)
- Bump beaglebone-tooling actions to v1.1.10 (fix junit_to_sarif) 
- Update unreleased section [skip ci] (#102) (#102)
- Update unreleased section [skip ci] (#103) (#103)
- Bump beaglebone-tooling to v1.1.12 
- Update unreleased section [skip ci] (#104) (#104)
- Bump beaglebone-tooling to v1.1.13 
- Update unreleased section [skip ci] (#105) (#105)
- Update unreleased section [skip ci] (#106) (#106)
- Bump beaglebone-tooling to v1.1.14 (#107)
- Update unreleased section [skip ci] (#108) (#108)
- Update unreleased section [skip ci] (#109) (#109)
- Bump beaglebone-tooling to v1.1.15 (#110)
- Update unreleased section [skip ci] (#111) (#111)
- Bump beaglebone-tooling to v1.1.16 (#123)
- Update unreleased section [skip ci] (#124) (#124)
- Update unreleased section [skip ci] (#125) (#125)
- Download-tooling auf v1.1.16 aktualisieren (konsistent mit anderen Actions) 
- Update unreleased section [skip ci] (#126) (#126)
- Update unreleased section [skip ci] (#128) (#128)
- Bump beaglebone-tooling auf v1.1.17 (alle Actions konsistent) 
- Update unreleased section [skip ci] (#129) (#129)
- Bump beaglebone-tooling to v1.1.18, rename shellcheck-sarif → shellcheck 
- Update unreleased section [skip ci] (#131) (#131)
- Update unreleased section [skip ci] (#133) (#133)
- Bump beaglebone-tooling to v1.1.19 (#134)
- Update unreleased section [skip ci] (#135) (#135)
- Update unreleased section [skip ci] (#137) (#137)
- Update unreleased section [skip ci] (#145) (#145)
- Bump beaglebone-tooling to v1.1.20 (#146)

### Software-Änderungen

- Podman container script and CI workflow (#45) (#46) (#46)
- Mount model dir rw, fix export paths, add export dirs step 
- Disable git credential prompt for public repo clone 
- Bypass git credential helper for public repo clone 
- Move git clone to workflow step, script only builds image 
- Use actions/checkout to clone Bausteinsicht repo 
- Drop container approach, run binary directly in CI 
- Install draw.io CLI and use xvfb-run for PNG export 
- SonarCloud Integration für Quality Monitoring (#47) (#48) (#48)
- Remove duplicate OUTPUT env for git-cliff, increase Pages smoke-test sleep to 30s 
- Replace fixed sleep with retry loop for Pages smoke-test (max 3min) 
- Git-cliff write to temp file then prepend to CHANGELOG.md 
- Copy bb_dashboard.html to index.html for GitHub Pages 
- Start_ticket zeigt automatisch Issue-Liste bei leerem Argument (#61) (#61)
- Automatisches PR-Review mit Bot-Token-Support in start_ticket (#64) (#64)
- ShellCheck SARIF Report für SonarCloud (#55) (#68) (#68)
- Deaktiviere C/C++ SonarCloud-Analyse + verbessertes Error Reporting (#70) (#70)
- POST /api/v1/backend wechselt jetzt tatsächlich den HAL-Backend (#72) (#72)
- Trend-Cache Git-Fallback via reports-Branch (#74) (#74)
- POST-Handler geben 400 bei ungültigem JSON zurück (#75) (#75)
- HTTP-Server mit ReadTimeout/WriteTimeout/IdleTimeout (Issue #21) (#77) (#77)
- Regression Test für BME280StreamHandler Flusher nil-Check (Issue #27) (#79) (#79)
- Flag.Parse() aus Library-Package entfernt (Issue #26) (#81) (#81)
- CORS OPTIONS Preflight-Requests behandeln (Issue #22) (#83) (#83)
- Collect_results.py + statisch/dynamisch Trennung (Issue #15) (#84) (#84)
- Phase 1 — Tooling in tooling/ Ordner gruppieren (Issue #85) (#86) (#86)
- Phase 3 — tooling/ aus Repo entfernen, via Release-Download (Issue #85) (#87) (#87)
- C Code Coverage CI-Integration (#88) (#88)
- Use download-tooling composite action 
- Use go-test composite action 
- Use shellcheck-sarif and c-test composite actions 
- Add explicit download-tooling step before go-test 
- Git worktree --orphan syntax für git 2.40+ 
- Use strictdoc and test-report composite actions 
- Use sonarcloud composite action 
- Remove download-tooling steps — scripts via GITHUB_ACTION_PATH 
- Add security-events:write for SARIF upload, bump to v1.1.9 
- Add strictdoc SARIF + requirements coverage, bump to v1.1.11 
- Alle SARIF- und Rust-Coverage-Pfade in sonar-project.properties ergänzen 
- SonarQube Issues Report in CI einbinden 
- Default case (*) in report.sh + tooling-Scan im CI (Issue #115) (#117) (#117)
- Download-tooling Step durch shellcheck-sarif include-tooling ersetzen 
- Duplicate string literals durch Konstanten ersetzen (S1192 CRITICAL) (#132) (#132)
- If-Statement auf neue Zeile, else ergänzt in bme280.c (S3972 CRITICAL) (#136) (#136)
- Explizite Casts für integer precision conversions in bme280.c und spi.c (S5276 MAJOR) (#144) (#144)
- SonarCloud Quality Gate Wait aktivieren — PR-Merge bei neuen Issues blockieren 


# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Infrastruktur & Tooling

- Use container script instead of inline podman commands 
- Separate build step from run commands 
- Add export-diagram, export-table and export-png steps 
- Commit export changes back to repo if files changed 
- Update exported diagrams [skip ci] 
- Update exported diagrams [skip ci] 
- Trigger only on beaglebone_black.jsonc changes 
- Trigger SonarCloud verification 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Gruppierung nach Software-Änderungen und Infrastruktur & Tooling (#65) (#65)
- Erstelle PR statt direktem Push auf main (branch protection fix) (#66) (#66)
- Update unreleased section [skip ci] (#67) (#67)
- Update unreleased section [skip ci] (#69) (#69)
- Update unreleased section [skip ci] (#71) (#71)
- Update unreleased section [skip ci] (#73) (#73)
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] (#76) (#76)
- Add entry for Issue #31 fix (#75) [skip ci] 
- Update unreleased section [skip ci] (#78) (#78)
- Add entry for Issue #21 fix (#77) [skip ci] 
- Update unreleased section [skip ci] (#80) (#80)
- Add entry for Issue #27 fix (#79) [skip ci] 
- Update unreleased section [skip ci] (#82) (#82)
- Update unreleased section [skip ci] (#89) (#89)
- Beaglebone-tooling auf v1.1.0 aktualisieren (#90) (#90)
- Update unreleased section [skip ci] (#91) (#91)
- Bump beaglebone-tooling actions to v1.1.1 
- Update unreleased section [skip ci] (#92) (#92)
- Bump beaglebone-tooling actions to v1.1.2 
- Update unreleased section [skip ci] (#93) (#93)
- Update unreleased section [skip ci] (#94) (#94)
- Bump beaglebone-tooling actions to v1.1.3 
- Update unreleased section [skip ci] (#95) (#95)
- Bump beaglebone-tooling actions to v1.1.4 
- Update unreleased section [skip ci] (#96) (#96)
- Bump beaglebone-tooling actions to v1.1.5 
- Update unreleased section [skip ci] (#97) (#97)
- Bump beaglebone-tooling actions to v1.1.6 
- Update unreleased section [skip ci] (#98) (#98)
- Replace all inline steps with beaglebone-tooling composite actions @v1.1.7 
- Update unreleased section [skip ci] (#99) (#99)
- Bump beaglebone-tooling actions to v1.1.8 
- Update unreleased section [skip ci] (#100) (#100)
- Bump beaglebone-tooling actions to v1.1.10 (fix junit_to_sarif) 
- Update unreleased section [skip ci] (#102) (#102)
- Update unreleased section [skip ci] (#103) (#103)
- Bump beaglebone-tooling to v1.1.12 
- Update unreleased section [skip ci] (#104) (#104)
- Bump beaglebone-tooling to v1.1.13 
- Update unreleased section [skip ci] (#105) (#105)
- Update unreleased section [skip ci] (#106) (#106)
- Bump beaglebone-tooling to v1.1.14 (#107)
- Update unreleased section [skip ci] (#108) (#108)
- Update unreleased section [skip ci] (#109) (#109)
- Bump beaglebone-tooling to v1.1.15 (#110)
- Update unreleased section [skip ci] (#111) (#111)
- Bump beaglebone-tooling to v1.1.16 (#123)
- Update unreleased section [skip ci] (#124) (#124)
- Update unreleased section [skip ci] (#125) (#125)
- Download-tooling auf v1.1.16 aktualisieren (konsistent mit anderen Actions) 
- Update unreleased section [skip ci] (#126) (#126)
- Update unreleased section [skip ci] (#128) (#128)
- Bump beaglebone-tooling auf v1.1.17 (alle Actions konsistent) 
- Update unreleased section [skip ci] (#129) (#129)
- Bump beaglebone-tooling to v1.1.18, rename shellcheck-sarif → shellcheck 
- Update unreleased section [skip ci] (#131) (#131)
- Update unreleased section [skip ci] (#133) (#133)
- Bump beaglebone-tooling to v1.1.19 (#134)
- Update unreleased section [skip ci] (#135) (#135)
- Update unreleased section [skip ci] (#137) (#137)

### Software-Änderungen

- Podman container script and CI workflow (#45) (#46) (#46)
- Mount model dir rw, fix export paths, add export dirs step 
- Disable git credential prompt for public repo clone 
- Bypass git credential helper for public repo clone 
- Move git clone to workflow step, script only builds image 
- Use actions/checkout to clone Bausteinsicht repo 
- Drop container approach, run binary directly in CI 
- Install draw.io CLI and use xvfb-run for PNG export 
- SonarCloud Integration für Quality Monitoring (#47) (#48) (#48)
- Remove duplicate OUTPUT env for git-cliff, increase Pages smoke-test sleep to 30s 
- Replace fixed sleep with retry loop for Pages smoke-test (max 3min) 
- Git-cliff write to temp file then prepend to CHANGELOG.md 
- Copy bb_dashboard.html to index.html for GitHub Pages 
- Start_ticket zeigt automatisch Issue-Liste bei leerem Argument (#61) (#61)
- Automatisches PR-Review mit Bot-Token-Support in start_ticket (#64) (#64)
- ShellCheck SARIF Report für SonarCloud (#55) (#68) (#68)
- Deaktiviere C/C++ SonarCloud-Analyse + verbessertes Error Reporting (#70) (#70)
- POST /api/v1/backend wechselt jetzt tatsächlich den HAL-Backend (#72) (#72)
- Trend-Cache Git-Fallback via reports-Branch (#74) (#74)
- POST-Handler geben 400 bei ungültigem JSON zurück (#75) (#75)
- HTTP-Server mit ReadTimeout/WriteTimeout/IdleTimeout (Issue #21) (#77) (#77)
- Regression Test für BME280StreamHandler Flusher nil-Check (Issue #27) (#79) (#79)
- Flag.Parse() aus Library-Package entfernt (Issue #26) (#81) (#81)
- CORS OPTIONS Preflight-Requests behandeln (Issue #22) (#83) (#83)
- Collect_results.py + statisch/dynamisch Trennung (Issue #15) (#84) (#84)
- Phase 1 — Tooling in tooling/ Ordner gruppieren (Issue #85) (#86) (#86)
- Phase 3 — tooling/ aus Repo entfernen, via Release-Download (Issue #85) (#87) (#87)
- C Code Coverage CI-Integration (#88) (#88)
- Use download-tooling composite action 
- Use go-test composite action 
- Use shellcheck-sarif and c-test composite actions 
- Add explicit download-tooling step before go-test 
- Git worktree --orphan syntax für git 2.40+ 
- Use strictdoc and test-report composite actions 
- Use sonarcloud composite action 
- Remove download-tooling steps — scripts via GITHUB_ACTION_PATH 
- Add security-events:write for SARIF upload, bump to v1.1.9 
- Add strictdoc SARIF + requirements coverage, bump to v1.1.11 
- Alle SARIF- und Rust-Coverage-Pfade in sonar-project.properties ergänzen 
- SonarQube Issues Report in CI einbinden 
- Default case (*) in report.sh + tooling-Scan im CI (Issue #115) (#117) (#117)
- Download-tooling Step durch shellcheck-sarif include-tooling ersetzen 
- Duplicate string literals durch Konstanten ersetzen (S1192 CRITICAL) (#132) (#132)
- If-Statement auf neue Zeile, else ergänzt in bme280.c (S3972 CRITICAL) (#136) (#136)
- Explizite Casts für integer precision conversions in bme280.c und spi.c (S5276 MAJOR) (#144) (#144)


# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixes

- fix(c): explizite Casts für integer precision conversions in `bme280.c` und `spi.c`, neue Hilfsmakros `pack2bytesInUint16`/`pack2bytesInInt16` (SonarQube c:S5276 MAJOR, #138)

### Infrastruktur & Tooling

- Use container script instead of inline podman commands 
- Separate build step from run commands 
- Add export-diagram, export-table and export-png steps 
- Commit export changes back to repo if files changed 
- Update exported diagrams [skip ci] 
- Update exported diagrams [skip ci] 
- Trigger only on beaglebone_black.jsonc changes 
- Trigger SonarCloud verification 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Gruppierung nach Software-Änderungen und Infrastruktur & Tooling (#65) (#65)
- Erstelle PR statt direktem Push auf main (branch protection fix) (#66) (#66)
- Update unreleased section [skip ci] (#67) (#67)
- Update unreleased section [skip ci] (#69) (#69)
- Update unreleased section [skip ci] (#71) (#71)
- Update unreleased section [skip ci] (#73) (#73)
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] (#76) (#76)
- Add entry for Issue #31 fix (#75) [skip ci] 
- Update unreleased section [skip ci] (#78) (#78)
- Add entry for Issue #21 fix (#77) [skip ci] 
- Update unreleased section [skip ci] (#80) (#80)
- Add entry for Issue #27 fix (#79) [skip ci] 
- Update unreleased section [skip ci] (#82) (#82)
- Update unreleased section [skip ci] (#89) (#89)
- Beaglebone-tooling auf v1.1.0 aktualisieren (#90) (#90)
- Update unreleased section [skip ci] (#91) (#91)
- Bump beaglebone-tooling actions to v1.1.1 
- Update unreleased section [skip ci] (#92) (#92)
- Bump beaglebone-tooling actions to v1.1.2 
- Update unreleased section [skip ci] (#93) (#93)
- Update unreleased section [skip ci] (#94) (#94)
- Bump beaglebone-tooling actions to v1.1.3 
- Update unreleased section [skip ci] (#95) (#95)
- Bump beaglebone-tooling actions to v1.1.4 
- Update unreleased section [skip ci] (#96) (#96)
- Bump beaglebone-tooling actions to v1.1.5 
- Update unreleased section [skip ci] (#97) (#97)
- Bump beaglebone-tooling actions to v1.1.6 
- Update unreleased section [skip ci] (#98) (#98)
- Replace all inline steps with beaglebone-tooling composite actions @v1.1.7 
- Update unreleased section [skip ci] (#99) (#99)
- Bump beaglebone-tooling actions to v1.1.8 
- Update unreleased section [skip ci] (#100) (#100)
- Bump beaglebone-tooling actions to v1.1.10 (fix junit_to_sarif) 
- Update unreleased section [skip ci] (#102) (#102)
- Update unreleased section [skip ci] (#103) (#103)
- Bump beaglebone-tooling to v1.1.12 
- Update unreleased section [skip ci] (#104) (#104)
- Bump beaglebone-tooling to v1.1.13 
- Update unreleased section [skip ci] (#105) (#105)
- Update unreleased section [skip ci] (#106) (#106)
- Bump beaglebone-tooling to v1.1.14 (#107)
- Update unreleased section [skip ci] (#108) (#108)
- Update unreleased section [skip ci] (#109) (#109)
- Bump beaglebone-tooling to v1.1.15 (#110)
- Update unreleased section [skip ci] (#111) (#111)
- Bump beaglebone-tooling to v1.1.16 (#123)
- Update unreleased section [skip ci] (#124) (#124)
- Update unreleased section [skip ci] (#125) (#125)
- Download-tooling auf v1.1.16 aktualisieren (konsistent mit anderen Actions) 
- Update unreleased section [skip ci] (#126) (#126)
- Update unreleased section [skip ci] (#128) (#128)
- Bump beaglebone-tooling auf v1.1.17 (alle Actions konsistent) 
- Update unreleased section [skip ci] (#129) (#129)
- Bump beaglebone-tooling to v1.1.18, rename shellcheck-sarif → shellcheck 
- Update unreleased section [skip ci] (#131) (#131)
- Update unreleased section [skip ci] (#133) (#133)
- Bump beaglebone-tooling to v1.1.19 (#134)
- Update unreleased section [skip ci] (#135) (#135)

### Software-Änderungen

- Podman container script and CI workflow (#45) (#46) (#46)
- Mount model dir rw, fix export paths, add export dirs step 
- Disable git credential prompt for public repo clone 
- Bypass git credential helper for public repo clone 
- Move git clone to workflow step, script only builds image 
- Use actions/checkout to clone Bausteinsicht repo 
- Drop container approach, run binary directly in CI 
- Install draw.io CLI and use xvfb-run for PNG export 
- SonarCloud Integration für Quality Monitoring (#47) (#48) (#48)
- Remove duplicate OUTPUT env for git-cliff, increase Pages smoke-test sleep to 30s 
- Replace fixed sleep with retry loop for Pages smoke-test (max 3min) 
- Git-cliff write to temp file then prepend to CHANGELOG.md 
- Copy bb_dashboard.html to index.html for GitHub Pages 
- Start_ticket zeigt automatisch Issue-Liste bei leerem Argument (#61) (#61)
- Automatisches PR-Review mit Bot-Token-Support in start_ticket (#64) (#64)
- ShellCheck SARIF Report für SonarCloud (#55) (#68) (#68)
- Deaktiviere C/C++ SonarCloud-Analyse + verbessertes Error Reporting (#70) (#70)
- POST /api/v1/backend wechselt jetzt tatsächlich den HAL-Backend (#72) (#72)
- Trend-Cache Git-Fallback via reports-Branch (#74) (#74)
- POST-Handler geben 400 bei ungültigem JSON zurück (#75) (#75)
- HTTP-Server mit ReadTimeout/WriteTimeout/IdleTimeout (Issue #21) (#77) (#77)
- Regression Test für BME280StreamHandler Flusher nil-Check (Issue #27) (#79) (#79)
- Flag.Parse() aus Library-Package entfernt (Issue #26) (#81) (#81)
- CORS OPTIONS Preflight-Requests behandeln (Issue #22) (#83) (#83)
- Collect_results.py + statisch/dynamisch Trennung (Issue #15) (#84) (#84)
- Phase 1 — Tooling in tooling/ Ordner gruppieren (Issue #85) (#86) (#86)
- Phase 3 — tooling/ aus Repo entfernen, via Release-Download (Issue #85) (#87) (#87)
- C Code Coverage CI-Integration (#88) (#88)
- Use download-tooling composite action 
- Use go-test composite action 
- Use shellcheck-sarif and c-test composite actions 
- Add explicit download-tooling step before go-test 
- Git worktree --orphan syntax für git 2.40+ 
- Use strictdoc and test-report composite actions 
- Use sonarcloud composite action 
- Remove download-tooling steps — scripts via GITHUB_ACTION_PATH 
- Add security-events:write for SARIF upload, bump to v1.1.9 
- Add strictdoc SARIF + requirements coverage, bump to v1.1.11 
- Alle SARIF- und Rust-Coverage-Pfade in sonar-project.properties ergänzen 
- SonarQube Issues Report in CI einbinden 
- Default case (*) in report.sh + tooling-Scan im CI (Issue #115) (#117) (#117)
- Download-tooling Step durch shellcheck-sarif include-tooling ersetzen 
- Duplicate string literals durch Konstanten ersetzen (S1192 CRITICAL) (#132) (#132)
- If-Statement auf neue Zeile, else ergänzt in bme280.c (S3972 CRITICAL) (#136) (#136)


# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixes

- fix(c): if-Statement auf neue Zeile und else ergänzt in bme280.c — SonarQube S3972 CRITICAL (#116)

### Infrastruktur & Tooling

- Use container script instead of inline podman commands 
- Separate build step from run commands 
- Add export-diagram, export-table and export-png steps 
- Commit export changes back to repo if files changed 
- Update exported diagrams [skip ci] 
- Update exported diagrams [skip ci] 
- Trigger only on beaglebone_black.jsonc changes 
- Trigger SonarCloud verification 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Gruppierung nach Software-Änderungen und Infrastruktur & Tooling (#65) (#65)
- Erstelle PR statt direktem Push auf main (branch protection fix) (#66) (#66)
- Update unreleased section [skip ci] (#67) (#67)
- Update unreleased section [skip ci] (#69) (#69)
- Update unreleased section [skip ci] (#71) (#71)
- Update unreleased section [skip ci] (#73) (#73)
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] (#76) (#76)
- Add entry for Issue #31 fix (#75) [skip ci] 
- Update unreleased section [skip ci] (#78) (#78)
- Add entry for Issue #21 fix (#77) [skip ci] 
- Update unreleased section [skip ci] (#80) (#80)
- Add entry for Issue #27 fix (#79) [skip ci] 
- Update unreleased section [skip ci] (#82) (#82)
- Update unreleased section [skip ci] (#89) (#89)
- Beaglebone-tooling auf v1.1.0 aktualisieren (#90) (#90)
- Update unreleased section [skip ci] (#91) (#91)
- Bump beaglebone-tooling actions to v1.1.1 
- Update unreleased section [skip ci] (#92) (#92)
- Bump beaglebone-tooling actions to v1.1.2 
- Update unreleased section [skip ci] (#93) (#93)
- Update unreleased section [skip ci] (#94) (#94)
- Bump beaglebone-tooling actions to v1.1.3 
- Update unreleased section [skip ci] (#95) (#95)
- Bump beaglebone-tooling actions to v1.1.4 
- Update unreleased section [skip ci] (#96) (#96)
- Bump beaglebone-tooling actions to v1.1.5 
- Update unreleased section [skip ci] (#97) (#97)
- Bump beaglebone-tooling actions to v1.1.6 
- Update unreleased section [skip ci] (#98) (#98)
- Replace all inline steps with beaglebone-tooling composite actions @v1.1.7 
- Update unreleased section [skip ci] (#99) (#99)
- Bump beaglebone-tooling actions to v1.1.8 
- Update unreleased section [skip ci] (#100) (#100)
- Bump beaglebone-tooling actions to v1.1.10 (fix junit_to_sarif) 
- Update unreleased section [skip ci] (#102) (#102)
- Update unreleased section [skip ci] (#103) (#103)
- Bump beaglebone-tooling to v1.1.12 
- Update unreleased section [skip ci] (#104) (#104)
- Bump beaglebone-tooling to v1.1.13 
- Update unreleased section [skip ci] (#105) (#105)
- Update unreleased section [skip ci] (#106) (#106)
- Bump beaglebone-tooling to v1.1.14 (#107)
- Update unreleased section [skip ci] (#108) (#108)
- Update unreleased section [skip ci] (#109) (#109)
- Bump beaglebone-tooling to v1.1.15 (#110)
- Update unreleased section [skip ci] (#111) (#111)
- Bump beaglebone-tooling to v1.1.16 (#123)
- Update unreleased section [skip ci] (#124) (#124)
- Update unreleased section [skip ci] (#125) (#125)
- Download-tooling auf v1.1.16 aktualisieren (konsistent mit anderen Actions) 
- Update unreleased section [skip ci] (#126) (#126)
- Update unreleased section [skip ci] (#128) (#128)
- Bump beaglebone-tooling auf v1.1.17 (alle Actions konsistent) 
- Update unreleased section [skip ci] (#129) (#129)
- Bump beaglebone-tooling to v1.1.18, rename shellcheck-sarif → shellcheck 
- Update unreleased section [skip ci] (#131) (#131)
- Update unreleased section [skip ci] (#133) (#133)
- Bump beaglebone-tooling to v1.1.19 (#134)

### Software-Änderungen

- Podman container script and CI workflow (#45) (#46) (#46)
- Mount model dir rw, fix export paths, add export dirs step 
- Disable git credential prompt for public repo clone 
- Bypass git credential helper for public repo clone 
- Move git clone to workflow step, script only builds image 
- Use actions/checkout to clone Bausteinsicht repo 
- Drop container approach, run binary directly in CI 
- Install draw.io CLI and use xvfb-run for PNG export 
- SonarCloud Integration für Quality Monitoring (#47) (#48) (#48)
- Remove duplicate OUTPUT env for git-cliff, increase Pages smoke-test sleep to 30s 
- Replace fixed sleep with retry loop for Pages smoke-test (max 3min) 
- Git-cliff write to temp file then prepend to CHANGELOG.md 
- Copy bb_dashboard.html to index.html for GitHub Pages 
- Start_ticket zeigt automatisch Issue-Liste bei leerem Argument (#61) (#61)
- Automatisches PR-Review mit Bot-Token-Support in start_ticket (#64) (#64)
- ShellCheck SARIF Report für SonarCloud (#55) (#68) (#68)
- Deaktiviere C/C++ SonarCloud-Analyse + verbessertes Error Reporting (#70) (#70)
- POST /api/v1/backend wechselt jetzt tatsächlich den HAL-Backend (#72) (#72)
- Trend-Cache Git-Fallback via reports-Branch (#74) (#74)
- POST-Handler geben 400 bei ungültigem JSON zurück (#75) (#75)
- HTTP-Server mit ReadTimeout/WriteTimeout/IdleTimeout (Issue #21) (#77) (#77)
- Regression Test für BME280StreamHandler Flusher nil-Check (Issue #27) (#79) (#79)
- Flag.Parse() aus Library-Package entfernt (Issue #26) (#81) (#81)
- CORS OPTIONS Preflight-Requests behandeln (Issue #22) (#83) (#83)
- Collect_results.py + statisch/dynamisch Trennung (Issue #15) (#84) (#84)
- Phase 1 — Tooling in tooling/ Ordner gruppieren (Issue #85) (#86) (#86)
- Phase 3 — tooling/ aus Repo entfernen, via Release-Download (Issue #85) (#87) (#87)
- C Code Coverage CI-Integration (#88) (#88)
- Use download-tooling composite action 
- Use go-test composite action 
- Use shellcheck-sarif and c-test composite actions 
- Add explicit download-tooling step before go-test 
- Git worktree --orphan syntax für git 2.40+ 
- Use strictdoc and test-report composite actions 
- Use sonarcloud composite action 
- Remove download-tooling steps — scripts via GITHUB_ACTION_PATH 
- Add security-events:write for SARIF upload, bump to v1.1.9 
- Add strictdoc SARIF + requirements coverage, bump to v1.1.11 
- Alle SARIF- und Rust-Coverage-Pfade in sonar-project.properties ergänzen 
- SonarQube Issues Report in CI einbinden 
- Default case (*) in report.sh + tooling-Scan im CI (Issue #115) (#117) (#117)
- Download-tooling Step durch shellcheck-sarif include-tooling ersetzen 
- Duplicate string literals durch Konstanten ersetzen (S1192 CRITICAL) (#132) (#132)


# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Infrastruktur & Tooling

- Use container script instead of inline podman commands 
- Separate build step from run commands 
- Add export-diagram, export-table and export-png steps 
- Commit export changes back to repo if files changed 
- Update exported diagrams [skip ci] 
- Update exported diagrams [skip ci] 
- Trigger only on beaglebone_black.jsonc changes 
- Trigger SonarCloud verification 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Gruppierung nach Software-Änderungen und Infrastruktur & Tooling (#65) (#65)
- Erstelle PR statt direktem Push auf main (branch protection fix) (#66) (#66)
- Update unreleased section [skip ci] (#67) (#67)
- Update unreleased section [skip ci] (#69) (#69)
- Update unreleased section [skip ci] (#71) (#71)
- Update unreleased section [skip ci] (#73) (#73)
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] (#76) (#76)
- Add entry for Issue #31 fix (#75) [skip ci] 
- Update unreleased section [skip ci] (#78) (#78)
- Add entry for Issue #21 fix (#77) [skip ci] 
- Update unreleased section [skip ci] (#80) (#80)
- Add entry for Issue #27 fix (#79) [skip ci] 
- Update unreleased section [skip ci] (#82) (#82)
- Update unreleased section [skip ci] (#89) (#89)
- Beaglebone-tooling auf v1.1.0 aktualisieren (#90) (#90)
- Update unreleased section [skip ci] (#91) (#91)
- Bump beaglebone-tooling actions to v1.1.1 
- Update unreleased section [skip ci] (#92) (#92)
- Bump beaglebone-tooling actions to v1.1.2 
- Update unreleased section [skip ci] (#93) (#93)
- Update unreleased section [skip ci] (#94) (#94)
- Bump beaglebone-tooling actions to v1.1.3 
- Update unreleased section [skip ci] (#95) (#95)
- Bump beaglebone-tooling actions to v1.1.4 
- Update unreleased section [skip ci] (#96) (#96)
- Bump beaglebone-tooling actions to v1.1.5 
- Update unreleased section [skip ci] (#97) (#97)
- Bump beaglebone-tooling actions to v1.1.6 
- Update unreleased section [skip ci] (#98) (#98)
- Replace all inline steps with beaglebone-tooling composite actions @v1.1.7 
- Update unreleased section [skip ci] (#99) (#99)
- Bump beaglebone-tooling actions to v1.1.8 
- Update unreleased section [skip ci] (#100) (#100)
- Bump beaglebone-tooling actions to v1.1.10 (fix junit_to_sarif) 
- Update unreleased section [skip ci] (#102) (#102)
- Update unreleased section [skip ci] (#103) (#103)
- Bump beaglebone-tooling to v1.1.12 
- Update unreleased section [skip ci] (#104) (#104)
- Bump beaglebone-tooling to v1.1.13 
- Update unreleased section [skip ci] (#105) (#105)
- Update unreleased section [skip ci] (#106) (#106)
- Bump beaglebone-tooling to v1.1.14 (#107)
- Update unreleased section [skip ci] (#108) (#108)
- Update unreleased section [skip ci] (#109) (#109)
- Bump beaglebone-tooling to v1.1.15 (#110)
- Update unreleased section [skip ci] (#111) (#111)
- Bump beaglebone-tooling to v1.1.16 (#123)
- Update unreleased section [skip ci] (#124) (#124)
- Update unreleased section [skip ci] (#125) (#125)
- Download-tooling auf v1.1.16 aktualisieren (konsistent mit anderen Actions) 
- Update unreleased section [skip ci] (#126) (#126)
- Update unreleased section [skip ci] (#128) (#128)
- Bump beaglebone-tooling auf v1.1.17 (alle Actions konsistent) 
- Update unreleased section [skip ci] (#129) (#129)
- Bump beaglebone-tooling to v1.1.18, rename shellcheck-sarif → shellcheck 
- Update unreleased section [skip ci] (#131) (#131)

### Software-Änderungen

- Podman container script and CI workflow (#45) (#46) (#46)
- Mount model dir rw, fix export paths, add export dirs step 
- Disable git credential prompt for public repo clone 
- Bypass git credential helper for public repo clone 
- Move git clone to workflow step, script only builds image 
- Use actions/checkout to clone Bausteinsicht repo 
- Drop container approach, run binary directly in CI 
- Install draw.io CLI and use xvfb-run for PNG export 
- SonarCloud Integration für Quality Monitoring (#47) (#48) (#48)
- Remove duplicate OUTPUT env for git-cliff, increase Pages smoke-test sleep to 30s 
- Replace fixed sleep with retry loop for Pages smoke-test (max 3min) 
- Git-cliff write to temp file then prepend to CHANGELOG.md 
- Copy bb_dashboard.html to index.html for GitHub Pages 
- Start_ticket zeigt automatisch Issue-Liste bei leerem Argument (#61) (#61)
- Automatisches PR-Review mit Bot-Token-Support in start_ticket (#64) (#64)
- ShellCheck SARIF Report für SonarCloud (#55) (#68) (#68)
- Deaktiviere C/C++ SonarCloud-Analyse + verbessertes Error Reporting (#70) (#70)
- POST /api/v1/backend wechselt jetzt tatsächlich den HAL-Backend (#72) (#72)
- Trend-Cache Git-Fallback via reports-Branch (#74) (#74)
- POST-Handler geben 400 bei ungültigem JSON zurück (#75) (#75)
- HTTP-Server mit ReadTimeout/WriteTimeout/IdleTimeout (Issue #21) (#77) (#77)
- Regression Test für BME280StreamHandler Flusher nil-Check (Issue #27) (#79) (#79)
- Flag.Parse() aus Library-Package entfernt (Issue #26) (#81) (#81)
- CORS OPTIONS Preflight-Requests behandeln (Issue #22) (#83) (#83)
- Collect_results.py + statisch/dynamisch Trennung (Issue #15) (#84) (#84)
- Phase 1 — Tooling in tooling/ Ordner gruppieren (Issue #85) (#86) (#86)
- Phase 3 — tooling/ aus Repo entfernen, via Release-Download (Issue #85) (#87) (#87)
- C Code Coverage CI-Integration (#88) (#88)
- Use download-tooling composite action 
- Use go-test composite action 
- Use shellcheck-sarif and c-test composite actions 
- Add explicit download-tooling step before go-test 
- Git worktree --orphan syntax für git 2.40+ 
- Use strictdoc and test-report composite actions 
- Use sonarcloud composite action 
- Remove download-tooling steps — scripts via GITHUB_ACTION_PATH 
- Add security-events:write for SARIF upload, bump to v1.1.9 
- Add strictdoc SARIF + requirements coverage, bump to v1.1.11 
- Alle SARIF- und Rust-Coverage-Pfade in sonar-project.properties ergänzen 
- SonarQube Issues Report in CI einbinden 
- Default case (*) in report.sh + tooling-Scan im CI (Issue #115) (#117) (#117)
- Download-tooling Step durch shellcheck-sarif include-tooling ersetzen 
- Duplicate string literals durch Konstanten ersetzen (S1192 CRITICAL) (#132) (#132)


# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Refactoring

- refactor(go): Duplicate string literals durch Konstanten ersetzen — `colorPrimary`, `gpioAPIPath`, `gpioValueHigh`, `spiModeDefault`, `errInvalidBody` (SonarQube S1192 CRITICAL, #112)

### Infrastruktur & Tooling

- Use container script instead of inline podman commands 
- Separate build step from run commands 
- Add export-diagram, export-table and export-png steps 
- Commit export changes back to repo if files changed 
- Update exported diagrams [skip ci] 
- Update exported diagrams [skip ci] 
- Trigger only on beaglebone_black.jsonc changes 
- Trigger SonarCloud verification 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Gruppierung nach Software-Änderungen und Infrastruktur & Tooling (#65) (#65)
- Erstelle PR statt direktem Push auf main (branch protection fix) (#66) (#66)
- Update unreleased section [skip ci] (#67) (#67)
- Update unreleased section [skip ci] (#69) (#69)
- Update unreleased section [skip ci] (#71) (#71)
- Update unreleased section [skip ci] (#73) (#73)
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] (#76) (#76)
- Add entry for Issue #31 fix (#75) [skip ci] 
- Update unreleased section [skip ci] (#78) (#78)
- Add entry for Issue #21 fix (#77) [skip ci] 
- Update unreleased section [skip ci] (#80) (#80)
- Add entry for Issue #27 fix (#79) [skip ci] 
- Update unreleased section [skip ci] (#82) (#82)
- Update unreleased section [skip ci] (#89) (#89)
- Beaglebone-tooling auf v1.1.0 aktualisieren (#90) (#90)
- Update unreleased section [skip ci] (#91) (#91)
- Bump beaglebone-tooling actions to v1.1.1 
- Update unreleased section [skip ci] (#92) (#92)
- Bump beaglebone-tooling actions to v1.1.2 
- Update unreleased section [skip ci] (#93) (#93)
- Update unreleased section [skip ci] (#94) (#94)
- Bump beaglebone-tooling actions to v1.1.3 
- Update unreleased section [skip ci] (#95) (#95)
- Bump beaglebone-tooling actions to v1.1.4 
- Update unreleased section [skip ci] (#96) (#96)
- Bump beaglebone-tooling actions to v1.1.5 
- Update unreleased section [skip ci] (#97) (#97)
- Bump beaglebone-tooling actions to v1.1.6 
- Update unreleased section [skip ci] (#98) (#98)
- Replace all inline steps with beaglebone-tooling composite actions @v1.1.7 
- Update unreleased section [skip ci] (#99) (#99)
- Bump beaglebone-tooling actions to v1.1.8 
- Update unreleased section [skip ci] (#100) (#100)
- Bump beaglebone-tooling actions to v1.1.10 (fix junit_to_sarif) 
- Update unreleased section [skip ci] (#102) (#102)
- Update unreleased section [skip ci] (#103) (#103)
- Bump beaglebone-tooling to v1.1.12 
- Update unreleased section [skip ci] (#104) (#104)
- Bump beaglebone-tooling to v1.1.13 
- Update unreleased section [skip ci] (#105) (#105)
- Update unreleased section [skip ci] (#106) (#106)
- Bump beaglebone-tooling to v1.1.14 (#107)
- Update unreleased section [skip ci] (#108) (#108)
- Update unreleased section [skip ci] (#109) (#109)
- Bump beaglebone-tooling to v1.1.15 (#110)
- Update unreleased section [skip ci] (#111) (#111)
- Bump beaglebone-tooling to v1.1.16 (#123)
- Update unreleased section [skip ci] (#124) (#124)
- Update unreleased section [skip ci] (#125) (#125)
- Download-tooling auf v1.1.16 aktualisieren (konsistent mit anderen Actions) 
- Update unreleased section [skip ci] (#126) (#126)
- Update unreleased section [skip ci] (#128) (#128)
- Bump beaglebone-tooling auf v1.1.17 (alle Actions konsistent) 
- Update unreleased section [skip ci] (#129) (#129)
- Bump beaglebone-tooling to v1.1.18, rename shellcheck-sarif → shellcheck 

### Software-Änderungen

- Podman container script and CI workflow (#45) (#46) (#46)
- Mount model dir rw, fix export paths, add export dirs step 
- Disable git credential prompt for public repo clone 
- Bypass git credential helper for public repo clone 
- Move git clone to workflow step, script only builds image 
- Use actions/checkout to clone Bausteinsicht repo 
- Drop container approach, run binary directly in CI 
- Install draw.io CLI and use xvfb-run for PNG export 
- SonarCloud Integration für Quality Monitoring (#47) (#48) (#48)
- Remove duplicate OUTPUT env for git-cliff, increase Pages smoke-test sleep to 30s 
- Replace fixed sleep with retry loop for Pages smoke-test (max 3min) 
- Git-cliff write to temp file then prepend to CHANGELOG.md 
- Copy bb_dashboard.html to index.html for GitHub Pages 
- Start_ticket zeigt automatisch Issue-Liste bei leerem Argument (#61) (#61)
- Automatisches PR-Review mit Bot-Token-Support in start_ticket (#64) (#64)
- ShellCheck SARIF Report für SonarCloud (#55) (#68) (#68)
- Deaktiviere C/C++ SonarCloud-Analyse + verbessertes Error Reporting (#70) (#70)
- POST /api/v1/backend wechselt jetzt tatsächlich den HAL-Backend (#72) (#72)
- Trend-Cache Git-Fallback via reports-Branch (#74) (#74)
- POST-Handler geben 400 bei ungültigem JSON zurück (#75) (#75)
- HTTP-Server mit ReadTimeout/WriteTimeout/IdleTimeout (Issue #21) (#77) (#77)
- Regression Test für BME280StreamHandler Flusher nil-Check (Issue #27) (#79) (#79)
- Flag.Parse() aus Library-Package entfernt (Issue #26) (#81) (#81)
- CORS OPTIONS Preflight-Requests behandeln (Issue #22) (#83) (#83)
- Collect_results.py + statisch/dynamisch Trennung (Issue #15) (#84) (#84)
- Phase 1 — Tooling in tooling/ Ordner gruppieren (Issue #85) (#86) (#86)
- Phase 3 — tooling/ aus Repo entfernen, via Release-Download (Issue #85) (#87) (#87)
- C Code Coverage CI-Integration (#88) (#88)
- Use download-tooling composite action 
- Use go-test composite action 
- Use shellcheck-sarif and c-test composite actions 
- Add explicit download-tooling step before go-test 
- Git worktree --orphan syntax für git 2.40+ 
- Use strictdoc and test-report composite actions 
- Use sonarcloud composite action 
- Remove download-tooling steps — scripts via GITHUB_ACTION_PATH 
- Add security-events:write for SARIF upload, bump to v1.1.9 
- Add strictdoc SARIF + requirements coverage, bump to v1.1.11 
- Alle SARIF- und Rust-Coverage-Pfade in sonar-project.properties ergänzen 
- SonarQube Issues Report in CI einbinden 
- Default case (*) in report.sh + tooling-Scan im CI (Issue #115) (#117) (#117)
- Download-tooling Step durch shellcheck-sarif include-tooling ersetzen 


# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Infrastruktur & Tooling

- Use container script instead of inline podman commands 
- Separate build step from run commands 
- Add export-diagram, export-table and export-png steps 
- Commit export changes back to repo if files changed 
- Update exported diagrams [skip ci] 
- Update exported diagrams [skip ci] 
- Trigger only on beaglebone_black.jsonc changes 
- Trigger SonarCloud verification 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Gruppierung nach Software-Änderungen und Infrastruktur & Tooling (#65) (#65)
- Erstelle PR statt direktem Push auf main (branch protection fix) (#66) (#66)
- Update unreleased section [skip ci] (#67) (#67)
- Update unreleased section [skip ci] (#69) (#69)
- Update unreleased section [skip ci] (#71) (#71)
- Update unreleased section [skip ci] (#73) (#73)
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] (#76) (#76)
- Add entry for Issue #31 fix (#75) [skip ci] 
- Update unreleased section [skip ci] (#78) (#78)
- Add entry for Issue #21 fix (#77) [skip ci] 
- Update unreleased section [skip ci] (#80) (#80)
- Add entry for Issue #27 fix (#79) [skip ci] 
- Update unreleased section [skip ci] (#82) (#82)
- Update unreleased section [skip ci] (#89) (#89)
- Beaglebone-tooling auf v1.1.0 aktualisieren (#90) (#90)
- Update unreleased section [skip ci] (#91) (#91)
- Bump beaglebone-tooling actions to v1.1.1 
- Update unreleased section [skip ci] (#92) (#92)
- Bump beaglebone-tooling actions to v1.1.2 
- Update unreleased section [skip ci] (#93) (#93)
- Update unreleased section [skip ci] (#94) (#94)
- Bump beaglebone-tooling actions to v1.1.3 
- Update unreleased section [skip ci] (#95) (#95)
- Bump beaglebone-tooling actions to v1.1.4 
- Update unreleased section [skip ci] (#96) (#96)
- Bump beaglebone-tooling actions to v1.1.5 
- Update unreleased section [skip ci] (#97) (#97)
- Bump beaglebone-tooling actions to v1.1.6 
- Update unreleased section [skip ci] (#98) (#98)
- Replace all inline steps with beaglebone-tooling composite actions @v1.1.7 
- Update unreleased section [skip ci] (#99) (#99)
- Bump beaglebone-tooling actions to v1.1.8 
- Update unreleased section [skip ci] (#100) (#100)
- Bump beaglebone-tooling actions to v1.1.10 (fix junit_to_sarif) 
- Update unreleased section [skip ci] (#102) (#102)
- Update unreleased section [skip ci] (#103) (#103)
- Bump beaglebone-tooling to v1.1.12 
- Update unreleased section [skip ci] (#104) (#104)
- Bump beaglebone-tooling to v1.1.13 
- Update unreleased section [skip ci] (#105) (#105)
- Update unreleased section [skip ci] (#106) (#106)
- Bump beaglebone-tooling to v1.1.14 (#107)
- Update unreleased section [skip ci] (#108) (#108)
- Update unreleased section [skip ci] (#109) (#109)
- Bump beaglebone-tooling to v1.1.15 (#110)
- Update unreleased section [skip ci] (#111) (#111)
- Bump beaglebone-tooling to v1.1.16 (#123)
- Update unreleased section [skip ci] (#124) (#124)
- Update unreleased section [skip ci] (#125) (#125)
- Download-tooling auf v1.1.16 aktualisieren (konsistent mit anderen Actions) 
- Update unreleased section [skip ci] (#126) (#126)
- Update unreleased section [skip ci] (#128) (#128)
- Bump beaglebone-tooling auf v1.1.17 (alle Actions konsistent) 

### Software-Änderungen

- Podman container script and CI workflow (#45) (#46) (#46)
- Mount model dir rw, fix export paths, add export dirs step 
- Disable git credential prompt for public repo clone 
- Bypass git credential helper for public repo clone 
- Move git clone to workflow step, script only builds image 
- Use actions/checkout to clone Bausteinsicht repo 
- Drop container approach, run binary directly in CI 
- Install draw.io CLI and use xvfb-run for PNG export 
- SonarCloud Integration für Quality Monitoring (#47) (#48) (#48)
- Remove duplicate OUTPUT env for git-cliff, increase Pages smoke-test sleep to 30s 
- Replace fixed sleep with retry loop for Pages smoke-test (max 3min) 
- Git-cliff write to temp file then prepend to CHANGELOG.md 
- Copy bb_dashboard.html to index.html for GitHub Pages 
- Start_ticket zeigt automatisch Issue-Liste bei leerem Argument (#61) (#61)
- Automatisches PR-Review mit Bot-Token-Support in start_ticket (#64) (#64)
- ShellCheck SARIF Report für SonarCloud (#55) (#68) (#68)
- Deaktiviere C/C++ SonarCloud-Analyse + verbessertes Error Reporting (#70) (#70)
- POST /api/v1/backend wechselt jetzt tatsächlich den HAL-Backend (#72) (#72)
- Trend-Cache Git-Fallback via reports-Branch (#74) (#74)
- POST-Handler geben 400 bei ungültigem JSON zurück (#75) (#75)
- HTTP-Server mit ReadTimeout/WriteTimeout/IdleTimeout (Issue #21) (#77) (#77)
- Regression Test für BME280StreamHandler Flusher nil-Check (Issue #27) (#79) (#79)
- Flag.Parse() aus Library-Package entfernt (Issue #26) (#81) (#81)
- CORS OPTIONS Preflight-Requests behandeln (Issue #22) (#83) (#83)
- Collect_results.py + statisch/dynamisch Trennung (Issue #15) (#84) (#84)
- Phase 1 — Tooling in tooling/ Ordner gruppieren (Issue #85) (#86) (#86)
- Phase 3 — tooling/ aus Repo entfernen, via Release-Download (Issue #85) (#87) (#87)
- C Code Coverage CI-Integration (#88) (#88)
- Use download-tooling composite action 
- Use go-test composite action 
- Use shellcheck-sarif and c-test composite actions 
- Add explicit download-tooling step before go-test 
- Git worktree --orphan syntax für git 2.40+ 
- Use strictdoc and test-report composite actions 
- Use sonarcloud composite action 
- Remove download-tooling steps — scripts via GITHUB_ACTION_PATH 
- Add security-events:write for SARIF upload, bump to v1.1.9 
- Add strictdoc SARIF + requirements coverage, bump to v1.1.11 
- Alle SARIF- und Rust-Coverage-Pfade in sonar-project.properties ergänzen 
- SonarQube Issues Report in CI einbinden 
- Default case (*) in report.sh + tooling-Scan im CI (Issue #115) (#117) (#117)
- Download-tooling Step durch shellcheck-sarif include-tooling ersetzen 


# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Infrastruktur & Tooling

- Use container script instead of inline podman commands 
- Separate build step from run commands 
- Add export-diagram, export-table and export-png steps 
- Commit export changes back to repo if files changed 
- Update exported diagrams [skip ci] 
- Update exported diagrams [skip ci] 
- Trigger only on beaglebone_black.jsonc changes 
- Trigger SonarCloud verification 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Gruppierung nach Software-Änderungen und Infrastruktur & Tooling (#65) (#65)
- Erstelle PR statt direktem Push auf main (branch protection fix) (#66) (#66)
- Update unreleased section [skip ci] (#67) (#67)
- Update unreleased section [skip ci] (#69) (#69)
- Update unreleased section [skip ci] (#71) (#71)
- Update unreleased section [skip ci] (#73) (#73)
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] (#76) (#76)
- Add entry for Issue #31 fix (#75) [skip ci] 
- Update unreleased section [skip ci] (#78) (#78)
- Add entry for Issue #21 fix (#77) [skip ci] 
- Update unreleased section [skip ci] (#80) (#80)
- Add entry for Issue #27 fix (#79) [skip ci] 
- Update unreleased section [skip ci] (#82) (#82)
- Update unreleased section [skip ci] (#89) (#89)
- Beaglebone-tooling auf v1.1.0 aktualisieren (#90) (#90)
- Update unreleased section [skip ci] (#91) (#91)
- Bump beaglebone-tooling actions to v1.1.1 
- Update unreleased section [skip ci] (#92) (#92)
- Bump beaglebone-tooling actions to v1.1.2 
- Update unreleased section [skip ci] (#93) (#93)
- Update unreleased section [skip ci] (#94) (#94)
- Bump beaglebone-tooling actions to v1.1.3 
- Update unreleased section [skip ci] (#95) (#95)
- Bump beaglebone-tooling actions to v1.1.4 
- Update unreleased section [skip ci] (#96) (#96)
- Bump beaglebone-tooling actions to v1.1.5 
- Update unreleased section [skip ci] (#97) (#97)
- Bump beaglebone-tooling actions to v1.1.6 
- Update unreleased section [skip ci] (#98) (#98)
- Replace all inline steps with beaglebone-tooling composite actions @v1.1.7 
- Update unreleased section [skip ci] (#99) (#99)
- Bump beaglebone-tooling actions to v1.1.8 
- Update unreleased section [skip ci] (#100) (#100)
- Bump beaglebone-tooling actions to v1.1.10 (fix junit_to_sarif) 
- Update unreleased section [skip ci] (#102) (#102)
- Update unreleased section [skip ci] (#103) (#103)
- Bump beaglebone-tooling to v1.1.12 
- Update unreleased section [skip ci] (#104) (#104)
- Bump beaglebone-tooling to v1.1.13 
- Update unreleased section [skip ci] (#105) (#105)
- Update unreleased section [skip ci] (#106) (#106)
- Bump beaglebone-tooling to v1.1.14 (#107)
- Update unreleased section [skip ci] (#108) (#108)
- Update unreleased section [skip ci] (#109) (#109)
- Bump beaglebone-tooling to v1.1.15 (#110)
- Update unreleased section [skip ci] (#111) (#111)
- Bump beaglebone-tooling to v1.1.16 (#123)
- Update unreleased section [skip ci] (#124) (#124)
- Update unreleased section [skip ci] (#125) (#125)
- Download-tooling auf v1.1.16 aktualisieren (konsistent mit anderen Actions) 
- Update unreleased section [skip ci] (#126) (#126)

### Software-Änderungen

- Podman container script and CI workflow (#45) (#46) (#46)
- Mount model dir rw, fix export paths, add export dirs step 
- Disable git credential prompt for public repo clone 
- Bypass git credential helper for public repo clone 
- Move git clone to workflow step, script only builds image 
- Use actions/checkout to clone Bausteinsicht repo 
- Drop container approach, run binary directly in CI 
- Install draw.io CLI and use xvfb-run for PNG export 
- SonarCloud Integration für Quality Monitoring (#47) (#48) (#48)
- Remove duplicate OUTPUT env for git-cliff, increase Pages smoke-test sleep to 30s 
- Replace fixed sleep with retry loop for Pages smoke-test (max 3min) 
- Git-cliff write to temp file then prepend to CHANGELOG.md 
- Copy bb_dashboard.html to index.html for GitHub Pages 
- Start_ticket zeigt automatisch Issue-Liste bei leerem Argument (#61) (#61)
- Automatisches PR-Review mit Bot-Token-Support in start_ticket (#64) (#64)
- ShellCheck SARIF Report für SonarCloud (#55) (#68) (#68)
- Deaktiviere C/C++ SonarCloud-Analyse + verbessertes Error Reporting (#70) (#70)
- POST /api/v1/backend wechselt jetzt tatsächlich den HAL-Backend (#72) (#72)
- Trend-Cache Git-Fallback via reports-Branch (#74) (#74)
- POST-Handler geben 400 bei ungültigem JSON zurück (#75) (#75)
- HTTP-Server mit ReadTimeout/WriteTimeout/IdleTimeout (Issue #21) (#77) (#77)
- Regression Test für BME280StreamHandler Flusher nil-Check (Issue #27) (#79) (#79)
- Flag.Parse() aus Library-Package entfernt (Issue #26) (#81) (#81)
- CORS OPTIONS Preflight-Requests behandeln (Issue #22) (#83) (#83)
- Collect_results.py + statisch/dynamisch Trennung (Issue #15) (#84) (#84)
- Phase 1 — Tooling in tooling/ Ordner gruppieren (Issue #85) (#86) (#86)
- Phase 3 — tooling/ aus Repo entfernen, via Release-Download (Issue #85) (#87) (#87)
- C Code Coverage CI-Integration (#88) (#88)
- Use download-tooling composite action 
- Use go-test composite action 
- Use shellcheck-sarif and c-test composite actions 
- Add explicit download-tooling step before go-test 
- Git worktree --orphan syntax für git 2.40+ 
- Use strictdoc and test-report composite actions 
- Use sonarcloud composite action 
- Remove download-tooling steps — scripts via GITHUB_ACTION_PATH 
- Add security-events:write for SARIF upload, bump to v1.1.9 
- Add strictdoc SARIF + requirements coverage, bump to v1.1.11 
- Alle SARIF- und Rust-Coverage-Pfade in sonar-project.properties ergänzen 
- SonarQube Issues Report in CI einbinden 
- Default case (*) in report.sh + tooling-Scan im CI (Issue #115) (#117) (#117)
- Download-tooling Step durch shellcheck-sarif include-tooling ersetzen 


# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Infrastruktur & Tooling

- Use container script instead of inline podman commands 
- Separate build step from run commands 
- Add export-diagram, export-table and export-png steps 
- Commit export changes back to repo if files changed 
- Update exported diagrams [skip ci] 
- Update exported diagrams [skip ci] 
- Trigger only on beaglebone_black.jsonc changes 
- Trigger SonarCloud verification 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Gruppierung nach Software-Änderungen und Infrastruktur & Tooling (#65) (#65)
- Erstelle PR statt direktem Push auf main (branch protection fix) (#66) (#66)
- Update unreleased section [skip ci] (#67) (#67)
- Update unreleased section [skip ci] (#69) (#69)
- Update unreleased section [skip ci] (#71) (#71)
- Update unreleased section [skip ci] (#73) (#73)
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] (#76) (#76)
- Add entry for Issue #31 fix (#75) [skip ci] 
- Update unreleased section [skip ci] (#78) (#78)
- Add entry for Issue #21 fix (#77) [skip ci] 
- Update unreleased section [skip ci] (#80) (#80)
- Add entry for Issue #27 fix (#79) [skip ci] 
- Update unreleased section [skip ci] (#82) (#82)
- Update unreleased section [skip ci] (#89) (#89)
- Beaglebone-tooling auf v1.1.0 aktualisieren (#90) (#90)
- Update unreleased section [skip ci] (#91) (#91)
- Bump beaglebone-tooling actions to v1.1.1 
- Update unreleased section [skip ci] (#92) (#92)
- Bump beaglebone-tooling actions to v1.1.2 
- Update unreleased section [skip ci] (#93) (#93)
- Update unreleased section [skip ci] (#94) (#94)
- Bump beaglebone-tooling actions to v1.1.3 
- Update unreleased section [skip ci] (#95) (#95)
- Bump beaglebone-tooling actions to v1.1.4 
- Update unreleased section [skip ci] (#96) (#96)
- Bump beaglebone-tooling actions to v1.1.5 
- Update unreleased section [skip ci] (#97) (#97)
- Bump beaglebone-tooling actions to v1.1.6 
- Update unreleased section [skip ci] (#98) (#98)
- Replace all inline steps with beaglebone-tooling composite actions @v1.1.7 
- Update unreleased section [skip ci] (#99) (#99)
- Bump beaglebone-tooling actions to v1.1.8 
- Update unreleased section [skip ci] (#100) (#100)
- Bump beaglebone-tooling actions to v1.1.10 (fix junit_to_sarif) 
- Update unreleased section [skip ci] (#102) (#102)
- Update unreleased section [skip ci] (#103) (#103)
- Bump beaglebone-tooling to v1.1.12 
- Update unreleased section [skip ci] (#104) (#104)
- Bump beaglebone-tooling to v1.1.13 
- Update unreleased section [skip ci] (#105) (#105)
- Update unreleased section [skip ci] (#106) (#106)
- Bump beaglebone-tooling to v1.1.14 (#107)
- Update unreleased section [skip ci] (#108) (#108)
- Update unreleased section [skip ci] (#109) (#109)
- Bump beaglebone-tooling to v1.1.15 (#110)
- Update unreleased section [skip ci] (#111) (#111)
- Bump beaglebone-tooling to v1.1.16 (#123)
- Update unreleased section [skip ci] (#124) (#124)
- Update unreleased section [skip ci] (#125) (#125)
- Download-tooling auf v1.1.16 aktualisieren (konsistent mit anderen Actions) 

### Software-Änderungen

- Podman container script and CI workflow (#45) (#46) (#46)
- Mount model dir rw, fix export paths, add export dirs step 
- Disable git credential prompt for public repo clone 
- Bypass git credential helper for public repo clone 
- Move git clone to workflow step, script only builds image 
- Use actions/checkout to clone Bausteinsicht repo 
- Drop container approach, run binary directly in CI 
- Install draw.io CLI and use xvfb-run for PNG export 
- SonarCloud Integration für Quality Monitoring (#47) (#48) (#48)
- Remove duplicate OUTPUT env for git-cliff, increase Pages smoke-test sleep to 30s 
- Replace fixed sleep with retry loop for Pages smoke-test (max 3min) 
- Git-cliff write to temp file then prepend to CHANGELOG.md 
- Copy bb_dashboard.html to index.html for GitHub Pages 
- Start_ticket zeigt automatisch Issue-Liste bei leerem Argument (#61) (#61)
- Automatisches PR-Review mit Bot-Token-Support in start_ticket (#64) (#64)
- ShellCheck SARIF Report für SonarCloud (#55) (#68) (#68)
- Deaktiviere C/C++ SonarCloud-Analyse + verbessertes Error Reporting (#70) (#70)
- POST /api/v1/backend wechselt jetzt tatsächlich den HAL-Backend (#72) (#72)
- Trend-Cache Git-Fallback via reports-Branch (#74) (#74)
- POST-Handler geben 400 bei ungültigem JSON zurück (#75) (#75)
- HTTP-Server mit ReadTimeout/WriteTimeout/IdleTimeout (Issue #21) (#77) (#77)
- Regression Test für BME280StreamHandler Flusher nil-Check (Issue #27) (#79) (#79)
- Flag.Parse() aus Library-Package entfernt (Issue #26) (#81) (#81)
- CORS OPTIONS Preflight-Requests behandeln (Issue #22) (#83) (#83)
- Collect_results.py + statisch/dynamisch Trennung (Issue #15) (#84) (#84)
- Phase 1 — Tooling in tooling/ Ordner gruppieren (Issue #85) (#86) (#86)
- Phase 3 — tooling/ aus Repo entfernen, via Release-Download (Issue #85) (#87) (#87)
- C Code Coverage CI-Integration (#88) (#88)
- Use download-tooling composite action 
- Use go-test composite action 
- Use shellcheck-sarif and c-test composite actions 
- Add explicit download-tooling step before go-test 
- Git worktree --orphan syntax für git 2.40+ 
- Use strictdoc and test-report composite actions 
- Use sonarcloud composite action 
- Remove download-tooling steps — scripts via GITHUB_ACTION_PATH 
- Add security-events:write for SARIF upload, bump to v1.1.9 
- Add strictdoc SARIF + requirements coverage, bump to v1.1.11 
- Alle SARIF- und Rust-Coverage-Pfade in sonar-project.properties ergänzen 
- SonarQube Issues Report in CI einbinden 
- Default case (*) in report.sh + tooling-Scan im CI (Issue #115) (#117) (#117)


# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Infrastruktur & Tooling

- Use container script instead of inline podman commands 
- Separate build step from run commands 
- Add export-diagram, export-table and export-png steps 
- Commit export changes back to repo if files changed 
- Update exported diagrams [skip ci] 
- Update exported diagrams [skip ci] 
- Trigger only on beaglebone_black.jsonc changes 
- Trigger SonarCloud verification 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Gruppierung nach Software-Änderungen und Infrastruktur & Tooling (#65) (#65)
- Erstelle PR statt direktem Push auf main (branch protection fix) (#66) (#66)
- Update unreleased section [skip ci] (#67) (#67)
- Update unreleased section [skip ci] (#69) (#69)
- Update unreleased section [skip ci] (#71) (#71)
- Update unreleased section [skip ci] (#73) (#73)
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] (#76) (#76)
- Add entry for Issue #31 fix (#75) [skip ci] 
- Update unreleased section [skip ci] (#78) (#78)
- Add entry for Issue #21 fix (#77) [skip ci] 
- Update unreleased section [skip ci] (#80) (#80)
- Add entry for Issue #27 fix (#79) [skip ci] 
- Update unreleased section [skip ci] (#82) (#82)
- Update unreleased section [skip ci] (#89) (#89)
- Beaglebone-tooling auf v1.1.0 aktualisieren (#90) (#90)
- Update unreleased section [skip ci] (#91) (#91)
- Bump beaglebone-tooling actions to v1.1.1 
- Update unreleased section [skip ci] (#92) (#92)
- Bump beaglebone-tooling actions to v1.1.2 
- Update unreleased section [skip ci] (#93) (#93)
- Update unreleased section [skip ci] (#94) (#94)
- Bump beaglebone-tooling actions to v1.1.3 
- Update unreleased section [skip ci] (#95) (#95)
- Bump beaglebone-tooling actions to v1.1.4 
- Update unreleased section [skip ci] (#96) (#96)
- Bump beaglebone-tooling actions to v1.1.5 
- Update unreleased section [skip ci] (#97) (#97)
- Bump beaglebone-tooling actions to v1.1.6 
- Update unreleased section [skip ci] (#98) (#98)
- Replace all inline steps with beaglebone-tooling composite actions @v1.1.7 
- Update unreleased section [skip ci] (#99) (#99)
- Bump beaglebone-tooling actions to v1.1.8 
- Update unreleased section [skip ci] (#100) (#100)
- Bump beaglebone-tooling actions to v1.1.10 (fix junit_to_sarif) 
- Update unreleased section [skip ci] (#102) (#102)
- Update unreleased section [skip ci] (#103) (#103)
- Bump beaglebone-tooling to v1.1.12 
- Update unreleased section [skip ci] (#104) (#104)
- Bump beaglebone-tooling to v1.1.13 
- Update unreleased section [skip ci] (#105) (#105)
- Update unreleased section [skip ci] (#106) (#106)
- Bump beaglebone-tooling to v1.1.14 (#107)
- Update unreleased section [skip ci] (#108) (#108)
- Update unreleased section [skip ci] (#109) (#109)
- Bump beaglebone-tooling to v1.1.15 (#110)
- Update unreleased section [skip ci] (#111) (#111)
- Bump beaglebone-tooling to v1.1.16 (#123)
- Update unreleased section [skip ci] (#124) (#124)

### Software-Änderungen

- Podman container script and CI workflow (#45) (#46) (#46)
- Mount model dir rw, fix export paths, add export dirs step 
- Disable git credential prompt for public repo clone 
- Bypass git credential helper for public repo clone 
- Move git clone to workflow step, script only builds image 
- Use actions/checkout to clone Bausteinsicht repo 
- Drop container approach, run binary directly in CI 
- Install draw.io CLI and use xvfb-run for PNG export 
- SonarCloud Integration für Quality Monitoring (#47) (#48) (#48)
- Remove duplicate OUTPUT env for git-cliff, increase Pages smoke-test sleep to 30s 
- Replace fixed sleep with retry loop for Pages smoke-test (max 3min) 
- Git-cliff write to temp file then prepend to CHANGELOG.md 
- Copy bb_dashboard.html to index.html for GitHub Pages 
- Start_ticket zeigt automatisch Issue-Liste bei leerem Argument (#61) (#61)
- Automatisches PR-Review mit Bot-Token-Support in start_ticket (#64) (#64)
- ShellCheck SARIF Report für SonarCloud (#55) (#68) (#68)
- Deaktiviere C/C++ SonarCloud-Analyse + verbessertes Error Reporting (#70) (#70)
- POST /api/v1/backend wechselt jetzt tatsächlich den HAL-Backend (#72) (#72)
- Trend-Cache Git-Fallback via reports-Branch (#74) (#74)
- POST-Handler geben 400 bei ungültigem JSON zurück (#75) (#75)
- HTTP-Server mit ReadTimeout/WriteTimeout/IdleTimeout (Issue #21) (#77) (#77)
- Regression Test für BME280StreamHandler Flusher nil-Check (Issue #27) (#79) (#79)
- Flag.Parse() aus Library-Package entfernt (Issue #26) (#81) (#81)
- CORS OPTIONS Preflight-Requests behandeln (Issue #22) (#83) (#83)
- Collect_results.py + statisch/dynamisch Trennung (Issue #15) (#84) (#84)
- Phase 1 — Tooling in tooling/ Ordner gruppieren (Issue #85) (#86) (#86)
- Phase 3 — tooling/ aus Repo entfernen, via Release-Download (Issue #85) (#87) (#87)
- C Code Coverage CI-Integration (#88) (#88)
- Use download-tooling composite action 
- Use go-test composite action 
- Use shellcheck-sarif and c-test composite actions 
- Add explicit download-tooling step before go-test 
- Git worktree --orphan syntax für git 2.40+ 
- Use strictdoc and test-report composite actions 
- Use sonarcloud composite action 
- Remove download-tooling steps — scripts via GITHUB_ACTION_PATH 
- Add security-events:write for SARIF upload, bump to v1.1.9 
- Add strictdoc SARIF + requirements coverage, bump to v1.1.11 
- Alle SARIF- und Rust-Coverage-Pfade in sonar-project.properties ergänzen 
- SonarQube Issues Report in CI einbinden 
- Default case (*) in report.sh + tooling-Scan im CI (Issue #115) (#117) (#117)


# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixes

- fix(shell): `*)` Default-Case in `report.sh` (SonarQube S131 CRITICAL) — beaglebone-tooling v1.1.16 ([#115](https://github.com/paulefl/beaglebone_black/issues/115))
- fix(ci): `download-tooling` vor `shellcheck-sarif` in `test-scripts`-Job, damit `tooling/report.sh` gescannt wird ([#115](https://github.com/paulefl/beaglebone_black/issues/115))


### Infrastruktur & Tooling

- Use container script instead of inline podman commands 
- Separate build step from run commands 
- Add export-diagram, export-table and export-png steps 
- Commit export changes back to repo if files changed 
- Update exported diagrams [skip ci] 
- Update exported diagrams [skip ci] 
- Trigger only on beaglebone_black.jsonc changes 
- Trigger SonarCloud verification 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Gruppierung nach Software-Änderungen und Infrastruktur & Tooling (#65) (#65)
- Erstelle PR statt direktem Push auf main (branch protection fix) (#66) (#66)
- Update unreleased section [skip ci] (#67) (#67)
- Update unreleased section [skip ci] (#69) (#69)
- Update unreleased section [skip ci] (#71) (#71)
- Update unreleased section [skip ci] (#73) (#73)
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] (#76) (#76)
- Add entry for Issue #31 fix (#75) [skip ci] 
- Update unreleased section [skip ci] (#78) (#78)
- Add entry for Issue #21 fix (#77) [skip ci] 
- Update unreleased section [skip ci] (#80) (#80)
- Add entry for Issue #27 fix (#79) [skip ci] 
- Update unreleased section [skip ci] (#82) (#82)
- Update unreleased section [skip ci] (#89) (#89)
- Beaglebone-tooling auf v1.1.0 aktualisieren (#90) (#90)
- Update unreleased section [skip ci] (#91) (#91)
- Bump beaglebone-tooling actions to v1.1.1 
- Update unreleased section [skip ci] (#92) (#92)
- Bump beaglebone-tooling actions to v1.1.2 
- Update unreleased section [skip ci] (#93) (#93)
- Update unreleased section [skip ci] (#94) (#94)
- Bump beaglebone-tooling actions to v1.1.3 
- Update unreleased section [skip ci] (#95) (#95)
- Bump beaglebone-tooling actions to v1.1.4 
- Update unreleased section [skip ci] (#96) (#96)
- Bump beaglebone-tooling actions to v1.1.5 
- Update unreleased section [skip ci] (#97) (#97)
- Bump beaglebone-tooling actions to v1.1.6 
- Update unreleased section [skip ci] (#98) (#98)
- Replace all inline steps with beaglebone-tooling composite actions @v1.1.7 
- Update unreleased section [skip ci] (#99) (#99)
- Bump beaglebone-tooling actions to v1.1.8 
- Update unreleased section [skip ci] (#100) (#100)
- Bump beaglebone-tooling actions to v1.1.10 (fix junit_to_sarif) 
- Update unreleased section [skip ci] (#102) (#102)
- Update unreleased section [skip ci] (#103) (#103)
- Bump beaglebone-tooling to v1.1.12 
- Update unreleased section [skip ci] (#104) (#104)
- Bump beaglebone-tooling to v1.1.13 
- Update unreleased section [skip ci] (#105) (#105)
- Update unreleased section [skip ci] (#106) (#106)
- Bump beaglebone-tooling to v1.1.14 (#107)
- Update unreleased section [skip ci] (#108) (#108)
- Update unreleased section [skip ci] (#109) (#109)
- Bump beaglebone-tooling to v1.1.15 (#110)
- Update unreleased section [skip ci] (#111) (#111)
- Bump beaglebone-tooling to v1.1.16 (#123)

### Software-Änderungen

- Podman container script and CI workflow (#45) (#46) (#46)
- Mount model dir rw, fix export paths, add export dirs step 
- Disable git credential prompt for public repo clone 
- Bypass git credential helper for public repo clone 
- Move git clone to workflow step, script only builds image 
- Use actions/checkout to clone Bausteinsicht repo 
- Drop container approach, run binary directly in CI 
- Install draw.io CLI and use xvfb-run for PNG export 
- SonarCloud Integration für Quality Monitoring (#47) (#48) (#48)
- Remove duplicate OUTPUT env for git-cliff, increase Pages smoke-test sleep to 30s 
- Replace fixed sleep with retry loop for Pages smoke-test (max 3min) 
- Git-cliff write to temp file then prepend to CHANGELOG.md 
- Copy bb_dashboard.html to index.html for GitHub Pages 
- Start_ticket zeigt automatisch Issue-Liste bei leerem Argument (#61) (#61)
- Automatisches PR-Review mit Bot-Token-Support in start_ticket (#64) (#64)
- ShellCheck SARIF Report für SonarCloud (#55) (#68) (#68)
- Deaktiviere C/C++ SonarCloud-Analyse + verbessertes Error Reporting (#70) (#70)
- POST /api/v1/backend wechselt jetzt tatsächlich den HAL-Backend (#72) (#72)
- Trend-Cache Git-Fallback via reports-Branch (#74) (#74)
- POST-Handler geben 400 bei ungültigem JSON zurück (#75) (#75)
- HTTP-Server mit ReadTimeout/WriteTimeout/IdleTimeout (Issue #21) (#77) (#77)
- Regression Test für BME280StreamHandler Flusher nil-Check (Issue #27) (#79) (#79)
- Flag.Parse() aus Library-Package entfernt (Issue #26) (#81) (#81)
- CORS OPTIONS Preflight-Requests behandeln (Issue #22) (#83) (#83)
- Collect_results.py + statisch/dynamisch Trennung (Issue #15) (#84) (#84)
- Phase 1 — Tooling in tooling/ Ordner gruppieren (Issue #85) (#86) (#86)
- Phase 3 — tooling/ aus Repo entfernen, via Release-Download (Issue #85) (#87) (#87)
- C Code Coverage CI-Integration (#88) (#88)
- Use download-tooling composite action 
- Use go-test composite action 
- Use shellcheck-sarif and c-test composite actions 
- Add explicit download-tooling step before go-test 
- Git worktree --orphan syntax für git 2.40+ 
- Use strictdoc and test-report composite actions 
- Use sonarcloud composite action 
- Remove download-tooling steps — scripts via GITHUB_ACTION_PATH 
- Add security-events:write for SARIF upload, bump to v1.1.9 
- Add strictdoc SARIF + requirements coverage, bump to v1.1.11 
- Alle SARIF- und Rust-Coverage-Pfade in sonar-project.properties ergänzen 
- SonarQube Issues Report in CI einbinden 


# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Infrastruktur & Tooling

- Use container script instead of inline podman commands 
- Separate build step from run commands 
- Add export-diagram, export-table and export-png steps 
- Commit export changes back to repo if files changed 
- Update exported diagrams [skip ci] 
- Update exported diagrams [skip ci] 
- Trigger only on beaglebone_black.jsonc changes 
- Trigger SonarCloud verification 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Gruppierung nach Software-Änderungen und Infrastruktur & Tooling (#65) (#65)
- Erstelle PR statt direktem Push auf main (branch protection fix) (#66) (#66)
- Update unreleased section [skip ci] (#67) (#67)
- Update unreleased section [skip ci] (#69) (#69)
- Update unreleased section [skip ci] (#71) (#71)
- Update unreleased section [skip ci] (#73) (#73)
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] (#76) (#76)
- Add entry for Issue #31 fix (#75) [skip ci] 
- Update unreleased section [skip ci] (#78) (#78)
- Add entry for Issue #21 fix (#77) [skip ci] 
- Update unreleased section [skip ci] (#80) (#80)
- Add entry for Issue #27 fix (#79) [skip ci] 
- Update unreleased section [skip ci] (#82) (#82)
- Update unreleased section [skip ci] (#89) (#89)
- Beaglebone-tooling auf v1.1.0 aktualisieren (#90) (#90)
- Update unreleased section [skip ci] (#91) (#91)
- Bump beaglebone-tooling actions to v1.1.1 
- Update unreleased section [skip ci] (#92) (#92)
- Bump beaglebone-tooling actions to v1.1.2 
- Update unreleased section [skip ci] (#93) (#93)
- Update unreleased section [skip ci] (#94) (#94)
- Bump beaglebone-tooling actions to v1.1.3 
- Update unreleased section [skip ci] (#95) (#95)
- Bump beaglebone-tooling actions to v1.1.4 
- Update unreleased section [skip ci] (#96) (#96)
- Bump beaglebone-tooling actions to v1.1.5 
- Update unreleased section [skip ci] (#97) (#97)
- Bump beaglebone-tooling actions to v1.1.6 
- Update unreleased section [skip ci] (#98) (#98)
- Replace all inline steps with beaglebone-tooling composite actions @v1.1.7 
- Update unreleased section [skip ci] (#99) (#99)
- Bump beaglebone-tooling actions to v1.1.8 
- Update unreleased section [skip ci] (#100) (#100)
- Bump beaglebone-tooling actions to v1.1.10 (fix junit_to_sarif) 
- Update unreleased section [skip ci] (#102) (#102)
- Update unreleased section [skip ci] (#103) (#103)
- Bump beaglebone-tooling to v1.1.12 
- Update unreleased section [skip ci] (#104) (#104)
- Bump beaglebone-tooling to v1.1.13 
- Update unreleased section [skip ci] (#105) (#105)
- Update unreleased section [skip ci] (#106) (#106)
- Bump beaglebone-tooling to v1.1.14 (#107)
- Update unreleased section [skip ci] (#108) (#108)
- Update unreleased section [skip ci] (#109) (#109)
- Bump beaglebone-tooling to v1.1.15 (#110)

### Software-Änderungen

- Podman container script and CI workflow (#45) (#46) (#46)
- Mount model dir rw, fix export paths, add export dirs step 
- Disable git credential prompt for public repo clone 
- Bypass git credential helper for public repo clone 
- Move git clone to workflow step, script only builds image 
- Use actions/checkout to clone Bausteinsicht repo 
- Drop container approach, run binary directly in CI 
- Install draw.io CLI and use xvfb-run for PNG export 
- SonarCloud Integration für Quality Monitoring (#47) (#48) (#48)
- Remove duplicate OUTPUT env for git-cliff, increase Pages smoke-test sleep to 30s 
- Replace fixed sleep with retry loop for Pages smoke-test (max 3min) 
- Git-cliff write to temp file then prepend to CHANGELOG.md 
- Copy bb_dashboard.html to index.html for GitHub Pages 
- Start_ticket zeigt automatisch Issue-Liste bei leerem Argument (#61) (#61)
- Automatisches PR-Review mit Bot-Token-Support in start_ticket (#64) (#64)
- ShellCheck SARIF Report für SonarCloud (#55) (#68) (#68)
- Deaktiviere C/C++ SonarCloud-Analyse + verbessertes Error Reporting (#70) (#70)
- POST /api/v1/backend wechselt jetzt tatsächlich den HAL-Backend (#72) (#72)
- Trend-Cache Git-Fallback via reports-Branch (#74) (#74)
- POST-Handler geben 400 bei ungültigem JSON zurück (#75) (#75)
- HTTP-Server mit ReadTimeout/WriteTimeout/IdleTimeout (Issue #21) (#77) (#77)
- Regression Test für BME280StreamHandler Flusher nil-Check (Issue #27) (#79) (#79)
- Flag.Parse() aus Library-Package entfernt (Issue #26) (#81) (#81)
- CORS OPTIONS Preflight-Requests behandeln (Issue #22) (#83) (#83)
- Collect_results.py + statisch/dynamisch Trennung (Issue #15) (#84) (#84)
- Phase 1 — Tooling in tooling/ Ordner gruppieren (Issue #85) (#86) (#86)
- Phase 3 — tooling/ aus Repo entfernen, via Release-Download (Issue #85) (#87) (#87)
- C Code Coverage CI-Integration (#88) (#88)
- Use download-tooling composite action 
- Use go-test composite action 
- Use shellcheck-sarif and c-test composite actions 
- Add explicit download-tooling step before go-test 
- Git worktree --orphan syntax für git 2.40+ 
- Use strictdoc and test-report composite actions 
- Use sonarcloud composite action 
- Remove download-tooling steps — scripts via GITHUB_ACTION_PATH 
- Add security-events:write for SARIF upload, bump to v1.1.9 
- Add strictdoc SARIF + requirements coverage, bump to v1.1.11 
- Alle SARIF- und Rust-Coverage-Pfade in sonar-project.properties ergänzen 
- SonarQube Issues Report in CI einbinden 


# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Infrastruktur & Tooling

- Use container script instead of inline podman commands 
- Separate build step from run commands 
- Add export-diagram, export-table and export-png steps 
- Commit export changes back to repo if files changed 
- Update exported diagrams [skip ci] 
- Update exported diagrams [skip ci] 
- Trigger only on beaglebone_black.jsonc changes 
- Trigger SonarCloud verification 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Gruppierung nach Software-Änderungen und Infrastruktur & Tooling (#65) (#65)
- Erstelle PR statt direktem Push auf main (branch protection fix) (#66) (#66)
- Update unreleased section [skip ci] (#67) (#67)
- Update unreleased section [skip ci] (#69) (#69)
- Update unreleased section [skip ci] (#71) (#71)
- Update unreleased section [skip ci] (#73) (#73)
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] (#76) (#76)
- Add entry for Issue #31 fix (#75) [skip ci] 
- Update unreleased section [skip ci] (#78) (#78)
- Add entry for Issue #21 fix (#77) [skip ci] 
- Update unreleased section [skip ci] (#80) (#80)
- Add entry for Issue #27 fix (#79) [skip ci] 
- Update unreleased section [skip ci] (#82) (#82)
- Update unreleased section [skip ci] (#89) (#89)
- Beaglebone-tooling auf v1.1.0 aktualisieren (#90) (#90)
- Update unreleased section [skip ci] (#91) (#91)
- Bump beaglebone-tooling actions to v1.1.1 
- Update unreleased section [skip ci] (#92) (#92)
- Bump beaglebone-tooling actions to v1.1.2 
- Update unreleased section [skip ci] (#93) (#93)
- Update unreleased section [skip ci] (#94) (#94)
- Bump beaglebone-tooling actions to v1.1.3 
- Update unreleased section [skip ci] (#95) (#95)
- Bump beaglebone-tooling actions to v1.1.4 
- Update unreleased section [skip ci] (#96) (#96)
- Bump beaglebone-tooling actions to v1.1.5 
- Update unreleased section [skip ci] (#97) (#97)
- Bump beaglebone-tooling actions to v1.1.6 
- Update unreleased section [skip ci] (#98) (#98)
- Replace all inline steps with beaglebone-tooling composite actions @v1.1.7 
- Update unreleased section [skip ci] (#99) (#99)
- Bump beaglebone-tooling actions to v1.1.8 
- Update unreleased section [skip ci] (#100) (#100)
- Bump beaglebone-tooling actions to v1.1.10 (fix junit_to_sarif) 
- Update unreleased section [skip ci] (#102) (#102)
- Update unreleased section [skip ci] (#103) (#103)
- Bump beaglebone-tooling to v1.1.12 
- Update unreleased section [skip ci] (#104) (#104)
- Bump beaglebone-tooling to v1.1.13 
- Update unreleased section [skip ci] (#105) (#105)
- Update unreleased section [skip ci] (#106) (#106)
- Bump beaglebone-tooling to v1.1.14 (#107)
- Update unreleased section [skip ci] (#108) (#108)

### Software-Änderungen

- Podman container script and CI workflow (#45) (#46) (#46)
- Mount model dir rw, fix export paths, add export dirs step 
- Disable git credential prompt for public repo clone 
- Bypass git credential helper for public repo clone 
- Move git clone to workflow step, script only builds image 
- Use actions/checkout to clone Bausteinsicht repo 
- Drop container approach, run binary directly in CI 
- Install draw.io CLI and use xvfb-run for PNG export 
- SonarCloud Integration für Quality Monitoring (#47) (#48) (#48)
- Remove duplicate OUTPUT env for git-cliff, increase Pages smoke-test sleep to 30s 
- Replace fixed sleep with retry loop for Pages smoke-test (max 3min) 
- Git-cliff write to temp file then prepend to CHANGELOG.md 
- Copy bb_dashboard.html to index.html for GitHub Pages 
- Start_ticket zeigt automatisch Issue-Liste bei leerem Argument (#61) (#61)
- Automatisches PR-Review mit Bot-Token-Support in start_ticket (#64) (#64)
- ShellCheck SARIF Report für SonarCloud (#55) (#68) (#68)
- Deaktiviere C/C++ SonarCloud-Analyse + verbessertes Error Reporting (#70) (#70)
- POST /api/v1/backend wechselt jetzt tatsächlich den HAL-Backend (#72) (#72)
- Trend-Cache Git-Fallback via reports-Branch (#74) (#74)
- POST-Handler geben 400 bei ungültigem JSON zurück (#75) (#75)
- HTTP-Server mit ReadTimeout/WriteTimeout/IdleTimeout (Issue #21) (#77) (#77)
- Regression Test für BME280StreamHandler Flusher nil-Check (Issue #27) (#79) (#79)
- Flag.Parse() aus Library-Package entfernt (Issue #26) (#81) (#81)
- CORS OPTIONS Preflight-Requests behandeln (Issue #22) (#83) (#83)
- Collect_results.py + statisch/dynamisch Trennung (Issue #15) (#84) (#84)
- Phase 1 — Tooling in tooling/ Ordner gruppieren (Issue #85) (#86) (#86)
- Phase 3 — tooling/ aus Repo entfernen, via Release-Download (Issue #85) (#87) (#87)
- C Code Coverage CI-Integration (#88) (#88)
- Use download-tooling composite action 
- Use go-test composite action 
- Use shellcheck-sarif and c-test composite actions 
- Add explicit download-tooling step before go-test 
- Git worktree --orphan syntax für git 2.40+ 
- Use strictdoc and test-report composite actions 
- Use sonarcloud composite action 
- Remove download-tooling steps — scripts via GITHUB_ACTION_PATH 
- Add security-events:write for SARIF upload, bump to v1.1.9 
- Add strictdoc SARIF + requirements coverage, bump to v1.1.11 
- Alle SARIF- und Rust-Coverage-Pfade in sonar-project.properties ergänzen 
- SonarQube Issues Report in CI einbinden 


# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Infrastruktur & Tooling

- Use container script instead of inline podman commands 
- Separate build step from run commands 
- Add export-diagram, export-table and export-png steps 
- Commit export changes back to repo if files changed 
- Update exported diagrams [skip ci] 
- Update exported diagrams [skip ci] 
- Trigger only on beaglebone_black.jsonc changes 
- Trigger SonarCloud verification 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Gruppierung nach Software-Änderungen und Infrastruktur & Tooling (#65) (#65)
- Erstelle PR statt direktem Push auf main (branch protection fix) (#66) (#66)
- Update unreleased section [skip ci] (#67) (#67)
- Update unreleased section [skip ci] (#69) (#69)
- Update unreleased section [skip ci] (#71) (#71)
- Update unreleased section [skip ci] (#73) (#73)
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] (#76) (#76)
- Add entry for Issue #31 fix (#75) [skip ci] 
- Update unreleased section [skip ci] (#78) (#78)
- Add entry for Issue #21 fix (#77) [skip ci] 
- Update unreleased section [skip ci] (#80) (#80)
- Add entry for Issue #27 fix (#79) [skip ci] 
- Update unreleased section [skip ci] (#82) (#82)
- Update unreleased section [skip ci] (#89) (#89)
- Beaglebone-tooling auf v1.1.0 aktualisieren (#90) (#90)
- Update unreleased section [skip ci] (#91) (#91)
- Bump beaglebone-tooling actions to v1.1.1 
- Update unreleased section [skip ci] (#92) (#92)
- Bump beaglebone-tooling actions to v1.1.2 
- Update unreleased section [skip ci] (#93) (#93)
- Update unreleased section [skip ci] (#94) (#94)
- Bump beaglebone-tooling actions to v1.1.3 
- Update unreleased section [skip ci] (#95) (#95)
- Bump beaglebone-tooling actions to v1.1.4 
- Update unreleased section [skip ci] (#96) (#96)
- Bump beaglebone-tooling actions to v1.1.5 
- Update unreleased section [skip ci] (#97) (#97)
- Bump beaglebone-tooling actions to v1.1.6 
- Update unreleased section [skip ci] (#98) (#98)
- Replace all inline steps with beaglebone-tooling composite actions @v1.1.7 
- Update unreleased section [skip ci] (#99) (#99)
- Bump beaglebone-tooling actions to v1.1.8 
- Update unreleased section [skip ci] (#100) (#100)
- Bump beaglebone-tooling actions to v1.1.10 (fix junit_to_sarif) 
- Update unreleased section [skip ci] (#102) (#102)
- Update unreleased section [skip ci] (#103) (#103)
- Bump beaglebone-tooling to v1.1.12 
- Update unreleased section [skip ci] (#104) (#104)
- Bump beaglebone-tooling to v1.1.13 
- Update unreleased section [skip ci] (#105) (#105)
- Update unreleased section [skip ci] (#106) (#106)
- Bump beaglebone-tooling to v1.1.14 (#107)

### Software-Änderungen

- Podman container script and CI workflow (#45) (#46) (#46)
- Mount model dir rw, fix export paths, add export dirs step 
- Disable git credential prompt for public repo clone 
- Bypass git credential helper for public repo clone 
- Move git clone to workflow step, script only builds image 
- Use actions/checkout to clone Bausteinsicht repo 
- Drop container approach, run binary directly in CI 
- Install draw.io CLI and use xvfb-run for PNG export 
- SonarCloud Integration für Quality Monitoring (#47) (#48) (#48)
- Remove duplicate OUTPUT env for git-cliff, increase Pages smoke-test sleep to 30s 
- Replace fixed sleep with retry loop for Pages smoke-test (max 3min) 
- Git-cliff write to temp file then prepend to CHANGELOG.md 
- Copy bb_dashboard.html to index.html for GitHub Pages 
- Start_ticket zeigt automatisch Issue-Liste bei leerem Argument (#61) (#61)
- Automatisches PR-Review mit Bot-Token-Support in start_ticket (#64) (#64)
- ShellCheck SARIF Report für SonarCloud (#55) (#68) (#68)
- Deaktiviere C/C++ SonarCloud-Analyse + verbessertes Error Reporting (#70) (#70)
- POST /api/v1/backend wechselt jetzt tatsächlich den HAL-Backend (#72) (#72)
- Trend-Cache Git-Fallback via reports-Branch (#74) (#74)
- POST-Handler geben 400 bei ungültigem JSON zurück (#75) (#75)
- HTTP-Server mit ReadTimeout/WriteTimeout/IdleTimeout (Issue #21) (#77) (#77)
- Regression Test für BME280StreamHandler Flusher nil-Check (Issue #27) (#79) (#79)
- Flag.Parse() aus Library-Package entfernt (Issue #26) (#81) (#81)
- CORS OPTIONS Preflight-Requests behandeln (Issue #22) (#83) (#83)
- Collect_results.py + statisch/dynamisch Trennung (Issue #15) (#84) (#84)
- Phase 1 — Tooling in tooling/ Ordner gruppieren (Issue #85) (#86) (#86)
- Phase 3 — tooling/ aus Repo entfernen, via Release-Download (Issue #85) (#87) (#87)
- C Code Coverage CI-Integration (#88) (#88)
- Use download-tooling composite action 
- Use go-test composite action 
- Use shellcheck-sarif and c-test composite actions 
- Add explicit download-tooling step before go-test 
- Git worktree --orphan syntax für git 2.40+ 
- Use strictdoc and test-report composite actions 
- Use sonarcloud composite action 
- Remove download-tooling steps — scripts via GITHUB_ACTION_PATH 
- Add security-events:write for SARIF upload, bump to v1.1.9 
- Add strictdoc SARIF + requirements coverage, bump to v1.1.11 
- Alle SARIF- und Rust-Coverage-Pfade in sonar-project.properties ergänzen 


# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Infrastruktur & Tooling

- Use container script instead of inline podman commands 
- Separate build step from run commands 
- Add export-diagram, export-table and export-png steps 
- Commit export changes back to repo if files changed 
- Update exported diagrams [skip ci] 
- Update exported diagrams [skip ci] 
- Trigger only on beaglebone_black.jsonc changes 
- Trigger SonarCloud verification 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Gruppierung nach Software-Änderungen und Infrastruktur & Tooling (#65) (#65)
- Erstelle PR statt direktem Push auf main (branch protection fix) (#66) (#66)
- Update unreleased section [skip ci] (#67) (#67)
- Update unreleased section [skip ci] (#69) (#69)
- Update unreleased section [skip ci] (#71) (#71)
- Update unreleased section [skip ci] (#73) (#73)
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] (#76) (#76)
- Add entry for Issue #31 fix (#75) [skip ci] 
- Update unreleased section [skip ci] (#78) (#78)
- Add entry for Issue #21 fix (#77) [skip ci] 
- Update unreleased section [skip ci] (#80) (#80)
- Add entry for Issue #27 fix (#79) [skip ci] 
- Update unreleased section [skip ci] (#82) (#82)
- Update unreleased section [skip ci] (#89) (#89)
- Beaglebone-tooling auf v1.1.0 aktualisieren (#90) (#90)
- Update unreleased section [skip ci] (#91) (#91)
- Bump beaglebone-tooling actions to v1.1.1 
- Update unreleased section [skip ci] (#92) (#92)
- Bump beaglebone-tooling actions to v1.1.2 
- Update unreleased section [skip ci] (#93) (#93)
- Update unreleased section [skip ci] (#94) (#94)
- Bump beaglebone-tooling actions to v1.1.3 
- Update unreleased section [skip ci] (#95) (#95)
- Bump beaglebone-tooling actions to v1.1.4 
- Update unreleased section [skip ci] (#96) (#96)
- Bump beaglebone-tooling actions to v1.1.5 
- Update unreleased section [skip ci] (#97) (#97)
- Bump beaglebone-tooling actions to v1.1.6 
- Update unreleased section [skip ci] (#98) (#98)
- Replace all inline steps with beaglebone-tooling composite actions @v1.1.7 
- Update unreleased section [skip ci] (#99) (#99)
- Bump beaglebone-tooling actions to v1.1.8 
- Update unreleased section [skip ci] (#100) (#100)
- Bump beaglebone-tooling actions to v1.1.10 (fix junit_to_sarif) 
- Update unreleased section [skip ci] (#102) (#102)
- Update unreleased section [skip ci] (#103) (#103)
- Bump beaglebone-tooling to v1.1.12 
- Update unreleased section [skip ci] (#104) (#104)
- Bump beaglebone-tooling to v1.1.13 
- Update unreleased section [skip ci] (#105) (#105)

### Software-Änderungen

- Podman container script and CI workflow (#45) (#46) (#46)
- Mount model dir rw, fix export paths, add export dirs step 
- Disable git credential prompt for public repo clone 
- Bypass git credential helper for public repo clone 
- Move git clone to workflow step, script only builds image 
- Use actions/checkout to clone Bausteinsicht repo 
- Drop container approach, run binary directly in CI 
- Install draw.io CLI and use xvfb-run for PNG export 
- SonarCloud Integration für Quality Monitoring (#47) (#48) (#48)
- Remove duplicate OUTPUT env for git-cliff, increase Pages smoke-test sleep to 30s 
- Replace fixed sleep with retry loop for Pages smoke-test (max 3min) 
- Git-cliff write to temp file then prepend to CHANGELOG.md 
- Copy bb_dashboard.html to index.html for GitHub Pages 
- Start_ticket zeigt automatisch Issue-Liste bei leerem Argument (#61) (#61)
- Automatisches PR-Review mit Bot-Token-Support in start_ticket (#64) (#64)
- ShellCheck SARIF Report für SonarCloud (#55) (#68) (#68)
- Deaktiviere C/C++ SonarCloud-Analyse + verbessertes Error Reporting (#70) (#70)
- POST /api/v1/backend wechselt jetzt tatsächlich den HAL-Backend (#72) (#72)
- Trend-Cache Git-Fallback via reports-Branch (#74) (#74)
- POST-Handler geben 400 bei ungültigem JSON zurück (#75) (#75)
- HTTP-Server mit ReadTimeout/WriteTimeout/IdleTimeout (Issue #21) (#77) (#77)
- Regression Test für BME280StreamHandler Flusher nil-Check (Issue #27) (#79) (#79)
- Flag.Parse() aus Library-Package entfernt (Issue #26) (#81) (#81)
- CORS OPTIONS Preflight-Requests behandeln (Issue #22) (#83) (#83)
- Collect_results.py + statisch/dynamisch Trennung (Issue #15) (#84) (#84)
- Phase 1 — Tooling in tooling/ Ordner gruppieren (Issue #85) (#86) (#86)
- Phase 3 — tooling/ aus Repo entfernen, via Release-Download (Issue #85) (#87) (#87)
- C Code Coverage CI-Integration (#88) (#88)
- Use download-tooling composite action 
- Use go-test composite action 
- Use shellcheck-sarif and c-test composite actions 
- Add explicit download-tooling step before go-test 
- Git worktree --orphan syntax für git 2.40+ 
- Use strictdoc and test-report composite actions 
- Use sonarcloud composite action 
- Remove download-tooling steps — scripts via GITHUB_ACTION_PATH 
- Add security-events:write for SARIF upload, bump to v1.1.9 
- Add strictdoc SARIF + requirements coverage, bump to v1.1.11 
- Alle SARIF- und Rust-Coverage-Pfade in sonar-project.properties ergänzen 


# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Infrastruktur & Tooling

- Use container script instead of inline podman commands 
- Separate build step from run commands 
- Add export-diagram, export-table and export-png steps 
- Commit export changes back to repo if files changed 
- Update exported diagrams [skip ci] 
- Update exported diagrams [skip ci] 
- Trigger only on beaglebone_black.jsonc changes 
- Trigger SonarCloud verification 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Gruppierung nach Software-Änderungen und Infrastruktur & Tooling (#65) (#65)
- Erstelle PR statt direktem Push auf main (branch protection fix) (#66) (#66)
- Update unreleased section [skip ci] (#67) (#67)
- Update unreleased section [skip ci] (#69) (#69)
- Update unreleased section [skip ci] (#71) (#71)
- Update unreleased section [skip ci] (#73) (#73)
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] (#76) (#76)
- Add entry for Issue #31 fix (#75) [skip ci] 
- Update unreleased section [skip ci] (#78) (#78)
- Add entry for Issue #21 fix (#77) [skip ci] 
- Update unreleased section [skip ci] (#80) (#80)
- Add entry for Issue #27 fix (#79) [skip ci] 
- Update unreleased section [skip ci] (#82) (#82)
- Update unreleased section [skip ci] (#89) (#89)
- Beaglebone-tooling auf v1.1.0 aktualisieren (#90) (#90)
- Update unreleased section [skip ci] (#91) (#91)
- Bump beaglebone-tooling actions to v1.1.1 
- Update unreleased section [skip ci] (#92) (#92)
- Bump beaglebone-tooling actions to v1.1.2 
- Update unreleased section [skip ci] (#93) (#93)
- Update unreleased section [skip ci] (#94) (#94)
- Bump beaglebone-tooling actions to v1.1.3 
- Update unreleased section [skip ci] (#95) (#95)
- Bump beaglebone-tooling actions to v1.1.4 
- Update unreleased section [skip ci] (#96) (#96)
- Bump beaglebone-tooling actions to v1.1.5 
- Update unreleased section [skip ci] (#97) (#97)
- Bump beaglebone-tooling actions to v1.1.6 
- Update unreleased section [skip ci] (#98) (#98)
- Replace all inline steps with beaglebone-tooling composite actions @v1.1.7 
- Update unreleased section [skip ci] (#99) (#99)
- Bump beaglebone-tooling actions to v1.1.8 
- Update unreleased section [skip ci] (#100) (#100)
- Bump beaglebone-tooling actions to v1.1.10 (fix junit_to_sarif) 
- Update unreleased section [skip ci] (#102) (#102)
- Update unreleased section [skip ci] (#103) (#103)
- Bump beaglebone-tooling to v1.1.12 
- Update unreleased section [skip ci] (#104) (#104)
- Bump beaglebone-tooling to v1.1.13 

### Software-Änderungen

- Podman container script and CI workflow (#45) (#46) (#46)
- Mount model dir rw, fix export paths, add export dirs step 
- Disable git credential prompt for public repo clone 
- Bypass git credential helper for public repo clone 
- Move git clone to workflow step, script only builds image 
- Use actions/checkout to clone Bausteinsicht repo 
- Drop container approach, run binary directly in CI 
- Install draw.io CLI and use xvfb-run for PNG export 
- SonarCloud Integration für Quality Monitoring (#47) (#48) (#48)
- Remove duplicate OUTPUT env for git-cliff, increase Pages smoke-test sleep to 30s 
- Replace fixed sleep with retry loop for Pages smoke-test (max 3min) 
- Git-cliff write to temp file then prepend to CHANGELOG.md 
- Copy bb_dashboard.html to index.html for GitHub Pages 
- Start_ticket zeigt automatisch Issue-Liste bei leerem Argument (#61) (#61)
- Automatisches PR-Review mit Bot-Token-Support in start_ticket (#64) (#64)
- ShellCheck SARIF Report für SonarCloud (#55) (#68) (#68)
- Deaktiviere C/C++ SonarCloud-Analyse + verbessertes Error Reporting (#70) (#70)
- POST /api/v1/backend wechselt jetzt tatsächlich den HAL-Backend (#72) (#72)
- Trend-Cache Git-Fallback via reports-Branch (#74) (#74)
- POST-Handler geben 400 bei ungültigem JSON zurück (#75) (#75)
- HTTP-Server mit ReadTimeout/WriteTimeout/IdleTimeout (Issue #21) (#77) (#77)
- Regression Test für BME280StreamHandler Flusher nil-Check (Issue #27) (#79) (#79)
- Flag.Parse() aus Library-Package entfernt (Issue #26) (#81) (#81)
- CORS OPTIONS Preflight-Requests behandeln (Issue #22) (#83) (#83)
- Collect_results.py + statisch/dynamisch Trennung (Issue #15) (#84) (#84)
- Phase 1 — Tooling in tooling/ Ordner gruppieren (Issue #85) (#86) (#86)
- Phase 3 — tooling/ aus Repo entfernen, via Release-Download (Issue #85) (#87) (#87)
- C Code Coverage CI-Integration (#88) (#88)
- Use download-tooling composite action 
- Use go-test composite action 
- Use shellcheck-sarif and c-test composite actions 
- Add explicit download-tooling step before go-test 
- Git worktree --orphan syntax für git 2.40+ 
- Use strictdoc and test-report composite actions 
- Use sonarcloud composite action 
- Remove download-tooling steps — scripts via GITHUB_ACTION_PATH 
- Add security-events:write for SARIF upload, bump to v1.1.9 
- Add strictdoc SARIF + requirements coverage, bump to v1.1.11 


# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Infrastruktur & Tooling

- Use container script instead of inline podman commands 
- Separate build step from run commands 
- Add export-diagram, export-table and export-png steps 
- Commit export changes back to repo if files changed 
- Update exported diagrams [skip ci] 
- Update exported diagrams [skip ci] 
- Trigger only on beaglebone_black.jsonc changes 
- Trigger SonarCloud verification 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Gruppierung nach Software-Änderungen und Infrastruktur & Tooling (#65) (#65)
- Erstelle PR statt direktem Push auf main (branch protection fix) (#66) (#66)
- Update unreleased section [skip ci] (#67) (#67)
- Update unreleased section [skip ci] (#69) (#69)
- Update unreleased section [skip ci] (#71) (#71)
- Update unreleased section [skip ci] (#73) (#73)
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] (#76) (#76)
- Add entry for Issue #31 fix (#75) [skip ci] 
- Update unreleased section [skip ci] (#78) (#78)
- Add entry for Issue #21 fix (#77) [skip ci] 
- Update unreleased section [skip ci] (#80) (#80)
- Add entry for Issue #27 fix (#79) [skip ci] 
- Update unreleased section [skip ci] (#82) (#82)
- Update unreleased section [skip ci] (#89) (#89)
- Beaglebone-tooling auf v1.1.0 aktualisieren (#90) (#90)
- Update unreleased section [skip ci] (#91) (#91)
- Bump beaglebone-tooling actions to v1.1.1 
- Update unreleased section [skip ci] (#92) (#92)
- Bump beaglebone-tooling actions to v1.1.2 
- Update unreleased section [skip ci] (#93) (#93)
- Update unreleased section [skip ci] (#94) (#94)
- Bump beaglebone-tooling actions to v1.1.3 
- Update unreleased section [skip ci] (#95) (#95)
- Bump beaglebone-tooling actions to v1.1.4 
- Update unreleased section [skip ci] (#96) (#96)
- Bump beaglebone-tooling actions to v1.1.5 
- Update unreleased section [skip ci] (#97) (#97)
- Bump beaglebone-tooling actions to v1.1.6 
- Update unreleased section [skip ci] (#98) (#98)
- Replace all inline steps with beaglebone-tooling composite actions @v1.1.7 
- Update unreleased section [skip ci] (#99) (#99)
- Bump beaglebone-tooling actions to v1.1.8 
- Update unreleased section [skip ci] (#100) (#100)
- Bump beaglebone-tooling actions to v1.1.10 (fix junit_to_sarif) 
- Update unreleased section [skip ci] (#102) (#102)
- Update unreleased section [skip ci] (#103) (#103)
- Bump beaglebone-tooling to v1.1.12 

### Software-Änderungen

- Podman container script and CI workflow (#45) (#46) (#46)
- Mount model dir rw, fix export paths, add export dirs step 
- Disable git credential prompt for public repo clone 
- Bypass git credential helper for public repo clone 
- Move git clone to workflow step, script only builds image 
- Use actions/checkout to clone Bausteinsicht repo 
- Drop container approach, run binary directly in CI 
- Install draw.io CLI and use xvfb-run for PNG export 
- SonarCloud Integration für Quality Monitoring (#47) (#48) (#48)
- Remove duplicate OUTPUT env for git-cliff, increase Pages smoke-test sleep to 30s 
- Replace fixed sleep with retry loop for Pages smoke-test (max 3min) 
- Git-cliff write to temp file then prepend to CHANGELOG.md 
- Copy bb_dashboard.html to index.html for GitHub Pages 
- Start_ticket zeigt automatisch Issue-Liste bei leerem Argument (#61) (#61)
- Automatisches PR-Review mit Bot-Token-Support in start_ticket (#64) (#64)
- ShellCheck SARIF Report für SonarCloud (#55) (#68) (#68)
- Deaktiviere C/C++ SonarCloud-Analyse + verbessertes Error Reporting (#70) (#70)
- POST /api/v1/backend wechselt jetzt tatsächlich den HAL-Backend (#72) (#72)
- Trend-Cache Git-Fallback via reports-Branch (#74) (#74)
- POST-Handler geben 400 bei ungültigem JSON zurück (#75) (#75)
- HTTP-Server mit ReadTimeout/WriteTimeout/IdleTimeout (Issue #21) (#77) (#77)
- Regression Test für BME280StreamHandler Flusher nil-Check (Issue #27) (#79) (#79)
- Flag.Parse() aus Library-Package entfernt (Issue #26) (#81) (#81)
- CORS OPTIONS Preflight-Requests behandeln (Issue #22) (#83) (#83)
- Collect_results.py + statisch/dynamisch Trennung (Issue #15) (#84) (#84)
- Phase 1 — Tooling in tooling/ Ordner gruppieren (Issue #85) (#86) (#86)
- Phase 3 — tooling/ aus Repo entfernen, via Release-Download (Issue #85) (#87) (#87)
- C Code Coverage CI-Integration (#88) (#88)
- Use download-tooling composite action 
- Use go-test composite action 
- Use shellcheck-sarif and c-test composite actions 
- Add explicit download-tooling step before go-test 
- Git worktree --orphan syntax für git 2.40+ 
- Use strictdoc and test-report composite actions 
- Use sonarcloud composite action 
- Remove download-tooling steps — scripts via GITHUB_ACTION_PATH 
- Add security-events:write for SARIF upload, bump to v1.1.9 
- Add strictdoc SARIF + requirements coverage, bump to v1.1.11 


# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Infrastruktur & Tooling

- Use container script instead of inline podman commands 
- Separate build step from run commands 
- Add export-diagram, export-table and export-png steps 
- Commit export changes back to repo if files changed 
- Update exported diagrams [skip ci] 
- Update exported diagrams [skip ci] 
- Trigger only on beaglebone_black.jsonc changes 
- Trigger SonarCloud verification 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Gruppierung nach Software-Änderungen und Infrastruktur & Tooling (#65) (#65)
- Erstelle PR statt direktem Push auf main (branch protection fix) (#66) (#66)
- Update unreleased section [skip ci] (#67) (#67)
- Update unreleased section [skip ci] (#69) (#69)
- Update unreleased section [skip ci] (#71) (#71)
- Update unreleased section [skip ci] (#73) (#73)
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] (#76) (#76)
- Add entry for Issue #31 fix (#75) [skip ci] 
- Update unreleased section [skip ci] (#78) (#78)
- Add entry for Issue #21 fix (#77) [skip ci] 
- Update unreleased section [skip ci] (#80) (#80)
- Add entry for Issue #27 fix (#79) [skip ci] 
- Update unreleased section [skip ci] (#82) (#82)
- Update unreleased section [skip ci] (#89) (#89)
- Beaglebone-tooling auf v1.1.0 aktualisieren (#90) (#90)
- Update unreleased section [skip ci] (#91) (#91)
- Bump beaglebone-tooling actions to v1.1.1 
- Update unreleased section [skip ci] (#92) (#92)
- Bump beaglebone-tooling actions to v1.1.2 
- Update unreleased section [skip ci] (#93) (#93)
- Update unreleased section [skip ci] (#94) (#94)
- Bump beaglebone-tooling actions to v1.1.3 
- Update unreleased section [skip ci] (#95) (#95)
- Bump beaglebone-tooling actions to v1.1.4 
- Update unreleased section [skip ci] (#96) (#96)
- Bump beaglebone-tooling actions to v1.1.5 
- Update unreleased section [skip ci] (#97) (#97)
- Bump beaglebone-tooling actions to v1.1.6 
- Update unreleased section [skip ci] (#98) (#98)
- Replace all inline steps with beaglebone-tooling composite actions @v1.1.7 
- Update unreleased section [skip ci] (#99) (#99)
- Bump beaglebone-tooling actions to v1.1.8 
- Update unreleased section [skip ci] (#100) (#100)
- Bump beaglebone-tooling actions to v1.1.10 (fix junit_to_sarif) 
- Update unreleased section [skip ci] (#102) (#102)

### Software-Änderungen

- Podman container script and CI workflow (#45) (#46) (#46)
- Mount model dir rw, fix export paths, add export dirs step 
- Disable git credential prompt for public repo clone 
- Bypass git credential helper for public repo clone 
- Move git clone to workflow step, script only builds image 
- Use actions/checkout to clone Bausteinsicht repo 
- Drop container approach, run binary directly in CI 
- Install draw.io CLI and use xvfb-run for PNG export 
- SonarCloud Integration für Quality Monitoring (#47) (#48) (#48)
- Remove duplicate OUTPUT env for git-cliff, increase Pages smoke-test sleep to 30s 
- Replace fixed sleep with retry loop for Pages smoke-test (max 3min) 
- Git-cliff write to temp file then prepend to CHANGELOG.md 
- Copy bb_dashboard.html to index.html for GitHub Pages 
- Start_ticket zeigt automatisch Issue-Liste bei leerem Argument (#61) (#61)
- Automatisches PR-Review mit Bot-Token-Support in start_ticket (#64) (#64)
- ShellCheck SARIF Report für SonarCloud (#55) (#68) (#68)
- Deaktiviere C/C++ SonarCloud-Analyse + verbessertes Error Reporting (#70) (#70)
- POST /api/v1/backend wechselt jetzt tatsächlich den HAL-Backend (#72) (#72)
- Trend-Cache Git-Fallback via reports-Branch (#74) (#74)
- POST-Handler geben 400 bei ungültigem JSON zurück (#75) (#75)
- HTTP-Server mit ReadTimeout/WriteTimeout/IdleTimeout (Issue #21) (#77) (#77)
- Regression Test für BME280StreamHandler Flusher nil-Check (Issue #27) (#79) (#79)
- Flag.Parse() aus Library-Package entfernt (Issue #26) (#81) (#81)
- CORS OPTIONS Preflight-Requests behandeln (Issue #22) (#83) (#83)
- Collect_results.py + statisch/dynamisch Trennung (Issue #15) (#84) (#84)
- Phase 1 — Tooling in tooling/ Ordner gruppieren (Issue #85) (#86) (#86)
- Phase 3 — tooling/ aus Repo entfernen, via Release-Download (Issue #85) (#87) (#87)
- C Code Coverage CI-Integration (#88) (#88)
- Use download-tooling composite action 
- Use go-test composite action 
- Use shellcheck-sarif and c-test composite actions 
- Add explicit download-tooling step before go-test 
- Git worktree --orphan syntax für git 2.40+ 
- Use strictdoc and test-report composite actions 
- Use sonarcloud composite action 
- Remove download-tooling steps — scripts via GITHUB_ACTION_PATH 
- Add security-events:write for SARIF upload, bump to v1.1.9 
- Add strictdoc SARIF + requirements coverage, bump to v1.1.11 


# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Infrastruktur & Tooling

- Use container script instead of inline podman commands 
- Separate build step from run commands 
- Add export-diagram, export-table and export-png steps 
- Commit export changes back to repo if files changed 
- Update exported diagrams [skip ci] 
- Update exported diagrams [skip ci] 
- Trigger only on beaglebone_black.jsonc changes 
- Trigger SonarCloud verification 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Gruppierung nach Software-Änderungen und Infrastruktur & Tooling (#65) (#65)
- Erstelle PR statt direktem Push auf main (branch protection fix) (#66) (#66)
- Update unreleased section [skip ci] (#67) (#67)
- Update unreleased section [skip ci] (#69) (#69)
- Update unreleased section [skip ci] (#71) (#71)
- Update unreleased section [skip ci] (#73) (#73)
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] (#76) (#76)
- Add entry for Issue #31 fix (#75) [skip ci] 
- Update unreleased section [skip ci] (#78) (#78)
- Add entry for Issue #21 fix (#77) [skip ci] 
- Update unreleased section [skip ci] (#80) (#80)
- Add entry for Issue #27 fix (#79) [skip ci] 
- Update unreleased section [skip ci] (#82) (#82)
- Update unreleased section [skip ci] (#89) (#89)
- Beaglebone-tooling auf v1.1.0 aktualisieren (#90) (#90)
- Update unreleased section [skip ci] (#91) (#91)
- Bump beaglebone-tooling actions to v1.1.1 
- Update unreleased section [skip ci] (#92) (#92)
- Bump beaglebone-tooling actions to v1.1.2 
- Update unreleased section [skip ci] (#93) (#93)
- Update unreleased section [skip ci] (#94) (#94)
- Bump beaglebone-tooling actions to v1.1.3 
- Update unreleased section [skip ci] (#95) (#95)
- Bump beaglebone-tooling actions to v1.1.4 
- Update unreleased section [skip ci] (#96) (#96)
- Bump beaglebone-tooling actions to v1.1.5 
- Update unreleased section [skip ci] (#97) (#97)
- Bump beaglebone-tooling actions to v1.1.6 
- Update unreleased section [skip ci] (#98) (#98)
- Replace all inline steps with beaglebone-tooling composite actions @v1.1.7 
- Update unreleased section [skip ci] (#99) (#99)
- Bump beaglebone-tooling actions to v1.1.8 
- Update unreleased section [skip ci] (#100) (#100)
- Bump beaglebone-tooling actions to v1.1.10 (fix junit_to_sarif) 

### Software-Änderungen

- Podman container script and CI workflow (#45) (#46) (#46)
- Mount model dir rw, fix export paths, add export dirs step 
- Disable git credential prompt for public repo clone 
- Bypass git credential helper for public repo clone 
- Move git clone to workflow step, script only builds image 
- Use actions/checkout to clone Bausteinsicht repo 
- Drop container approach, run binary directly in CI 
- Install draw.io CLI and use xvfb-run for PNG export 
- SonarCloud Integration für Quality Monitoring (#47) (#48) (#48)
- Remove duplicate OUTPUT env for git-cliff, increase Pages smoke-test sleep to 30s 
- Replace fixed sleep with retry loop for Pages smoke-test (max 3min) 
- Git-cliff write to temp file then prepend to CHANGELOG.md 
- Copy bb_dashboard.html to index.html for GitHub Pages 
- Start_ticket zeigt automatisch Issue-Liste bei leerem Argument (#61) (#61)
- Automatisches PR-Review mit Bot-Token-Support in start_ticket (#64) (#64)
- ShellCheck SARIF Report für SonarCloud (#55) (#68) (#68)
- Deaktiviere C/C++ SonarCloud-Analyse + verbessertes Error Reporting (#70) (#70)
- POST /api/v1/backend wechselt jetzt tatsächlich den HAL-Backend (#72) (#72)
- Trend-Cache Git-Fallback via reports-Branch (#74) (#74)
- POST-Handler geben 400 bei ungültigem JSON zurück (#75) (#75)
- HTTP-Server mit ReadTimeout/WriteTimeout/IdleTimeout (Issue #21) (#77) (#77)
- Regression Test für BME280StreamHandler Flusher nil-Check (Issue #27) (#79) (#79)
- Flag.Parse() aus Library-Package entfernt (Issue #26) (#81) (#81)
- CORS OPTIONS Preflight-Requests behandeln (Issue #22) (#83) (#83)
- Collect_results.py + statisch/dynamisch Trennung (Issue #15) (#84) (#84)
- Phase 1 — Tooling in tooling/ Ordner gruppieren (Issue #85) (#86) (#86)
- Phase 3 — tooling/ aus Repo entfernen, via Release-Download (Issue #85) (#87) (#87)
- C Code Coverage CI-Integration (#88) (#88)
- Use download-tooling composite action 
- Use go-test composite action 
- Use shellcheck-sarif and c-test composite actions 
- Add explicit download-tooling step before go-test 
- Git worktree --orphan syntax für git 2.40+ 
- Use strictdoc and test-report composite actions 
- Use sonarcloud composite action 
- Remove download-tooling steps — scripts via GITHUB_ACTION_PATH 
- Add security-events:write for SARIF upload, bump to v1.1.9 


# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Infrastruktur & Tooling

- Use container script instead of inline podman commands 
- Separate build step from run commands 
- Add export-diagram, export-table and export-png steps 
- Commit export changes back to repo if files changed 
- Update exported diagrams [skip ci] 
- Update exported diagrams [skip ci] 
- Trigger only on beaglebone_black.jsonc changes 
- Trigger SonarCloud verification 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Gruppierung nach Software-Änderungen und Infrastruktur & Tooling (#65) (#65)
- Erstelle PR statt direktem Push auf main (branch protection fix) (#66) (#66)
- Update unreleased section [skip ci] (#67) (#67)
- Update unreleased section [skip ci] (#69) (#69)
- Update unreleased section [skip ci] (#71) (#71)
- Update unreleased section [skip ci] (#73) (#73)
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] (#76) (#76)
- Add entry for Issue #31 fix (#75) [skip ci] 
- Update unreleased section [skip ci] (#78) (#78)
- Add entry for Issue #21 fix (#77) [skip ci] 
- Update unreleased section [skip ci] (#80) (#80)
- Add entry for Issue #27 fix (#79) [skip ci] 
- Update unreleased section [skip ci] (#82) (#82)
- Update unreleased section [skip ci] (#89) (#89)
- Beaglebone-tooling auf v1.1.0 aktualisieren (#90) (#90)
- Update unreleased section [skip ci] (#91) (#91)
- Bump beaglebone-tooling actions to v1.1.1 
- Update unreleased section [skip ci] (#92) (#92)
- Bump beaglebone-tooling actions to v1.1.2 
- Update unreleased section [skip ci] (#93) (#93)
- Update unreleased section [skip ci] (#94) (#94)
- Bump beaglebone-tooling actions to v1.1.3 
- Update unreleased section [skip ci] (#95) (#95)
- Bump beaglebone-tooling actions to v1.1.4 
- Update unreleased section [skip ci] (#96) (#96)
- Bump beaglebone-tooling actions to v1.1.5 
- Update unreleased section [skip ci] (#97) (#97)
- Bump beaglebone-tooling actions to v1.1.6 
- Update unreleased section [skip ci] (#98) (#98)
- Replace all inline steps with beaglebone-tooling composite actions @v1.1.7 
- Update unreleased section [skip ci] (#99) (#99)
- Bump beaglebone-tooling actions to v1.1.8 

### Software-Änderungen

- Podman container script and CI workflow (#45) (#46) (#46)
- Mount model dir rw, fix export paths, add export dirs step 
- Disable git credential prompt for public repo clone 
- Bypass git credential helper for public repo clone 
- Move git clone to workflow step, script only builds image 
- Use actions/checkout to clone Bausteinsicht repo 
- Drop container approach, run binary directly in CI 
- Install draw.io CLI and use xvfb-run for PNG export 
- SonarCloud Integration für Quality Monitoring (#47) (#48) (#48)
- Remove duplicate OUTPUT env for git-cliff, increase Pages smoke-test sleep to 30s 
- Replace fixed sleep with retry loop for Pages smoke-test (max 3min) 
- Git-cliff write to temp file then prepend to CHANGELOG.md 
- Copy bb_dashboard.html to index.html for GitHub Pages 
- Start_ticket zeigt automatisch Issue-Liste bei leerem Argument (#61) (#61)
- Automatisches PR-Review mit Bot-Token-Support in start_ticket (#64) (#64)
- ShellCheck SARIF Report für SonarCloud (#55) (#68) (#68)
- Deaktiviere C/C++ SonarCloud-Analyse + verbessertes Error Reporting (#70) (#70)
- POST /api/v1/backend wechselt jetzt tatsächlich den HAL-Backend (#72) (#72)
- Trend-Cache Git-Fallback via reports-Branch (#74) (#74)
- POST-Handler geben 400 bei ungültigem JSON zurück (#75) (#75)
- HTTP-Server mit ReadTimeout/WriteTimeout/IdleTimeout (Issue #21) (#77) (#77)
- Regression Test für BME280StreamHandler Flusher nil-Check (Issue #27) (#79) (#79)
- Flag.Parse() aus Library-Package entfernt (Issue #26) (#81) (#81)
- CORS OPTIONS Preflight-Requests behandeln (Issue #22) (#83) (#83)
- Collect_results.py + statisch/dynamisch Trennung (Issue #15) (#84) (#84)
- Phase 1 — Tooling in tooling/ Ordner gruppieren (Issue #85) (#86) (#86)
- Phase 3 — tooling/ aus Repo entfernen, via Release-Download (Issue #85) (#87) (#87)
- C Code Coverage CI-Integration (#88) (#88)
- Use download-tooling composite action 
- Use go-test composite action 
- Use shellcheck-sarif and c-test composite actions 
- Add explicit download-tooling step before go-test 
- Git worktree --orphan syntax für git 2.40+ 
- Use strictdoc and test-report composite actions 
- Use sonarcloud composite action 
- Remove download-tooling steps — scripts via GITHUB_ACTION_PATH 


# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Infrastruktur & Tooling

- Use container script instead of inline podman commands 
- Separate build step from run commands 
- Add export-diagram, export-table and export-png steps 
- Commit export changes back to repo if files changed 
- Update exported diagrams [skip ci] 
- Update exported diagrams [skip ci] 
- Trigger only on beaglebone_black.jsonc changes 
- Trigger SonarCloud verification 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Gruppierung nach Software-Änderungen und Infrastruktur & Tooling (#65) (#65)
- Erstelle PR statt direktem Push auf main (branch protection fix) (#66) (#66)
- Update unreleased section [skip ci] (#67) (#67)
- Update unreleased section [skip ci] (#69) (#69)
- Update unreleased section [skip ci] (#71) (#71)
- Update unreleased section [skip ci] (#73) (#73)
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] (#76) (#76)
- Add entry for Issue #31 fix (#75) [skip ci] 
- Update unreleased section [skip ci] (#78) (#78)
- Add entry for Issue #21 fix (#77) [skip ci] 
- Update unreleased section [skip ci] (#80) (#80)
- Add entry for Issue #27 fix (#79) [skip ci] 
- Update unreleased section [skip ci] (#82) (#82)
- Update unreleased section [skip ci] (#89) (#89)
- Beaglebone-tooling auf v1.1.0 aktualisieren (#90) (#90)
- Update unreleased section [skip ci] (#91) (#91)
- Bump beaglebone-tooling actions to v1.1.1 
- Update unreleased section [skip ci] (#92) (#92)
- Bump beaglebone-tooling actions to v1.1.2 
- Update unreleased section [skip ci] (#93) (#93)
- Update unreleased section [skip ci] (#94) (#94)
- Bump beaglebone-tooling actions to v1.1.3 
- Update unreleased section [skip ci] (#95) (#95)
- Bump beaglebone-tooling actions to v1.1.4 
- Update unreleased section [skip ci] (#96) (#96)
- Bump beaglebone-tooling actions to v1.1.5 
- Update unreleased section [skip ci] (#97) (#97)
- Bump beaglebone-tooling actions to v1.1.6 
- Update unreleased section [skip ci] (#98) (#98)
- Replace all inline steps with beaglebone-tooling composite actions @v1.1.7 

### Software-Änderungen

- Podman container script and CI workflow (#45) (#46) (#46)
- Mount model dir rw, fix export paths, add export dirs step 
- Disable git credential prompt for public repo clone 
- Bypass git credential helper for public repo clone 
- Move git clone to workflow step, script only builds image 
- Use actions/checkout to clone Bausteinsicht repo 
- Drop container approach, run binary directly in CI 
- Install draw.io CLI and use xvfb-run for PNG export 
- SonarCloud Integration für Quality Monitoring (#47) (#48) (#48)
- Remove duplicate OUTPUT env for git-cliff, increase Pages smoke-test sleep to 30s 
- Replace fixed sleep with retry loop for Pages smoke-test (max 3min) 
- Git-cliff write to temp file then prepend to CHANGELOG.md 
- Copy bb_dashboard.html to index.html for GitHub Pages 
- Start_ticket zeigt automatisch Issue-Liste bei leerem Argument (#61) (#61)
- Automatisches PR-Review mit Bot-Token-Support in start_ticket (#64) (#64)
- ShellCheck SARIF Report für SonarCloud (#55) (#68) (#68)
- Deaktiviere C/C++ SonarCloud-Analyse + verbessertes Error Reporting (#70) (#70)
- POST /api/v1/backend wechselt jetzt tatsächlich den HAL-Backend (#72) (#72)
- Trend-Cache Git-Fallback via reports-Branch (#74) (#74)
- POST-Handler geben 400 bei ungültigem JSON zurück (#75) (#75)
- HTTP-Server mit ReadTimeout/WriteTimeout/IdleTimeout (Issue #21) (#77) (#77)
- Regression Test für BME280StreamHandler Flusher nil-Check (Issue #27) (#79) (#79)
- Flag.Parse() aus Library-Package entfernt (Issue #26) (#81) (#81)
- CORS OPTIONS Preflight-Requests behandeln (Issue #22) (#83) (#83)
- Collect_results.py + statisch/dynamisch Trennung (Issue #15) (#84) (#84)
- Phase 1 — Tooling in tooling/ Ordner gruppieren (Issue #85) (#86) (#86)
- Phase 3 — tooling/ aus Repo entfernen, via Release-Download (Issue #85) (#87) (#87)
- C Code Coverage CI-Integration (#88) (#88)
- Use download-tooling composite action 
- Use go-test composite action 
- Use shellcheck-sarif and c-test composite actions 
- Add explicit download-tooling step before go-test 
- Git worktree --orphan syntax für git 2.40+ 
- Use strictdoc and test-report composite actions 
- Use sonarcloud composite action 
- Remove download-tooling steps — scripts via GITHUB_ACTION_PATH 


# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Infrastruktur & Tooling

- Use container script instead of inline podman commands 
- Separate build step from run commands 
- Add export-diagram, export-table and export-png steps 
- Commit export changes back to repo if files changed 
- Update exported diagrams [skip ci] 
- Update exported diagrams [skip ci] 
- Trigger only on beaglebone_black.jsonc changes 
- Trigger SonarCloud verification 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Gruppierung nach Software-Änderungen und Infrastruktur & Tooling (#65) (#65)
- Erstelle PR statt direktem Push auf main (branch protection fix) (#66) (#66)
- Update unreleased section [skip ci] (#67) (#67)
- Update unreleased section [skip ci] (#69) (#69)
- Update unreleased section [skip ci] (#71) (#71)
- Update unreleased section [skip ci] (#73) (#73)
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] (#76) (#76)
- Add entry for Issue #31 fix (#75) [skip ci] 
- Update unreleased section [skip ci] (#78) (#78)
- Add entry for Issue #21 fix (#77) [skip ci] 
- Update unreleased section [skip ci] (#80) (#80)
- Add entry for Issue #27 fix (#79) [skip ci] 
- Update unreleased section [skip ci] (#82) (#82)
- Update unreleased section [skip ci] (#89) (#89)
- Beaglebone-tooling auf v1.1.0 aktualisieren (#90) (#90)
- Update unreleased section [skip ci] (#91) (#91)
- Bump beaglebone-tooling actions to v1.1.1 
- Update unreleased section [skip ci] (#92) (#92)
- Bump beaglebone-tooling actions to v1.1.2 
- Update unreleased section [skip ci] (#93) (#93)
- Update unreleased section [skip ci] (#94) (#94)
- Bump beaglebone-tooling actions to v1.1.3 
- Update unreleased section [skip ci] (#95) (#95)
- Bump beaglebone-tooling actions to v1.1.4 
- Update unreleased section [skip ci] (#96) (#96)
- Bump beaglebone-tooling actions to v1.1.5 
- Update unreleased section [skip ci] (#97) (#97)
- Bump beaglebone-tooling actions to v1.1.6 

### Software-Änderungen

- Podman container script and CI workflow (#45) (#46) (#46)
- Mount model dir rw, fix export paths, add export dirs step 
- Disable git credential prompt for public repo clone 
- Bypass git credential helper for public repo clone 
- Move git clone to workflow step, script only builds image 
- Use actions/checkout to clone Bausteinsicht repo 
- Drop container approach, run binary directly in CI 
- Install draw.io CLI and use xvfb-run for PNG export 
- SonarCloud Integration für Quality Monitoring (#47) (#48) (#48)
- Remove duplicate OUTPUT env for git-cliff, increase Pages smoke-test sleep to 30s 
- Replace fixed sleep with retry loop for Pages smoke-test (max 3min) 
- Git-cliff write to temp file then prepend to CHANGELOG.md 
- Copy bb_dashboard.html to index.html for GitHub Pages 
- Start_ticket zeigt automatisch Issue-Liste bei leerem Argument (#61) (#61)
- Automatisches PR-Review mit Bot-Token-Support in start_ticket (#64) (#64)
- ShellCheck SARIF Report für SonarCloud (#55) (#68) (#68)
- Deaktiviere C/C++ SonarCloud-Analyse + verbessertes Error Reporting (#70) (#70)
- POST /api/v1/backend wechselt jetzt tatsächlich den HAL-Backend (#72) (#72)
- Trend-Cache Git-Fallback via reports-Branch (#74) (#74)
- POST-Handler geben 400 bei ungültigem JSON zurück (#75) (#75)
- HTTP-Server mit ReadTimeout/WriteTimeout/IdleTimeout (Issue #21) (#77) (#77)
- Regression Test für BME280StreamHandler Flusher nil-Check (Issue #27) (#79) (#79)
- Flag.Parse() aus Library-Package entfernt (Issue #26) (#81) (#81)
- CORS OPTIONS Preflight-Requests behandeln (Issue #22) (#83) (#83)
- Collect_results.py + statisch/dynamisch Trennung (Issue #15) (#84) (#84)
- Phase 1 — Tooling in tooling/ Ordner gruppieren (Issue #85) (#86) (#86)
- Phase 3 — tooling/ aus Repo entfernen, via Release-Download (Issue #85) (#87) (#87)
- C Code Coverage CI-Integration (#88) (#88)
- Use download-tooling composite action 
- Use go-test composite action 
- Use shellcheck-sarif and c-test composite actions 
- Add explicit download-tooling step before go-test 
- Git worktree --orphan syntax für git 2.40+ 
- Use strictdoc and test-report composite actions 
- Use sonarcloud composite action 
- Remove download-tooling steps — scripts via GITHUB_ACTION_PATH 


# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Infrastruktur & Tooling

- Use container script instead of inline podman commands 
- Separate build step from run commands 
- Add export-diagram, export-table and export-png steps 
- Commit export changes back to repo if files changed 
- Update exported diagrams [skip ci] 
- Update exported diagrams [skip ci] 
- Trigger only on beaglebone_black.jsonc changes 
- Trigger SonarCloud verification 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Gruppierung nach Software-Änderungen und Infrastruktur & Tooling (#65) (#65)
- Erstelle PR statt direktem Push auf main (branch protection fix) (#66) (#66)
- Update unreleased section [skip ci] (#67) (#67)
- Update unreleased section [skip ci] (#69) (#69)
- Update unreleased section [skip ci] (#71) (#71)
- Update unreleased section [skip ci] (#73) (#73)
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] (#76) (#76)
- Add entry for Issue #31 fix (#75) [skip ci] 
- Update unreleased section [skip ci] (#78) (#78)
- Add entry for Issue #21 fix (#77) [skip ci] 
- Update unreleased section [skip ci] (#80) (#80)
- Add entry for Issue #27 fix (#79) [skip ci] 
- Update unreleased section [skip ci] (#82) (#82)
- Update unreleased section [skip ci] (#89) (#89)
- Beaglebone-tooling auf v1.1.0 aktualisieren (#90) (#90)
- Update unreleased section [skip ci] (#91) (#91)
- Bump beaglebone-tooling actions to v1.1.1 
- Update unreleased section [skip ci] (#92) (#92)
- Bump beaglebone-tooling actions to v1.1.2 
- Update unreleased section [skip ci] (#93) (#93)
- Update unreleased section [skip ci] (#94) (#94)
- Bump beaglebone-tooling actions to v1.1.3 
- Update unreleased section [skip ci] (#95) (#95)
- Bump beaglebone-tooling actions to v1.1.4 
- Update unreleased section [skip ci] (#96) (#96)
- Bump beaglebone-tooling actions to v1.1.5 

### Software-Änderungen

- Podman container script and CI workflow (#45) (#46) (#46)
- Mount model dir rw, fix export paths, add export dirs step 
- Disable git credential prompt for public repo clone 
- Bypass git credential helper for public repo clone 
- Move git clone to workflow step, script only builds image 
- Use actions/checkout to clone Bausteinsicht repo 
- Drop container approach, run binary directly in CI 
- Install draw.io CLI and use xvfb-run for PNG export 
- SonarCloud Integration für Quality Monitoring (#47) (#48) (#48)
- Remove duplicate OUTPUT env for git-cliff, increase Pages smoke-test sleep to 30s 
- Replace fixed sleep with retry loop for Pages smoke-test (max 3min) 
- Git-cliff write to temp file then prepend to CHANGELOG.md 
- Copy bb_dashboard.html to index.html for GitHub Pages 
- Start_ticket zeigt automatisch Issue-Liste bei leerem Argument (#61) (#61)
- Automatisches PR-Review mit Bot-Token-Support in start_ticket (#64) (#64)
- ShellCheck SARIF Report für SonarCloud (#55) (#68) (#68)
- Deaktiviere C/C++ SonarCloud-Analyse + verbessertes Error Reporting (#70) (#70)
- POST /api/v1/backend wechselt jetzt tatsächlich den HAL-Backend (#72) (#72)
- Trend-Cache Git-Fallback via reports-Branch (#74) (#74)
- POST-Handler geben 400 bei ungültigem JSON zurück (#75) (#75)
- HTTP-Server mit ReadTimeout/WriteTimeout/IdleTimeout (Issue #21) (#77) (#77)
- Regression Test für BME280StreamHandler Flusher nil-Check (Issue #27) (#79) (#79)
- Flag.Parse() aus Library-Package entfernt (Issue #26) (#81) (#81)
- CORS OPTIONS Preflight-Requests behandeln (Issue #22) (#83) (#83)
- Collect_results.py + statisch/dynamisch Trennung (Issue #15) (#84) (#84)
- Phase 1 — Tooling in tooling/ Ordner gruppieren (Issue #85) (#86) (#86)
- Phase 3 — tooling/ aus Repo entfernen, via Release-Download (Issue #85) (#87) (#87)
- C Code Coverage CI-Integration (#88) (#88)
- Use download-tooling composite action 
- Use go-test composite action 
- Use shellcheck-sarif and c-test composite actions 
- Add explicit download-tooling step before go-test 
- Git worktree --orphan syntax für git 2.40+ 
- Use strictdoc and test-report composite actions 
- Use sonarcloud composite action 


# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Infrastruktur & Tooling

- Use container script instead of inline podman commands 
- Separate build step from run commands 
- Add export-diagram, export-table and export-png steps 
- Commit export changes back to repo if files changed 
- Update exported diagrams [skip ci] 
- Update exported diagrams [skip ci] 
- Trigger only on beaglebone_black.jsonc changes 
- Trigger SonarCloud verification 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Gruppierung nach Software-Änderungen und Infrastruktur & Tooling (#65) (#65)
- Erstelle PR statt direktem Push auf main (branch protection fix) (#66) (#66)
- Update unreleased section [skip ci] (#67) (#67)
- Update unreleased section [skip ci] (#69) (#69)
- Update unreleased section [skip ci] (#71) (#71)
- Update unreleased section [skip ci] (#73) (#73)
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] (#76) (#76)
- Add entry for Issue #31 fix (#75) [skip ci] 
- Update unreleased section [skip ci] (#78) (#78)
- Add entry for Issue #21 fix (#77) [skip ci] 
- Update unreleased section [skip ci] (#80) (#80)
- Add entry for Issue #27 fix (#79) [skip ci] 
- Update unreleased section [skip ci] (#82) (#82)
- Update unreleased section [skip ci] (#89) (#89)
- Beaglebone-tooling auf v1.1.0 aktualisieren (#90) (#90)
- Update unreleased section [skip ci] (#91) (#91)
- Bump beaglebone-tooling actions to v1.1.1 
- Update unreleased section [skip ci] (#92) (#92)
- Bump beaglebone-tooling actions to v1.1.2 
- Update unreleased section [skip ci] (#93) (#93)
- Update unreleased section [skip ci] (#94) (#94)
- Bump beaglebone-tooling actions to v1.1.3 
- Update unreleased section [skip ci] (#95) (#95)
- Bump beaglebone-tooling actions to v1.1.4 

### Software-Änderungen

- Podman container script and CI workflow (#45) (#46) (#46)
- Mount model dir rw, fix export paths, add export dirs step 
- Disable git credential prompt for public repo clone 
- Bypass git credential helper for public repo clone 
- Move git clone to workflow step, script only builds image 
- Use actions/checkout to clone Bausteinsicht repo 
- Drop container approach, run binary directly in CI 
- Install draw.io CLI and use xvfb-run for PNG export 
- SonarCloud Integration für Quality Monitoring (#47) (#48) (#48)
- Remove duplicate OUTPUT env for git-cliff, increase Pages smoke-test sleep to 30s 
- Replace fixed sleep with retry loop for Pages smoke-test (max 3min) 
- Git-cliff write to temp file then prepend to CHANGELOG.md 
- Copy bb_dashboard.html to index.html for GitHub Pages 
- Start_ticket zeigt automatisch Issue-Liste bei leerem Argument (#61) (#61)
- Automatisches PR-Review mit Bot-Token-Support in start_ticket (#64) (#64)
- ShellCheck SARIF Report für SonarCloud (#55) (#68) (#68)
- Deaktiviere C/C++ SonarCloud-Analyse + verbessertes Error Reporting (#70) (#70)
- POST /api/v1/backend wechselt jetzt tatsächlich den HAL-Backend (#72) (#72)
- Trend-Cache Git-Fallback via reports-Branch (#74) (#74)
- POST-Handler geben 400 bei ungültigem JSON zurück (#75) (#75)
- HTTP-Server mit ReadTimeout/WriteTimeout/IdleTimeout (Issue #21) (#77) (#77)
- Regression Test für BME280StreamHandler Flusher nil-Check (Issue #27) (#79) (#79)
- Flag.Parse() aus Library-Package entfernt (Issue #26) (#81) (#81)
- CORS OPTIONS Preflight-Requests behandeln (Issue #22) (#83) (#83)
- Collect_results.py + statisch/dynamisch Trennung (Issue #15) (#84) (#84)
- Phase 1 — Tooling in tooling/ Ordner gruppieren (Issue #85) (#86) (#86)
- Phase 3 — tooling/ aus Repo entfernen, via Release-Download (Issue #85) (#87) (#87)
- C Code Coverage CI-Integration (#88) (#88)
- Use download-tooling composite action 
- Use go-test composite action 
- Use shellcheck-sarif and c-test composite actions 
- Add explicit download-tooling step before go-test 
- Git worktree --orphan syntax für git 2.40+ 
- Use strictdoc and test-report composite actions 
- Use sonarcloud composite action 


# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Infrastruktur & Tooling

- Use container script instead of inline podman commands 
- Separate build step from run commands 
- Add export-diagram, export-table and export-png steps 
- Commit export changes back to repo if files changed 
- Update exported diagrams [skip ci] 
- Update exported diagrams [skip ci] 
- Trigger only on beaglebone_black.jsonc changes 
- Trigger SonarCloud verification 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Gruppierung nach Software-Änderungen und Infrastruktur & Tooling (#65) (#65)
- Erstelle PR statt direktem Push auf main (branch protection fix) (#66) (#66)
- Update unreleased section [skip ci] (#67) (#67)
- Update unreleased section [skip ci] (#69) (#69)
- Update unreleased section [skip ci] (#71) (#71)
- Update unreleased section [skip ci] (#73) (#73)
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] (#76) (#76)
- Add entry for Issue #31 fix (#75) [skip ci] 
- Update unreleased section [skip ci] (#78) (#78)
- Add entry for Issue #21 fix (#77) [skip ci] 
- Update unreleased section [skip ci] (#80) (#80)
- Add entry for Issue #27 fix (#79) [skip ci] 
- Update unreleased section [skip ci] (#82) (#82)
- Update unreleased section [skip ci] (#89) (#89)
- Beaglebone-tooling auf v1.1.0 aktualisieren (#90) (#90)
- Update unreleased section [skip ci] (#91) (#91)
- Bump beaglebone-tooling actions to v1.1.1 
- Update unreleased section [skip ci] (#92) (#92)
- Bump beaglebone-tooling actions to v1.1.2 
- Update unreleased section [skip ci] (#93) (#93)
- Update unreleased section [skip ci] (#94) (#94)
- Bump beaglebone-tooling actions to v1.1.3 

### Software-Änderungen

- Podman container script and CI workflow (#45) (#46) (#46)
- Mount model dir rw, fix export paths, add export dirs step 
- Disable git credential prompt for public repo clone 
- Bypass git credential helper for public repo clone 
- Move git clone to workflow step, script only builds image 
- Use actions/checkout to clone Bausteinsicht repo 
- Drop container approach, run binary directly in CI 
- Install draw.io CLI and use xvfb-run for PNG export 
- SonarCloud Integration für Quality Monitoring (#47) (#48) (#48)
- Remove duplicate OUTPUT env for git-cliff, increase Pages smoke-test sleep to 30s 
- Replace fixed sleep with retry loop for Pages smoke-test (max 3min) 
- Git-cliff write to temp file then prepend to CHANGELOG.md 
- Copy bb_dashboard.html to index.html for GitHub Pages 
- Start_ticket zeigt automatisch Issue-Liste bei leerem Argument (#61) (#61)
- Automatisches PR-Review mit Bot-Token-Support in start_ticket (#64) (#64)
- ShellCheck SARIF Report für SonarCloud (#55) (#68) (#68)
- Deaktiviere C/C++ SonarCloud-Analyse + verbessertes Error Reporting (#70) (#70)
- POST /api/v1/backend wechselt jetzt tatsächlich den HAL-Backend (#72) (#72)
- Trend-Cache Git-Fallback via reports-Branch (#74) (#74)
- POST-Handler geben 400 bei ungültigem JSON zurück (#75) (#75)
- HTTP-Server mit ReadTimeout/WriteTimeout/IdleTimeout (Issue #21) (#77) (#77)
- Regression Test für BME280StreamHandler Flusher nil-Check (Issue #27) (#79) (#79)
- Flag.Parse() aus Library-Package entfernt (Issue #26) (#81) (#81)
- CORS OPTIONS Preflight-Requests behandeln (Issue #22) (#83) (#83)
- Collect_results.py + statisch/dynamisch Trennung (Issue #15) (#84) (#84)
- Phase 1 — Tooling in tooling/ Ordner gruppieren (Issue #85) (#86) (#86)
- Phase 3 — tooling/ aus Repo entfernen, via Release-Download (Issue #85) (#87) (#87)
- C Code Coverage CI-Integration (#88) (#88)
- Use download-tooling composite action 
- Use go-test composite action 
- Use shellcheck-sarif and c-test composite actions 
- Add explicit download-tooling step before go-test 
- Git worktree --orphan syntax für git 2.40+ 
- Use strictdoc and test-report composite actions 


# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Infrastruktur & Tooling

- Use container script instead of inline podman commands 
- Separate build step from run commands 
- Add export-diagram, export-table and export-png steps 
- Commit export changes back to repo if files changed 
- Update exported diagrams [skip ci] 
- Update exported diagrams [skip ci] 
- Trigger only on beaglebone_black.jsonc changes 
- Trigger SonarCloud verification 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Gruppierung nach Software-Änderungen und Infrastruktur & Tooling (#65) (#65)
- Erstelle PR statt direktem Push auf main (branch protection fix) (#66) (#66)
- Update unreleased section [skip ci] (#67) (#67)
- Update unreleased section [skip ci] (#69) (#69)
- Update unreleased section [skip ci] (#71) (#71)
- Update unreleased section [skip ci] (#73) (#73)
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] (#76) (#76)
- Add entry for Issue #31 fix (#75) [skip ci] 
- Update unreleased section [skip ci] (#78) (#78)
- Add entry for Issue #21 fix (#77) [skip ci] 
- Update unreleased section [skip ci] (#80) (#80)
- Add entry for Issue #27 fix (#79) [skip ci] 
- Update unreleased section [skip ci] (#82) (#82)
- Update unreleased section [skip ci] (#89) (#89)
- Beaglebone-tooling auf v1.1.0 aktualisieren (#90) (#90)
- Update unreleased section [skip ci] (#91) (#91)
- Bump beaglebone-tooling actions to v1.1.1 
- Update unreleased section [skip ci] (#92) (#92)
- Bump beaglebone-tooling actions to v1.1.2 
- Update unreleased section [skip ci] (#93) (#93)

### Software-Änderungen

- Podman container script and CI workflow (#45) (#46) (#46)
- Mount model dir rw, fix export paths, add export dirs step 
- Disable git credential prompt for public repo clone 
- Bypass git credential helper for public repo clone 
- Move git clone to workflow step, script only builds image 
- Use actions/checkout to clone Bausteinsicht repo 
- Drop container approach, run binary directly in CI 
- Install draw.io CLI and use xvfb-run for PNG export 
- SonarCloud Integration für Quality Monitoring (#47) (#48) (#48)
- Remove duplicate OUTPUT env for git-cliff, increase Pages smoke-test sleep to 30s 
- Replace fixed sleep with retry loop for Pages smoke-test (max 3min) 
- Git-cliff write to temp file then prepend to CHANGELOG.md 
- Copy bb_dashboard.html to index.html for GitHub Pages 
- Start_ticket zeigt automatisch Issue-Liste bei leerem Argument (#61) (#61)
- Automatisches PR-Review mit Bot-Token-Support in start_ticket (#64) (#64)
- ShellCheck SARIF Report für SonarCloud (#55) (#68) (#68)
- Deaktiviere C/C++ SonarCloud-Analyse + verbessertes Error Reporting (#70) (#70)
- POST /api/v1/backend wechselt jetzt tatsächlich den HAL-Backend (#72) (#72)
- Trend-Cache Git-Fallback via reports-Branch (#74) (#74)
- POST-Handler geben 400 bei ungültigem JSON zurück (#75) (#75)
- HTTP-Server mit ReadTimeout/WriteTimeout/IdleTimeout (Issue #21) (#77) (#77)
- Regression Test für BME280StreamHandler Flusher nil-Check (Issue #27) (#79) (#79)
- Flag.Parse() aus Library-Package entfernt (Issue #26) (#81) (#81)
- CORS OPTIONS Preflight-Requests behandeln (Issue #22) (#83) (#83)
- Collect_results.py + statisch/dynamisch Trennung (Issue #15) (#84) (#84)
- Phase 1 — Tooling in tooling/ Ordner gruppieren (Issue #85) (#86) (#86)
- Phase 3 — tooling/ aus Repo entfernen, via Release-Download (Issue #85) (#87) (#87)
- C Code Coverage CI-Integration (#88) (#88)
- Use download-tooling composite action 
- Use go-test composite action 
- Use shellcheck-sarif and c-test composite actions 
- Add explicit download-tooling step before go-test 
- Git worktree --orphan syntax für git 2.40+ 


# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Infrastruktur & Tooling

- Use container script instead of inline podman commands 
- Separate build step from run commands 
- Add export-diagram, export-table and export-png steps 
- Commit export changes back to repo if files changed 
- Update exported diagrams [skip ci] 
- Update exported diagrams [skip ci] 
- Trigger only on beaglebone_black.jsonc changes 
- Trigger SonarCloud verification 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Gruppierung nach Software-Änderungen und Infrastruktur & Tooling (#65) (#65)
- Erstelle PR statt direktem Push auf main (branch protection fix) (#66) (#66)
- Update unreleased section [skip ci] (#67) (#67)
- Update unreleased section [skip ci] (#69) (#69)
- Update unreleased section [skip ci] (#71) (#71)
- Update unreleased section [skip ci] (#73) (#73)
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] (#76) (#76)
- Add entry for Issue #31 fix (#75) [skip ci] 
- Update unreleased section [skip ci] (#78) (#78)
- Add entry for Issue #21 fix (#77) [skip ci] 
- Update unreleased section [skip ci] (#80) (#80)
- Add entry for Issue #27 fix (#79) [skip ci] 
- Update unreleased section [skip ci] (#82) (#82)
- Update unreleased section [skip ci] (#89) (#89)
- Beaglebone-tooling auf v1.1.0 aktualisieren (#90) (#90)
- Update unreleased section [skip ci] (#91) (#91)
- Bump beaglebone-tooling actions to v1.1.1 
- Update unreleased section [skip ci] (#92) (#92)
- Bump beaglebone-tooling actions to v1.1.2 

### Software-Änderungen

- Podman container script and CI workflow (#45) (#46) (#46)
- Mount model dir rw, fix export paths, add export dirs step 
- Disable git credential prompt for public repo clone 
- Bypass git credential helper for public repo clone 
- Move git clone to workflow step, script only builds image 
- Use actions/checkout to clone Bausteinsicht repo 
- Drop container approach, run binary directly in CI 
- Install draw.io CLI and use xvfb-run for PNG export 
- SonarCloud Integration für Quality Monitoring (#47) (#48) (#48)
- Remove duplicate OUTPUT env for git-cliff, increase Pages smoke-test sleep to 30s 
- Replace fixed sleep with retry loop for Pages smoke-test (max 3min) 
- Git-cliff write to temp file then prepend to CHANGELOG.md 
- Copy bb_dashboard.html to index.html for GitHub Pages 
- Start_ticket zeigt automatisch Issue-Liste bei leerem Argument (#61) (#61)
- Automatisches PR-Review mit Bot-Token-Support in start_ticket (#64) (#64)
- ShellCheck SARIF Report für SonarCloud (#55) (#68) (#68)
- Deaktiviere C/C++ SonarCloud-Analyse + verbessertes Error Reporting (#70) (#70)
- POST /api/v1/backend wechselt jetzt tatsächlich den HAL-Backend (#72) (#72)
- Trend-Cache Git-Fallback via reports-Branch (#74) (#74)
- POST-Handler geben 400 bei ungültigem JSON zurück (#75) (#75)
- HTTP-Server mit ReadTimeout/WriteTimeout/IdleTimeout (Issue #21) (#77) (#77)
- Regression Test für BME280StreamHandler Flusher nil-Check (Issue #27) (#79) (#79)
- Flag.Parse() aus Library-Package entfernt (Issue #26) (#81) (#81)
- CORS OPTIONS Preflight-Requests behandeln (Issue #22) (#83) (#83)
- Collect_results.py + statisch/dynamisch Trennung (Issue #15) (#84) (#84)
- Phase 1 — Tooling in tooling/ Ordner gruppieren (Issue #85) (#86) (#86)
- Phase 3 — tooling/ aus Repo entfernen, via Release-Download (Issue #85) (#87) (#87)
- C Code Coverage CI-Integration (#88) (#88)
- Use download-tooling composite action 
- Use go-test composite action 
- Use shellcheck-sarif and c-test composite actions 
- Add explicit download-tooling step before go-test 


# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Infrastruktur & Tooling

- Use container script instead of inline podman commands 
- Separate build step from run commands 
- Add export-diagram, export-table and export-png steps 
- Commit export changes back to repo if files changed 
- Update exported diagrams [skip ci] 
- Update exported diagrams [skip ci] 
- Trigger only on beaglebone_black.jsonc changes 
- Trigger SonarCloud verification 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Gruppierung nach Software-Änderungen und Infrastruktur & Tooling (#65) (#65)
- Erstelle PR statt direktem Push auf main (branch protection fix) (#66) (#66)
- Update unreleased section [skip ci] (#67) (#67)
- Update unreleased section [skip ci] (#69) (#69)
- Update unreleased section [skip ci] (#71) (#71)
- Update unreleased section [skip ci] (#73) (#73)
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] (#76) (#76)
- Add entry for Issue #31 fix (#75) [skip ci] 
- Update unreleased section [skip ci] (#78) (#78)
- Add entry for Issue #21 fix (#77) [skip ci] 
- Update unreleased section [skip ci] (#80) (#80)
- Add entry for Issue #27 fix (#79) [skip ci] 
- Update unreleased section [skip ci] (#82) (#82)
- Update unreleased section [skip ci] (#89) (#89)
- Beaglebone-tooling auf v1.1.0 aktualisieren (#90) (#90)
- Update unreleased section [skip ci] (#91) (#91)
- Bump beaglebone-tooling actions to v1.1.1 

### Software-Änderungen

- Podman container script and CI workflow (#45) (#46) (#46)
- Mount model dir rw, fix export paths, add export dirs step 
- Disable git credential prompt for public repo clone 
- Bypass git credential helper for public repo clone 
- Move git clone to workflow step, script only builds image 
- Use actions/checkout to clone Bausteinsicht repo 
- Drop container approach, run binary directly in CI 
- Install draw.io CLI and use xvfb-run for PNG export 
- SonarCloud Integration für Quality Monitoring (#47) (#48) (#48)
- Remove duplicate OUTPUT env for git-cliff, increase Pages smoke-test sleep to 30s 
- Replace fixed sleep with retry loop for Pages smoke-test (max 3min) 
- Git-cliff write to temp file then prepend to CHANGELOG.md 
- Copy bb_dashboard.html to index.html for GitHub Pages 
- Start_ticket zeigt automatisch Issue-Liste bei leerem Argument (#61) (#61)
- Automatisches PR-Review mit Bot-Token-Support in start_ticket (#64) (#64)
- ShellCheck SARIF Report für SonarCloud (#55) (#68) (#68)
- Deaktiviere C/C++ SonarCloud-Analyse + verbessertes Error Reporting (#70) (#70)
- POST /api/v1/backend wechselt jetzt tatsächlich den HAL-Backend (#72) (#72)
- Trend-Cache Git-Fallback via reports-Branch (#74) (#74)
- POST-Handler geben 400 bei ungültigem JSON zurück (#75) (#75)
- HTTP-Server mit ReadTimeout/WriteTimeout/IdleTimeout (Issue #21) (#77) (#77)
- Regression Test für BME280StreamHandler Flusher nil-Check (Issue #27) (#79) (#79)
- Flag.Parse() aus Library-Package entfernt (Issue #26) (#81) (#81)
- CORS OPTIONS Preflight-Requests behandeln (Issue #22) (#83) (#83)
- Collect_results.py + statisch/dynamisch Trennung (Issue #15) (#84) (#84)
- Phase 1 — Tooling in tooling/ Ordner gruppieren (Issue #85) (#86) (#86)
- Phase 3 — tooling/ aus Repo entfernen, via Release-Download (Issue #85) (#87) (#87)
- C Code Coverage CI-Integration (#88) (#88)
- Use download-tooling composite action 
- Use go-test composite action 
- Use shellcheck-sarif and c-test composite actions 


# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Infrastruktur & Tooling

- Use container script instead of inline podman commands 
- Separate build step from run commands 
- Add export-diagram, export-table and export-png steps 
- Commit export changes back to repo if files changed 
- Update exported diagrams [skip ci] 
- Update exported diagrams [skip ci] 
- Trigger only on beaglebone_black.jsonc changes 
- Trigger SonarCloud verification 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Gruppierung nach Software-Änderungen und Infrastruktur & Tooling (#65) (#65)
- Erstelle PR statt direktem Push auf main (branch protection fix) (#66) (#66)
- Update unreleased section [skip ci] (#67) (#67)
- Update unreleased section [skip ci] (#69) (#69)
- Update unreleased section [skip ci] (#71) (#71)
- Update unreleased section [skip ci] (#73) (#73)
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] (#76) (#76)
- Add entry for Issue #31 fix (#75) [skip ci] 
- Update unreleased section [skip ci] (#78) (#78)
- Add entry for Issue #21 fix (#77) [skip ci] 
- Update unreleased section [skip ci] (#80) (#80)
- Add entry for Issue #27 fix (#79) [skip ci] 
- Update unreleased section [skip ci] (#82) (#82)
- Update unreleased section [skip ci] (#89) (#89)
- Beaglebone-tooling auf v1.1.0 aktualisieren (#90) (#90)

### Software-Änderungen

- Podman container script and CI workflow (#45) (#46) (#46)
- Mount model dir rw, fix export paths, add export dirs step 
- Disable git credential prompt for public repo clone 
- Bypass git credential helper for public repo clone 
- Move git clone to workflow step, script only builds image 
- Use actions/checkout to clone Bausteinsicht repo 
- Drop container approach, run binary directly in CI 
- Install draw.io CLI and use xvfb-run for PNG export 
- SonarCloud Integration für Quality Monitoring (#47) (#48) (#48)
- Remove duplicate OUTPUT env for git-cliff, increase Pages smoke-test sleep to 30s 
- Replace fixed sleep with retry loop for Pages smoke-test (max 3min) 
- Git-cliff write to temp file then prepend to CHANGELOG.md 
- Copy bb_dashboard.html to index.html for GitHub Pages 
- Start_ticket zeigt automatisch Issue-Liste bei leerem Argument (#61) (#61)
- Automatisches PR-Review mit Bot-Token-Support in start_ticket (#64) (#64)
- ShellCheck SARIF Report für SonarCloud (#55) (#68) (#68)
- Deaktiviere C/C++ SonarCloud-Analyse + verbessertes Error Reporting (#70) (#70)
- POST /api/v1/backend wechselt jetzt tatsächlich den HAL-Backend (#72) (#72)
- Trend-Cache Git-Fallback via reports-Branch (#74) (#74)
- POST-Handler geben 400 bei ungültigem JSON zurück (#75) (#75)
- HTTP-Server mit ReadTimeout/WriteTimeout/IdleTimeout (Issue #21) (#77) (#77)
- Regression Test für BME280StreamHandler Flusher nil-Check (Issue #27) (#79) (#79)
- Flag.Parse() aus Library-Package entfernt (Issue #26) (#81) (#81)
- CORS OPTIONS Preflight-Requests behandeln (Issue #22) (#83) (#83)
- Collect_results.py + statisch/dynamisch Trennung (Issue #15) (#84) (#84)
- Phase 1 — Tooling in tooling/ Ordner gruppieren (Issue #85) (#86) (#86)
- Phase 3 — tooling/ aus Repo entfernen, via Release-Download (Issue #85) (#87) (#87)
- C Code Coverage CI-Integration (#88) (#88)


# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Infrastruktur & Tooling

- Use container script instead of inline podman commands 
- Separate build step from run commands 
- Add export-diagram, export-table and export-png steps 
- Commit export changes back to repo if files changed 
- Update exported diagrams [skip ci] 
- Update exported diagrams [skip ci] 
- Trigger only on beaglebone_black.jsonc changes 
- Trigger SonarCloud verification 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Gruppierung nach Software-Änderungen und Infrastruktur & Tooling (#65) (#65)
- Erstelle PR statt direktem Push auf main (branch protection fix) (#66) (#66)
- Update unreleased section [skip ci] (#67) (#67)
- Update unreleased section [skip ci] (#69) (#69)
- Update unreleased section [skip ci] (#71) (#71)
- Update unreleased section [skip ci] (#73) (#73)
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] (#76) (#76)
- Add entry for Issue #31 fix (#75) [skip ci] 
- Update unreleased section [skip ci] (#78) (#78)
- Add entry for Issue #21 fix (#77) [skip ci] 
- Update unreleased section [skip ci] (#80) (#80)
- Add entry for Issue #27 fix (#79) [skip ci] 
- Update unreleased section [skip ci] (#82) (#82)

### Software-Änderungen

- Podman container script and CI workflow (#45) (#46) (#46)
- Mount model dir rw, fix export paths, add export dirs step 
- Disable git credential prompt for public repo clone 
- Bypass git credential helper for public repo clone 
- Move git clone to workflow step, script only builds image 
- Use actions/checkout to clone Bausteinsicht repo 
- Drop container approach, run binary directly in CI 
- Install draw.io CLI and use xvfb-run for PNG export 
- SonarCloud Integration für Quality Monitoring (#47) (#48) (#48)
- Remove duplicate OUTPUT env for git-cliff, increase Pages smoke-test sleep to 30s 
- Replace fixed sleep with retry loop for Pages smoke-test (max 3min) 
- Git-cliff write to temp file then prepend to CHANGELOG.md 
- Copy bb_dashboard.html to index.html for GitHub Pages 
- Start_ticket zeigt automatisch Issue-Liste bei leerem Argument (#61) (#61)
- Automatisches PR-Review mit Bot-Token-Support in start_ticket (#64) (#64)
- ShellCheck SARIF Report für SonarCloud (#55) (#68) (#68)
- Deaktiviere C/C++ SonarCloud-Analyse + verbessertes Error Reporting (#70) (#70)
- POST /api/v1/backend wechselt jetzt tatsächlich den HAL-Backend (#72) (#72)
- Trend-Cache Git-Fallback via reports-Branch (#74) (#74)
- POST-Handler geben 400 bei ungültigem JSON zurück (#75) (#75)
- HTTP-Server mit ReadTimeout/WriteTimeout/IdleTimeout (Issue #21) (#77) (#77)
- Regression Test für BME280StreamHandler Flusher nil-Check (Issue #27) (#79) (#79)
- Flag.Parse() aus Library-Package entfernt (Issue #26) (#81) (#81)
- CORS OPTIONS Preflight-Requests behandeln (Issue #22) (#83) (#83)
- Collect_results.py + statisch/dynamisch Trennung (Issue #15) (#84) (#84)
- Phase 1 — Tooling in tooling/ Ordner gruppieren (Issue #85) (#86) (#86)
- Phase 3 — tooling/ aus Repo entfernen, via Release-Download (Issue #85) (#87) (#87)
- C Code Coverage CI-Integration (#88) (#88)


# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Infrastruktur & Tooling

- refactor(tooling): Phase 3 — tooling/ aus Repo entfernt, beaglebone-tooling Release-Download in CI (Issue #85) (#87)
- refactor(tooling): Phase 2 — eigenes Repo paulefl/beaglebone-tooling mit Requirements, Tests und Release v1.0.0 (Issue #85)
- refactor(tooling): Phase 1 — Tooling in tooling/ Ordner gruppieren, Code/Tooling-Trennung vorbereitet (Issue #85) (#86)
- fix(reports): Dashboard zeigt ❓ für 27 Tests — collect_results.py implementiert, static/dynamic JSON getrennt (Issue #15) (#84)
- Use container script instead of inline podman commands 
- Separate build step from run commands 
- Add export-diagram, export-table and export-png steps 
- Commit export changes back to repo if files changed 
- Update exported diagrams [skip ci] 
- Update exported diagrams [skip ci] 
- Trigger only on beaglebone_black.jsonc changes 
- Trigger SonarCloud verification 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Gruppierung nach Software-Änderungen und Infrastruktur & Tooling (#65) (#65)
- Erstelle PR statt direktem Push auf main (branch protection fix) (#66) (#66)
- Update unreleased section [skip ci] (#67) (#67)
- Update unreleased section [skip ci] (#69) (#69)
- Update unreleased section [skip ci] (#71) (#71)
- Update unreleased section [skip ci] (#73) (#73)
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] (#76) (#76)
- Add entry for Issue #31 fix (#75) [skip ci] 
- Update unreleased section [skip ci] (#78) (#78)
- Add entry for Issue #21 fix (#77) [skip ci] 
- Update unreleased section [skip ci] (#80) (#80)
- Add entry for Issue #27 fix (#79) [skip ci] 

### Software-Änderungen

- Podman container script and CI workflow (#45) (#46) (#46)
- Mount model dir rw, fix export paths, add export dirs step 
- Disable git credential prompt for public repo clone 
- Bypass git credential helper for public repo clone 
- Move git clone to workflow step, script only builds image 
- Use actions/checkout to clone Bausteinsicht repo 
- Drop container approach, run binary directly in CI 
- Install draw.io CLI and use xvfb-run for PNG export 
- SonarCloud Integration für Quality Monitoring (#47) (#48) (#48)
- Remove duplicate OUTPUT env for git-cliff, increase Pages smoke-test sleep to 30s 
- Replace fixed sleep with retry loop for Pages smoke-test (max 3min) 
- Git-cliff write to temp file then prepend to CHANGELOG.md 
- Copy bb_dashboard.html to index.html for GitHub Pages 
- Start_ticket zeigt automatisch Issue-Liste bei leerem Argument (#61) (#61)
- Automatisches PR-Review mit Bot-Token-Support in start_ticket (#64) (#64)
- ShellCheck SARIF Report für SonarCloud (#55) (#68) (#68)
- Deaktiviere C/C++ SonarCloud-Analyse + verbessertes Error Reporting (#70) (#70)
- POST /api/v1/backend wechselt jetzt tatsächlich den HAL-Backend (#72) (#72)
- Trend-Cache Git-Fallback via reports-Branch (#74) (#74)
- POST-Handler geben 400 bei ungültigem JSON zurück (#75) (#75)
- HTTP-Server mit ReadTimeout/WriteTimeout/IdleTimeout (Issue #21) (#77) (#77)
- Regression Test für BME280StreamHandler Flusher nil-Check (Issue #27) (#79) (#79)
- Flag.Parse() aus Library-Package entfernt (Issue #26) (#81) (#81)
- CORS OPTIONS Preflight-Requests behandeln — CORSMiddleware als zentraler Wrapper (Issue #22) (#83) (#83)


# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Infrastruktur & Tooling

- Use container script instead of inline podman commands 
- Separate build step from run commands 
- Add export-diagram, export-table and export-png steps 
- Commit export changes back to repo if files changed 
- Update exported diagrams [skip ci] 
- Update exported diagrams [skip ci] 
- Trigger only on beaglebone_black.jsonc changes 
- Trigger SonarCloud verification 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Gruppierung nach Software-Änderungen und Infrastruktur & Tooling (#65) (#65)
- Erstelle PR statt direktem Push auf main (branch protection fix) (#66) (#66)
- Update unreleased section [skip ci] (#67) (#67)
- Update unreleased section [skip ci] (#69) (#69)
- Update unreleased section [skip ci] (#71) (#71)
- Update unreleased section [skip ci] (#73) (#73)
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] (#76) (#76)
- Add entry for Issue #31 fix (#75) [skip ci] 
- Update unreleased section [skip ci] (#78) (#78)
- Add entry for Issue #21 fix (#77) [skip ci] 

### Software-Änderungen

- Podman container script and CI workflow (#45) (#46) (#46)
- Mount model dir rw, fix export paths, add export dirs step 
- Disable git credential prompt for public repo clone 
- Bypass git credential helper for public repo clone 
- Move git clone to workflow step, script only builds image 
- Use actions/checkout to clone Bausteinsicht repo 
- Drop container approach, run binary directly in CI 
- Install draw.io CLI and use xvfb-run for PNG export 
- SonarCloud Integration für Quality Monitoring (#47) (#48) (#48)
- Remove duplicate OUTPUT env for git-cliff, increase Pages smoke-test sleep to 30s 
- Replace fixed sleep with retry loop for Pages smoke-test (max 3min) 
- Git-cliff write to temp file then prepend to CHANGELOG.md 
- Copy bb_dashboard.html to index.html for GitHub Pages 
- Start_ticket zeigt automatisch Issue-Liste bei leerem Argument (#61) (#61)
- Automatisches PR-Review mit Bot-Token-Support in start_ticket (#64) (#64)
- ShellCheck SARIF Report für SonarCloud (#55) (#68) (#68)
- Deaktiviere C/C++ SonarCloud-Analyse + verbessertes Error Reporting (#70) (#70)
- POST /api/v1/backend wechselt jetzt tatsächlich den HAL-Backend (#72) (#72)
- Trend-Cache Git-Fallback via reports-Branch (#74) (#74)
- POST-Handler geben 400 bei ungültigem JSON zurück (#75) (#75)
- HTTP-Server mit ReadTimeout/WriteTimeout/IdleTimeout (Issue #21) (#77) (#77)
- Regression Test für BME280StreamHandler Flusher nil-Check (Issue #27) (#79) (#79)


# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Infrastruktur & Tooling

- Use container script instead of inline podman commands 
- Separate build step from run commands 
- Add export-diagram, export-table and export-png steps 
- Commit export changes back to repo if files changed 
- Update exported diagrams [skip ci] 
- Update exported diagrams [skip ci] 
- Trigger only on beaglebone_black.jsonc changes 
- Trigger SonarCloud verification 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Gruppierung nach Software-Änderungen und Infrastruktur & Tooling (#65) (#65)
- Erstelle PR statt direktem Push auf main (branch protection fix) (#66) (#66)
- Update unreleased section [skip ci] (#67) (#67)
- Update unreleased section [skip ci] (#69) (#69)
- Update unreleased section [skip ci] (#71) (#71)
- Update unreleased section [skip ci] (#73) (#73)
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] (#76) (#76)
- Add entry for Issue #31 fix (#75) [skip ci] 

### Software-Änderungen

- Podman container script and CI workflow (#45) (#46) (#46)
- Mount model dir rw, fix export paths, add export dirs step 
- Disable git credential prompt for public repo clone 
- Bypass git credential helper for public repo clone 
- Move git clone to workflow step, script only builds image 
- Use actions/checkout to clone Bausteinsicht repo 
- Drop container approach, run binary directly in CI 
- Install draw.io CLI and use xvfb-run for PNG export 
- SonarCloud Integration für Quality Monitoring (#47) (#48) (#48)
- Remove duplicate OUTPUT env for git-cliff, increase Pages smoke-test sleep to 30s 
- Replace fixed sleep with retry loop for Pages smoke-test (max 3min) 
- Git-cliff write to temp file then prepend to CHANGELOG.md 
- Copy bb_dashboard.html to index.html for GitHub Pages 
- Start_ticket zeigt automatisch Issue-Liste bei leerem Argument (#61) (#61)
- Automatisches PR-Review mit Bot-Token-Support in start_ticket (#64) (#64)
- ShellCheck SARIF Report für SonarCloud (#55) (#68) (#68)
- Deaktiviere C/C++ SonarCloud-Analyse + verbessertes Error Reporting (#70) (#70)
- POST /api/v1/backend wechselt jetzt tatsächlich den HAL-Backend (#72) (#72)
- Trend-Cache Git-Fallback via reports-Branch (#74) (#74)
- POST-Handler geben 400 bei ungültigem JSON zurück (#75) (#75)
- HTTP-Server mit ReadTimeout/WriteTimeout/IdleTimeout (Issue #21) (#77) (#77)
- BME280StreamHandler Flusher nil-Check Regression Test + REQ SWR-007 (#79) (#79)


# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Infrastruktur & Tooling

- Use container script instead of inline podman commands 
- Separate build step from run commands 
- Add export-diagram, export-table and export-png steps 
- Commit export changes back to repo if files changed 
- Update exported diagrams [skip ci] 
- Update exported diagrams [skip ci] 
- Trigger only on beaglebone_black.jsonc changes 
- Trigger SonarCloud verification 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Gruppierung nach Software-Änderungen und Infrastruktur & Tooling (#65) (#65)
- Erstelle PR statt direktem Push auf main (branch protection fix) (#66) (#66)
- Update unreleased section [skip ci] (#67) (#67)
- Update unreleased section [skip ci] (#69) (#69)
- Update unreleased section [skip ci] (#71) (#71)
- Update unreleased section [skip ci] (#73) (#73)
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 

### Software-Änderungen

- Podman container script and CI workflow (#45) (#46) (#46)
- Mount model dir rw, fix export paths, add export dirs step 
- Disable git credential prompt for public repo clone 
- Bypass git credential helper for public repo clone 
- Move git clone to workflow step, script only builds image 
- Use actions/checkout to clone Bausteinsicht repo 
- Drop container approach, run binary directly in CI 
- Install draw.io CLI and use xvfb-run for PNG export 
- SonarCloud Integration für Quality Monitoring (#47) (#48) (#48)
- Remove duplicate OUTPUT env for git-cliff, increase Pages smoke-test sleep to 30s 
- Replace fixed sleep with retry loop for Pages smoke-test (max 3min) 
- Git-cliff write to temp file then prepend to CHANGELOG.md 
- Copy bb_dashboard.html to index.html for GitHub Pages 
- Start_ticket zeigt automatisch Issue-Liste bei leerem Argument (#61) (#61)
- Automatisches PR-Review mit Bot-Token-Support in start_ticket (#64) (#64)
- ShellCheck SARIF Report für SonarCloud (#55) (#68) (#68)
- Deaktiviere C/C++ SonarCloud-Analyse + verbessertes Error Reporting (#70) (#70)
- POST /api/v1/backend wechselt jetzt tatsächlich den HAL-Backend (#72) (#72)
- Trend-Cache Git-Fallback via reports-Branch (#74) (#74)
- POST-Handler geben 400 bei ungültigem JSON zurück (#75) (#75)
- HTTP-Server mit ReadTimeout/WriteTimeout/IdleTimeout gegen Ressourcenerschöpfung (#77) (#77)


# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Infrastruktur & Tooling

- Use container script instead of inline podman commands 
- Separate build step from run commands 
- Add export-diagram, export-table and export-png steps 
- Commit export changes back to repo if files changed 
- Update exported diagrams [skip ci] 
- Update exported diagrams [skip ci] 
- Trigger only on beaglebone_black.jsonc changes 
- Trigger SonarCloud verification 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Gruppierung nach Software-Änderungen und Infrastruktur & Tooling (#65) (#65)
- Erstelle PR statt direktem Push auf main (branch protection fix) (#66) (#66)
- Update unreleased section [skip ci] (#67) (#67)
- Update unreleased section [skip ci] (#69) (#69)
- Update unreleased section [skip ci] (#71) (#71)

### Software-Änderungen

- Podman container script and CI workflow (#45) (#46) (#46)
- Mount model dir rw, fix export paths, add export dirs step 
- Disable git credential prompt for public repo clone 
- Bypass git credential helper for public repo clone 
- Move git clone to workflow step, script only builds image 
- Use actions/checkout to clone Bausteinsicht repo 
- Drop container approach, run binary directly in CI 
- Install draw.io CLI and use xvfb-run for PNG export 
- SonarCloud Integration für Quality Monitoring (#47) (#48) (#48)
- Remove duplicate OUTPUT env for git-cliff, increase Pages smoke-test sleep to 30s 
- Replace fixed sleep with retry loop for Pages smoke-test (max 3min) 
- Git-cliff write to temp file then prepend to CHANGELOG.md 
- Copy bb_dashboard.html to index.html for GitHub Pages 
- Start_ticket zeigt automatisch Issue-Liste bei leerem Argument (#61) (#61)
- Automatisches PR-Review mit Bot-Token-Support in start_ticket (#64) (#64)
- ShellCheck SARIF Report für SonarCloud (#55) (#68) (#68)
- Deaktiviere C/C++ SonarCloud-Analyse + verbessertes Error Reporting (#70) (#70)
- POST /api/v1/backend wechselt jetzt tatsächlich den HAL-Backend (#72) (#72)
- fix(api): POST-Handler geben HTTP 400 bei ungültigem JSON zurück, REQ HW-API-007 (#75) (#75)


# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Infrastruktur & Tooling

- Use container script instead of inline podman commands 
- Separate build step from run commands 
- Add export-diagram, export-table and export-png steps 
- Commit export changes back to repo if files changed 
- Update exported diagrams [skip ci] 
- Update exported diagrams [skip ci] 
- Trigger only on beaglebone_black.jsonc changes 
- Trigger SonarCloud verification 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Gruppierung nach Software-Änderungen und Infrastruktur & Tooling (#65) (#65)
- Erstelle PR statt direktem Push auf main (branch protection fix) (#66) (#66)
- Update unreleased section [skip ci] (#67) (#67)
- Update unreleased section [skip ci] (#69) (#69)

### Software-Änderungen

- Podman container script and CI workflow (#45) (#46) (#46)
- Mount model dir rw, fix export paths, add export dirs step 
- Disable git credential prompt for public repo clone 
- Bypass git credential helper for public repo clone 
- Move git clone to workflow step, script only builds image 
- Use actions/checkout to clone Bausteinsicht repo 
- Drop container approach, run binary directly in CI 
- Install draw.io CLI and use xvfb-run for PNG export 
- SonarCloud Integration für Quality Monitoring (#47) (#48) (#48)
- Remove duplicate OUTPUT env for git-cliff, increase Pages smoke-test sleep to 30s 
- Replace fixed sleep with retry loop for Pages smoke-test (max 3min) 
- Git-cliff write to temp file then prepend to CHANGELOG.md 
- Copy bb_dashboard.html to index.html for GitHub Pages 
- Start_ticket zeigt automatisch Issue-Liste bei leerem Argument (#61) (#61)
- Automatisches PR-Review mit Bot-Token-Support in start_ticket (#64) (#64)
- ShellCheck SARIF Report für SonarCloud (#55) (#68) (#68)
- Deaktiviere C/C++ SonarCloud-Analyse + verbessertes Error Reporting (#70) (#70)
- fix(api): POST /api/v1/backend wechselt jetzt tatsächlich den HAL-Backend (#72)
- fix(ci): Trend-Cache Git-Fallback via reports-Branch (#74)


# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Infrastruktur & Tooling

- Use container script instead of inline podman commands 
- Separate build step from run commands 
- Add export-diagram, export-table and export-png steps 
- Commit export changes back to repo if files changed 
- Update exported diagrams [skip ci] 
- Update exported diagrams [skip ci] 
- Trigger only on beaglebone_black.jsonc changes 
- Trigger SonarCloud verification 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Gruppierung nach Software-Änderungen und Infrastruktur & Tooling (#65) (#65)
- Erstelle PR statt direktem Push auf main (branch protection fix) (#66) (#66)
- Update unreleased section [skip ci] (#67) (#67)

### Software-Änderungen

- Podman container script and CI workflow (#45) (#46) (#46)
- Mount model dir rw, fix export paths, add export dirs step 
- Disable git credential prompt for public repo clone 
- Bypass git credential helper for public repo clone 
- Move git clone to workflow step, script only builds image 
- Use actions/checkout to clone Bausteinsicht repo 
- Drop container approach, run binary directly in CI 
- Install draw.io CLI and use xvfb-run for PNG export 
- SonarCloud Integration für Quality Monitoring (#47) (#48) (#48)
- Remove duplicate OUTPUT env for git-cliff, increase Pages smoke-test sleep to 30s 
- Replace fixed sleep with retry loop for Pages smoke-test (max 3min) 
- Git-cliff write to temp file then prepend to CHANGELOG.md 
- Copy bb_dashboard.html to index.html for GitHub Pages 
- Start_ticket zeigt automatisch Issue-Liste bei leerem Argument (#61) (#61)
- Automatisches PR-Review mit Bot-Token-Support in start_ticket (#64) (#64)
- ShellCheck SARIF Report für SonarCloud (#55) (#68) (#68)


# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Infrastruktur & Tooling

- Use container script instead of inline podman commands 
- Separate build step from run commands 
- Add export-diagram, export-table and export-png steps 
- Commit export changes back to repo if files changed 
- Update exported diagrams [skip ci] 
- Update exported diagrams [skip ci] 
- Trigger only on beaglebone_black.jsonc changes 
- Trigger SonarCloud verification 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Update unreleased section [skip ci] 
- Gruppierung nach Software-Änderungen und Infrastruktur & Tooling (#65) (#65)
- Erstelle PR statt direktem Push auf main (branch protection fix) (#66) (#66)

### Software-Änderungen

- Podman container script and CI workflow (#45) (#46) (#46)
- Mount model dir rw, fix export paths, add export dirs step 
- Disable git credential prompt for public repo clone 
- Bypass git credential helper for public repo clone 
- Move git clone to workflow step, script only builds image 
- Use actions/checkout to clone Bausteinsicht repo 
- Drop container approach, run binary directly in CI 
- Install draw.io CLI and use xvfb-run for PNG export 
- SonarCloud Integration für Quality Monitoring (#47) (#48) (#48)
- Remove duplicate OUTPUT env for git-cliff, increase Pages smoke-test sleep to 30s 
- Replace fixed sleep with retry loop for Pages smoke-test (max 3min) 
- Git-cliff write to temp file then prepend to CHANGELOG.md 
- Copy bb_dashboard.html to index.html for GitHub Pages 
- Start_ticket zeigt automatisch Issue-Liste bei leerem Argument (#61) (#61)
- Automatisches PR-Review mit Bot-Token-Support in start_ticket (#64) (#64)


# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Software-Änderungen

- Podman container script and CI workflow (#45) (#46)
- SonarCloud Integration für Quality Monitoring (#47) (#48)
- start_ticket Skill zeigt automatisch nummerierte Issue-Liste bei leerem Argument (#59)
- start_ticket automatisches PR-Review nach CI: Diff-Analyse, Findings-Klassifizierung, Bot-Token-Support für Approval (#62)
- Mount model dir rw, fix export paths, add export dirs step
- Drop container approach, run binary directly in CI
- Install draw.io CLI and use xvfb-run for PNG export
- Remove duplicate OUTPUT env for git-cliff, increase Pages smoke-test sleep to 30s
- Replace fixed sleep with retry loop for Pages smoke-test (max 3min)
- Git-cliff write to temp file then prepend to CHANGELOG.md
- Copy bb_dashboard.html to index.html for GitHub Pages

### Infrastruktur & Tooling

- Use container script instead of inline podman commands
- Separate build step from run commands
- Add export-diagram, export-table and export-png steps
- Commit export changes back to repo if files changed
- Trigger only on beaglebone_black.jsonc changes
- Trigger SonarCloud verification
- Update unreleased section [skip ci]
- Gruppiere Changelog nach Software-Änderungen und Infrastruktur & Tooling (#60)

---

> **Version source of truth:** [`Makefile`](Makefile) — `VERSION` variable.
> The version is only bumped manually when an official GitHub Release (git tag) is created.

---

## [1.1.0] — unreleased (next)

### Added
- SonarCloud Integration: `sonar-project.properties`, Go JUnit XML + Cobertura Coverage, Python JUnit XML + Coverage XML, `sonarcloud` CI Job (#47)
- Bausteinsicht via Podman Container: `scripts/bausteinsicht-container.sh` + CI Workflow `bausteinsicht.yml` (#45)
- GitHub Pages Smoke-Test nach Deploy — prüft HTTP 200 auf Pages-URL (#40)
- Automatisierter Release-Workflow via `workflow_dispatch` mit bump-Input (patch/minor/major) (#43)
- BME280 Hardware-Spec als Markdown: Bosch Datasheet BST-BME280-DS001 rev 1.24 (10 Dateien) + SeenGreat Modul-Doku mit BeagleBone Black Verdrahtung (#39)
- BeagleBone Black Hardware-Spec als Markdown (11 Kapitel) aus offizieller Dokumentation (#37)
- StrictDoc Requirements Management mit Custom Grammar: `SYS_REQUIREMENT`, `SW_REQUIREMENT`, `HW_REQUIREMENT`, `SOURCE_CODE`, `TEST_CASE` (#33)
- StrictDoc Exporte: HTML, PDF (html2pdf), Excel, ReqIF — deployed auf GitHub Pages
- Pytest JUnit XML Integration für StrictDoc Traceability
- Setup-Labels Workflow für reproduzierbare GitHub-Label-Konfiguration
- Automatisiertes Changelog-Handling mit Keep a Changelog Standard (#41)
- `cliff.toml` Konfiguration für `git-cliff` nach Conventional Commits
- CI: `git-cliff` generiert `[Unreleased]`-Section automatisch bei Merge auf `main`
- `VERSION` Variable im Makefile als zentrale Versionsquelle

### Fixed
- Hardcodierter Fallback-Pfad `/home/claude/` in `generate_reports.py` entfernt (#34)
- StrictDoc GitHub Pages URL korrigiert (`output/strictdoc/html/`)
- StrictDoc PDF-Ausgabepfad (`html2pdf/` statt `pdf/`)
- `continue-on-error` für optionale StrictDoc-Artefakt-Downloads hinzugefügt
- Source-Traceability auf relevante Verzeichnisse begrenzt (`go-api/`, `c-lib/`, `project/rust-lib/`, `tests/`)
- `Makefile` zu StrictDoc `include_source_paths` hinzugefügt (SYS-005)

### CI
- `report`-Job: Abhängigkeit auf `build-cli` ergänzt
- `download-artifact` Version auf v8 vereinheitlicht

---

## [1.0.0] — 2026-03-17

### Added
- **HAL Layer**: C + Rust Libraries mit automatischem Backend-Fallback (`HW_BACKEND=auto/c/rust`)
- **REST API**: Go Server auf Port 5000 mit Endpoints für BME280, GPIO, UART, SPI
- **BME280**: Vollständiger Bosch Kompensationsalgorithmus (Temperatur, Luftdruck, Luftfeuchtigkeit)
- **HAL Interface**: Einheitliches Go Interface (`HardwareDriver`) für C, Rust und Mock Backend
- **Mock Driver**: Fehler-Injektion und Call-Tracking für Hardware-unabhängige Unit Tests
- **CLI (bbcli)**: Cobra CLI mit Shell Completion (Bash/Zsh/Fish), Cross-Compilation für linux/arm7
- **TUI (bbtui)**: BubbleTea Terminal UI
- **Desktop GUI (bbgui)**: Fyne Desktop Applikation
- **Web GUI**: HTML/JS Dashboard mit SSE Live-Updates
- **Test Report Dashboard**: HTML Dashboard mit Testergebnissen, Coverage und Pass-Rate
- **Trend-Tracking**: GitHub Actions Workflow Summary mit historischem Verlauf
- **Quality Gates**: Automatische Schwellenwertprüfung (≥90% Pass-Rate, ≥75% Coverage)
- **Bausteinsicht**: Architektur-Modell als JSONC + exportierte Bilder
- **CLAUDE.md**: Projektdokumentation für Claude Code

### Fixed
- Go HAL: Import-Zyklus zwischen `pkg/hal` und `pkg/hal/c` behoben
- Go Unit Tests: Race condition fixes, Coverage verbessert
- Test-Ergebnis-Status (`outcome_icon`) für Go-Tests korrigiert
- Go Version auf 1.23 angehoben

### Dependencies
- Dependabot: `actions/setup-go@6`, `actions/upload-artifact@7`, `actions/download-artifact@8`, `codecov/codecov-action@5`
- Dependabot: `fyne.io/fyne/v2` → 2.7.3, `github.com/spf13/viper` → 1.21.0, `github.com/spf13/cobra` aktualisiert

---

## Version Format

`MAJOR.MINOR.PATCH`

- **MAJOR**: Breaking Changes
- **MINOR**: Neue Features (abwärtskompatibel)
- **PATCH**: Bugfixes

[Unreleased]: https://github.com/paulefl/beaglebone_black/compare/v1.0.0...HEAD
[1.1.0]: https://github.com/paulefl/beaglebone_black/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/paulefl/beaglebone_black/releases/tag/v1.0.0