# TODO: Dashboard-Deploy prüfen und #279 abschließen

Issue: [#279 fix(ci): Dashboard-Deploy (upload-dashboard/unzip-dashboard) hat keine SSH-Zugangsdaten](https://github.com/paul-fleischmann-com/beaglebone_black/issues/279)

## Problem
In der Pipeline `centralized-reporting` (`.drone.yml`) fehlten die SSH-Zugangsdaten für zwei Steps:

| Step | Image | Fehler (Build 12) |
|---|---|---|
| `upload-dashboard` | `appleboy/drone-scp` | `can't connect without a private SSH key or password` |
| `unzip-dashboard` | `appleboy/drone-ssh` | `missing server host` |

Beide Steps lesen drei Drone-Secrets:

```yaml
settings:
  host:     {from_secret: deploy_host}
  username: {from_secret: deploy_user}
  key:      {from_secret: ssh_key}
```

Die Secrets waren auf dem Drone-Server nicht (oder leer) gesetzt. Es ist kein Code-Problem. Laut Kommentar im Issue sind `deploy_host`, `deploy_user` und `ssh_key` inzwischen gesetzt. Was noch fehlt, ist die Bestätigung durch einen grünen Build.

## Schritte

### 1. Build prüfen
Drone-UI → Repository → Build **19** (oder den neuesten Build der Pipeline `centralized-reporting`).

- [ ] Steps `generate-dashboard`, `upload-dashboard`, `unzip-dashboard` öffnen
- [ ] `upload-dashboard` muss `allure-dashboard.zip` nach `/var/www/downloads/dashboard/` kopiert haben
- [ ] `unzip-dashboard` muss ohne Fehler durchlaufen (`unzip -o allure-dashboard.zip`)
- [ ] Meldungen wie `can't connect without a private SSH key` oder `missing server host` dürfen nicht mehr auftauchen

### 2. Ergebnis auf dem Zielhost kontrollieren
Per SSH auf `deploy_host` als `deploy_user`:

- [ ] `ls -l /var/www/downloads/dashboard/` zeigt `allure-dashboard.zip` mit aktuellem Zeitstempel
- [ ] Das Dashboard ist entpackt (z. B. `index.html` im selben Verzeichnis) und im Browser erreichbar
- [ ] `unzip` ist auf dem Zielhost installiert (`which unzip`), sonst schlägt `unzip-dashboard` fehl

### 3. Falls der Build trotzdem fehlschlägt
| Meldung | Wahrscheinliche Ursache | Maßnahme |
|---|---|---|
| `can't connect without a private SSH key or password` | Secret `ssh_key` leer | Secret in Drone neu setzen (kompletter privater Schlüssel inkl. `-----BEGIN ... KEY-----`-Zeilen) |
| `missing server host` | Secret `deploy_host` leer | Secret `deploy_host` setzen (Hostname oder IP, ohne Port) |
| `ssh: handshake failed: unable to authenticate` | Öffentlicher Schlüssel fehlt auf dem Zielhost, oder `deploy_user` falsch | Öffentlichen Schlüssel in `~/.ssh/authorized_keys` von `deploy_user` eintragen |
| `Permission denied` beim Kopieren | `deploy_user` darf nicht nach `/var/www/downloads/dashboard/` schreiben | Verzeichnis anlegen und Rechte geben (`chown`/`chmod`) |
| `unzip: command not found` | `unzip` fehlt auf dem Zielhost | `sudo apt install unzip` |
| `generate-dashboard` rot | Dashboard wird nicht erzeugt (anderer Fehler) | Log von `scripts/allure-dashboard.sh` prüfen |

Die Secrets legst du in der Drone-UI an: Repository → **Settings → Secrets**. Alternativ per CLI:
`drone secret add --repository paul-fleischmann-com/beaglebone_black --name <name> --data <wert>`

### 4. Abschließen
- [ ] Ist der Build grün: Issue #279 mit Hinweis auf den grünen Build schließen
- [ ] Danach diese Datei löschen oder nach `docs/` überführen

## Hinweise
- `upload-dashboard` und `unzip-dashboard` laufen mit `when: status: [success, failure]`, d. h. auch nach fehlgeschlagenen Tests. Ein roter Step kann also auch hier auftreten, obwohl die Tests grün sind.
- Dieselbe Secret-Lücke gab es bei `git_token` (`push-exports`) und bei `beagle_host` (siehe `ToDO/285-drone-secret-beagle-host.md`). Werden weitere Pipelines rot mit leeren Secrets, lohnt ein Abgleich aller `from_secret:`-Namen in `.drone.yml` mit der Secret-Liste in Drone.
