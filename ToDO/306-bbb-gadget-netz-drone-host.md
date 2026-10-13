# TODO: BBB per USB-Gadget-Netz am Drone-Host anbinden (Variante A, #306)

Issue: [#306 analysis(network): BeagleBone Black über USB ins interne Netz einbinden](https://github.com/paul-fleischmann-com/beaglebone_black/issues/306)
Analyse: `docs/how-to/bbb-usb-netzwerk-analyse.md` (PR #307)

## Ziel
Das BBB hängt per Mini-USB am Drone-Host `192.168.2.55`. Drone-Container erreichen es unter `192.168.7.2` (REST-API Port 5000, SSH Port 22). Im Code ändert sich nichts. Alle Schritte laufen auf `192.168.2.55`, Drone-Einstellungen in der Drone-UI.

Hinweis: Alle Befehle sind ungetestet (aus Dokumentation abgeleitet). Der Host ist ein Debian-Linux mit Benutzer `deploy` und **Podman** (nicht Docker; Interface `podman1`, `10.89.0.1/24`). Befehle mit `podman` statt `docker`.

## Schritte

### 1. BBB anschließen
- [ ] Mini-USB-Kabel vom BBB in einen USB-Port des Hosts (kein schwach versorgter Hub)
- [ ] BBB zusätzlich über das Netzteil am Barrel-Jack versorgen (5 V, 1,2–2 A), nicht nur über USB
- [ ] Etwa eine Minute warten, bis das Board gebootet hat

### 2. USB-Interface auf dem Host prüfen
```bash
lsusb                  # BBB als Gadget-Gerät (Linux Foundation / RNDIS / CDC Ethernet)
dmesg | tail -n 20
ip -br addr
```
- [ ] Ein neues Interface (`usb0` oder `enx<MAC>`) ist vorhanden
- [x] Interface gefunden: `enx647060d23516`, `UP`, `192.168.7.1/30` (per DHCP vom BBB)

Hinweis: `dmesg` meldet als Benutzer `deploy` „Die Operation ist nicht erlaubt“ (`kernel.dmesg_restrict`). Dann `sudo dmesg | tail -n 20` nehmen; `lsusb` und `ip -br addr` brauchen keine Root-Rechte.

### 3. Adresse setzen, falls keine vergeben wurde
Normalerweise bekommt der Host `192.168.7.1/24` per DHCP vom BBB. Fehlt die Adresse, vorübergehend:
```bash
sudo ip addr add 192.168.7.1/24 dev <interface>
sudo ip link set <interface> up
```
- [ ] Interface hat `192.168.7.1/24`

### 4. Verbindung zum BBB testen
```bash
ping -c 3 192.168.7.2
ssh debian@192.168.7.2                       # Passwort laut docs/SETUP.md
curl http://192.168.7.2:5000/health          # nur, wenn die API auf dem BBB läuft
```
- [ ] `ping` antwortet
- [ ] SSH-Login funktioniert
- [ ] `curl` liefert `{"status":"ok"}` (sonst Deployment laut `docs/SETUP.md` prüfen, Dienst `embedded-sw`)

### 5. SSH-Schlüssel für Drone hinterlegen
Der öffentliche Teil des Schlüssels, dessen privater Teil als Secret `ssh_key_bbb` in Drone liegt, muss auf dem BBB stehen. `<pfad>` in den Befehlen ist der Ordner, in dem die Schlüsseldatei liegt, normalerweise `~/.ssh/`.

**Fall 1: Schlüssel existiert schon.** Nachsehen:
```bash
ls -l ~/.ssh/
```
Dateien wie `id_ed25519` (privat) und `id_ed25519.pub` (öffentlich) liegen dort. Dann:
```bash
ssh-copy-id -i ~/.ssh/id_ed25519.pub debian@192.168.7.2
```
Heißt die Datei anders (`id_rsa.pub`, `beagle_key.pub` laut `docs/SETUP.md`), den Namen entsprechend einsetzen.

**Fall 2: Noch kein Schlüssel.** Eigenen Schlüssel nur für Drone anlegen, ohne Passphrase (Drone kann keine eingeben):
```bash
ssh-keygen -t ed25519 -f ~/.ssh/drone_bbb -C "drone-bbb" -N ""
ssh-copy-id -i ~/.ssh/drone_bbb.pub debian@192.168.7.2
ssh -i ~/.ssh/drone_bbb debian@192.168.7.2 true      # muss ohne Passwort laufen
```
`ssh-copy-id` fragt einmal das Passwort des BBB-Benutzers `debian` (laut `docs/SETUP.md`).

**Privater Teil für Drone:** Als Secret `ssh_key_bbb` kommt der **private** Schlüssel (Datei ohne `.pub`):
```bash
cat ~/.ssh/drone_bbb
```
Den kompletten Inhalt inklusive der Zeilen `-----BEGIN OPENSSH PRIVATE KEY-----` und `-----END ...-----` in der Drone-UI einfügen. Den privaten Schlüssel nirgends sonst weitergeben (nicht in Chats, Issues oder Commits).

- [ ] Schlüssel vorhanden (Fall 1) oder angelegt (Fall 2)
- [ ] Login mit dem Schlüssel ohne Passwort funktioniert

### 6. Prüfen, ob Podman-Container das BBB erreichen
```bash
sysctl net.ipv4.ip_forward          # soll 1 sein (sonst setzen, siehe Tabelle)
podman run --rm docker.io/library/alpine ping -c 2 192.168.7.2
podman run --rm docker.io/curlimages/curl -s http://192.168.7.2:5000/health
```
- [ ] Container erreicht `192.168.7.2` (Ping und `curl`)

Falls es fehlschlägt:
| Symptom | Ursache | Maßnahme |
|---|---|---|
| Weiterleitung geblockt | Firewall (`ufw`/`nftables`) | Weiterleitung von `podman1` nach `enx647060d23516` erlauben |
| Kein Routing | `ip_forward` ist 0 | `sudo sysctl -w net.ipv4.ip_forward=1`, dauerhaft über `/etc/sysctl.d/99-forward.conf` mit `net.ipv4.ip_forward=1` |
| Subnetz belegt | Ein Podman-Netz nutzt `192.168.7.0/24` | `podman network ls` und `podman network inspect <name>` prüfen, Netz umlegen |

### 7. Interface dauerhaft machen
Sonst ist die Adresse nach einem Neustart weg. Netzwerkdienst des Hosts feststellen: `systemctl status NetworkManager systemd-networkd`.

**NetworkManager:**
```bash
sudo nmcli con add type ethernet ifname <interface> con-name bbb \
  ipv4.method manual ipv4.addresses 192.168.7.1/24 ipv6.method ignore
```
**systemd-networkd** (`/etc/systemd/network/30-bbb.network`):
```ini
[Match]
Name=<interface>

[Network]
Address=192.168.7.1/24
```
Danach `sudo systemctl restart systemd-networkd`. Bei `usb0` kann sich der Name ändern; dann in `[Match]` die MAC-Adresse (`MACAddress=`) verwenden.

- [ ] Nach einem Neustart des Hosts (oder Ab- und Anstecken des BBB) ist `192.168.7.1` wieder gesetzt und `ping 192.168.7.2` geht

### 8. Drone konfigurieren
Drone-UI → Repository `paul-fleischmann-com/beaglebone_black` → Settings → Secrets:
- [ ] `beagle_host` = `192.168.7.2`
- [ ] `beagle_user` = `debian`
- [ ] `ssh_key_bbb` = privater Schlüssel aus Schritt 5

### 9. Pipeline testen
- [ ] Drone-UI → Cron → Job `nightly` → *Run now*
- [ ] Im Step `test-all-backends` erscheint nicht mehr `BEAGLE_HOST=… gesetzt aber nicht erreichbar`
- [ ] Die Backends `c`, `rust`, `auto` laufen durch

### 10. Abschließen
- [ ] #306 mit Hinweis auf das Ergebnis schließen (Variante A funktioniert oder Begründung für eine andere Variante)
- [ ] #285 (`beagle_host`) ist damit praktisch erledigt; falls sie noch offen ist, hier verlinken
- [ ] Diese Datei und `ToDO/285-drone-secret-beagle-host.md` löschen oder nach `docs/` überführen

## Stolpersteine
- Wird das BBB abgesteckt oder startet es neu, verschwindet das USB-Interface und kommt wieder. Mit Schritt 7 stellt sich die Adresse von selbst wieder her.
- `192.168.7.0/24` darf im LAN nicht doppelt vorkommen. Das LAN `192.168.2.0/24` ist unkritisch.
- `192.168.7.2` ist nur für den Drone-Host und seine Container erreichbar, nicht für andere LAN-Rechner. Dafür wäre Port-Forwarding (Variante B in `docs/how-to/bbb-usb-netzwerk-analyse.md`) und eine Code-Erweiterung um `BEAGLE_PORT` nötig.
