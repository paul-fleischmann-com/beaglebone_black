# TODO: Drone-Secret `beagle_host` setzen (Issue #285)

Issue: [#285 fix(ci): nightly-hardware-regression hat keinen BEAGLE_HOST](https://github.com/paul-fleischmann-com/beaglebone_black/issues/285)

## Problem
Die Pipeline `nightly-hardware-regression` (`.drone.yml`, Step `test-all-backends`) setzt

```yaml
environment:
  BEAGLE_HOST: {from_secret: beagle_host}
```

Das Drone-Secret `beagle_host` ist im Repo nicht oder leer konfiguriert. Drone setzt die Variable dann als leeren String. `tests/conftest.py` erkennt `BEAGLE_HOST` als „explizit gesetzt“, findet den Host unter Port 5000 nicht und bricht ab:

```
! _pytest.outcomes.Exit: BEAGLE_HOST= gesetzt aber nicht erreichbar (Port 5000) !
```

Das Verhalten des Testframeworks ist korrekt. Ein Code-Fix ist nicht nötig, es fehlt die Konfiguration in Drone.

## Schritte

### 1. Erreichbare Adresse des BeagleBone Black bestimmen
Der Drone-Runner (Container auf dem Build-Host) muss das BBB über das Netzwerk erreichen. `192.168.7.2` (USB-Netz) gilt nur für den direkt angeschlossenen Rechner und ist für Drone meist nicht nutzbar.

- [ ] BBB per Ethernet ins LAN hängen
- [ ] IP-Adresse feststellen: `ssh debian@192.168.7.2 "ip -4 addr show eth0"` (oder am Router nachsehen)
- [ ] Besser: feste IP oder DHCP-Reservierung im Router eintragen, damit sich die Adresse nicht ändert

### 2. Vom Drone-Host aus testen
Auf dem Rechner, auf dem der Drone-Runner läuft:

- [ ] `ping <BBB-IP>`
- [ ] `curl http://<BBB-IP>:5000/api/v1/health` (REST-API muss laufen; Pfad bei Bedarf an die aktuelle API anpassen)
- [ ] Falls kein Dienst läuft: auf dem BBB `systemctl status embedded-sw`, ggf. neu starten

### 3. Secret in Drone anlegen
Drone-UI → Repository `paul-fleischmann-com/beaglebone_black` → **Settings → Secrets → New Secret**

- [ ] Name: `beagle_host`
- [ ] Wert: IP oder Hostname aus Schritt 1 (ohne `http://`, ohne Port)
- [ ] Optional: *Allow Pull Requests* nur aktivieren, wenn nötig (Secrets sind dann für PR-Builds sichtbar)

Alternativ per CLI: `drone secret add --repository paul-fleischmann-com/beaglebone_black --name beagle_host --data <BBB-IP>`

### 4. Weitere Secrets prüfen (SSH-basierte Hardware-Tests)
Einige Tests unter `tests/hardware/` arbeiten per SSH (z. B. `test_uart.py`, `test_acfcan.py`). Dafür sind weitere Secrets nötig. Prüfen, ob sie gesetzt sind:

- [ ] `beagle_user` (z. B. `debian`)
- [ ] `ssh_key_bbb` (privater SSH-Schlüssel, dessen öffentlicher Teil in `~/.ssh/authorized_keys` auf dem BBB steht)

Hinweis: Der Step `test-all-backends` reicht bisher nur `BEAGLE_HOST` an die Tests durch. Falls die SSH-Tests im Nachtlauf laufen sollen, müssen `beagle_user` und `ssh_key_bbb` zusätzlich im `environment` des Steps in `.drone.yml` eingetragen und im Test auswertbar sein. Das ist ein eigener Code-Schritt und im Issue nicht enthalten.

Verwandte Lücken: #279 (`deploy_host`/`deploy_user`/`ssh_key` für den Dashboard-Deploy) und das fehlende `git_token` bei `push-exports`.

### 5. Pipeline testen
- [ ] Drone-UI → Repository → **Cron** → Job `nightly` → **Run now** (oder Build manuell neu starten)
- [ ] Log von `test-all-backends` prüfen: Es darf nicht mehr `BEAGLE_HOST= gesetzt aber nicht erreichbar` erscheinen
- [ ] Die Backends `c`, `rust`, `auto` laufen nacheinander (`HW_BACKEND=<b> pytest tests/hardware/ -v --timeout=60`)

### 6. Abschließen
- [ ] Nächtlichen Lauf (02:00) abwarten und Ergebnis prüfen
- [ ] Bei grünem Lauf Issue #285 schließen und diese Datei löschen oder nach `docs/` überführen

## Fehlerbilder
| Meldung | Ursache |
|---|---|
| `BEAGLE_HOST= gesetzt aber nicht erreichbar` | Secret fehlt oder ist leer |
| `BEAGLE_HOST=<ip> gesetzt aber nicht erreichbar (Port 5000)` | IP falsch, BBB aus, REST-API läuft nicht oder Firewall |
| SSH-Tests schlagen fehl, REST-Tests laufen | `beagle_user`/`ssh_key_bbb` fehlen oder sind nicht an den Step durchgereicht |
