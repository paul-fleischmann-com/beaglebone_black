# TODO: Offene Punkte zu #271 (hardware-freie E2E-ACF-CAN-Verifikation)

Issue: [#271 test(demo): Lokale/CI-Verifikation der E2E-ACF-CAN-Kette (#270) ohne physisches Board](https://github.com/paul-fleischmann-com/beaglebone_black/issues/271)

## Stand
Die Umsetzung ist im Repo vorhanden. Es fehlt nur die Bestätigung, dass die CI-Pipeline auf `main` grün läuft.

| Was | Wo | Status |
|---|---|---|
| Test mit 5 Namespaces, `veth`/`vxcan`, Mock-HAL für D5, Teardown, `candump`/`tcpdump`-Mitschnitt | `tests/integration/test_e2e_local.py` (PR #274) | gemerged |
| `integration` von der BEAGLE_HOST-Skip-Regel ausgenommen | `tests/conftest.py` (PR #274) | gemerged |
| Privilegierte Drone-Pipeline `e2e-demo-local-test` | `.drone.yml` (PR #274) | gemerged |
| Fix: `set -e`, `modprobe`-Guard, Debian-trixie-Image | #276 | geschlossen |
| Zusatzschritt: `TestConnSendReceiveRoundtrip` mit `vcan0` | `.drone.yml`, `pkg/e2edemo/cansock_test.go` (PR #301, #280) | gemerged, Lauf nicht bestätigt |

## Offene Schritte

### 1. Drone-Lauf auf `main` prüfen
Drone-UI → Repository → Pipeline `e2e-demo-local-test` → letzten Build auf `main`.
Die Pipeline läuft nur bei Änderungen an den Pfaden aus `.drone.yml` (`project/go-api/pkg/e2edemo/**`, `cmd/can-hal-bridge/**`, `cmd/rest-can-gateway/**`, `pkg/hal/mock/**`, `tests/integration/test_e2e_local.py`, `tests/conftest.py`, `scripts/build_acfcan_native.sh`, `scripts/setup_open1722.sh`, `.drone.yml`). Seit PR #301 (`.drone.yml` geändert) sollte ein Build existieren.

- [ ] Es gibt einen Build für den Merge von PR #301 (oder du startest einen manuell: Build → *Restart* bzw. *Custom Build* auf `main`)
- [ ] Step `test-e2e-local` ist grün

### 2. Log von `test-e2e-local` auswerten
- [ ] `build_acfcan_native.sh` hat `acfcan.ko` gebaut (keine Fehler bei den Kernel-Headers)
- [ ] `modprobe vcan` und `ip link add dev vcan0 type vcan` laufen ohne Fehler (neu seit #301, bisher unbestätigt)
- [ ] Die Zeile `--- PASS: TestConnSendReceiveRoundtrip` erscheint (ein Skip lässt den Step rot werden)
- [ ] Der Python-Test `test_temperatur_kommt_exakt_ueber_die_gesamte_kette_zurueck` ist `PASSED`
- [ ] Im Log (mit `-s`) sind die `candump`- und `tcpdump`-Mitschnitte sichtbar

### 3. Falls der Lauf rot ist
| Symptom | Wahrscheinliche Ursache | Maßnahme |
|---|---|---|
| `modprobe: FATAL: Module vcan not found` | Kernel des Runners ohne `vcan` oder `/lib/modules` nicht im Container | Hinweis im Issue #280/#301 ergänzen; `vcan`-Schritt per `|| echo` überspringen oder auf `vxcan` umstellen |
| `ip: RTNETLINK answers: Operation not permitted` | Step läuft nicht `privileged` | `privileged: true` für `test-e2e-local` prüfen |
| `build_acfcan_native.sh` schlägt fehl | Kernel-Headers des Runner-Hosts nicht installierbar | Siehe #276 und `scripts/build_acfcan_native.sh` |
| Test wird geskippt | `acfcan.ko`, `can-hal-bridge-native` oder `rest-can-gateway-native` fehlt | Build-Schritte im CMD-Block prüfen |
| Timeout im Round-Trip | Gateway/Bridge oder Tunnel startet nicht | D2-/D5-Logs im Testoutput lesen |

### 4. Abschluss
- [ ] Ist der Lauf grün: #271 mit Verweis auf PR #274, #276 und #301 schließen
- [ ] Danach diese Datei löschen

## Nicht Teil von #271
- Verifikation auf dem echten BeagleBone Black (echter I2C-Sensor, echtes `acfcan` auf dem BBB-Kernel): **#273**
- Der Test beweist nicht das Verhalten des BBB-Kernels oder -Treibers. Das steht auch im Docstring von `tests/integration/test_e2e_local.py`.
