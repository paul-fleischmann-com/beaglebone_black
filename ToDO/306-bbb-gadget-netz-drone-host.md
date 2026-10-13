# TODO: BBB per USB-Gadget-Netz am Drone-Host anbinden (Variante A, #306)

Issue: [#306 analysis(network): BeagleBone Black über USB ins interne Netz einbinden](https://github.com/paul-fleischmann-com/beaglebone_black/issues/306)
Analyse: `docs/how-to/bbb-usb-netzwerk-analyse.md` (PR #307)

## Ziel
Das BBB hängt per Mini-USB am Drone-Host `192.168.2.55`. Drone-Container erreichen es unter `192.168.7.2` (REST-API Port 5000, SSH Port 22). Im Code ändert sich nichts. Alle Schritte laufen auf `192.168.2.55`, Drone-Einstellungen in der Drone-UI.

Hinweis: Alle Befehle sind ungetestet (aus Dokumentation abgeleitet). Annahme: Linux-Host (vermutlich Debian 13), Drone läuft in Docker.

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
- [ ] Interface-Name notiert: `________________`

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
Der öffentliche Teil des Schlüssels, den du als Secret `ssh_key_bbb` verwendest, muss auf dem BBB liegen:
```bash
ssh-copy-id -i <pfad>/id_ed25519.pub debian@192.168.7.2
ssh -i <pfad>/id_ed25519 debian@192.168.7.2 true      # muss ohne Passwort laufen
```
- [ ] Login mit dem Schlüssel ohne Passwort funktioniert

### 6. Prüfen, ob Docker-Container das BBB erreichen
```bash
sysctl net.ipv4.ip_forward          # soll 1 sein (Docker setzt es)
docker run --rm alpine ping -c 2 192.168.7.2
docker run --rm curlimages/curl -s http://192.168.7.2:5000/health
```
- [ ] Container erreicht `192.168.7.2` (Ping und `curl`)

Falls es fehlschlägt:
| Symptom | Ursache | Maßnahme |
|---|---|---|
| Weiterleitung geblockt | Firewall (`ufw`) | `sudo ufw route allow in on docker0 out on <interface>` |
| Kein Routing | `ip_forward` ist 0 | `sudo sysctl -w net.ipv4.ip_forward=1` |
| Subnetz belegt | Ein Docker-Netz nutzt `192.168.7.0/24` | `docker network ls` und `docker network inspect <name>` prüfen, Netz umlegen |

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
