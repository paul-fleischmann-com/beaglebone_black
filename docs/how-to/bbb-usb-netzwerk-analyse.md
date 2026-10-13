# BeagleBone Black über USB ins interne Netz einbinden (Analyse zu #306)

Stand: Analyse auf Basis von Dokumentation, Foren und dem Repo. **Nichts davon wurde am echten Board getestet** (siehe [Offen](#offen)).

## Ausgangslage
- Das BBB ist bisher über das **USB-Gadget-Netz** (Mini-USB, RNDIS/ECM) mit dem Entwicklungsrechner verbunden. Das Board hat dort `192.168.7.2` (siehe `docs/SETUP.md`). Diese Adresse gilt nur für den direkt angeschlossenen Rechner, nicht für das LAN und nicht für den Drone-Runner.
- Drone-Nachtläufe und Hardware-Tests (`BEAGLE_HOST`, siehe `ToDO/285-drone-secret-beagle-host.md`) brauchen eine **aus dem LAN erreichbare Adresse**.
- Das BBB hat zusätzlich einen onboard-Ethernet-Port (RJ45). Er ist die Vergleichsbasis.

## Varianten

| # | Variante | Aufwand | Kosten | Risiko | Bewertung |
|---|---|---|---|---|---|
| 0 | **Onboard-Ethernet (RJ45)** an Router/Switch | sehr gering | Kabel | gering | **Empfohlen, falls ein Kabel möglich ist** |
| 1 | **USB-Ethernet-Adapter** am USB-Host-Port | mittel | ca. 10–20 € | Treiber im Image, Stromaufnahme | Beste USB-Alternative |
| 2 | **USB-WLAN-Stick** am USB-Host-Port | mittel bis hoch | ca. 10–20 € | Treiber/Firmware, Stabilität, Stromaufnahme | Nur wenn kein Kabel möglich |
| 3 | **Gadget-Netz zu einem Zwischenrechner** (NAT/Bridge) | mittel | keine | Rechner muss dauerhaft laufen | Nur als Notlösung |
| 4 | **Gadget direkt an einem Router mit USB-Host-Port** | unklar | keine | Router muss RNDIS/ECM als Netzwerkschnittstelle unterstützen | Meist nicht möglich |

### Variante 0: Onboard-Ethernet
Kein USB nötig. Das Board bekommt per DHCP eine Adresse, im Router reserviert man sie dauerhaft. Das löst das Problem aus #285/#306 ohne Zusatzhardware. Wenn ein Netzwerkkabel zum Board geführt werden kann, ist das die Lösung.

### Variante 1: USB-Ethernet-Adapter
- Adapter an den **USB-Host-Port (Typ A)** des BBB, Kabel zum Router.
- **Treiber:** Gängige Chipsätze sind ASIX (AX88772) und Realtek (RTL8152/8153). Foren berichten, dass auf manchen BBB-Debian-Images das Modul `asix` (mit `mii` und `usbnet`) fehlt oder das Interface trotz geladenem Modul nicht erscheint ([Forum 1](https://forum.beagleboard.org/t/wish-to-use-a-usb-to-wired-ethenet-adapter/22063), [Forum 2](https://forum.beagleboard.org/t/beaglebone-black-miss-mii-ko-and-usbnet-ko-so-no-usb-to-ethernet-converter-work/23355)). Ob das auf dem aktuell verwendeten Image zutrifft, ist am Board zu prüfen (`lsusb`, `dmesg | tail`, `ip link`, `modinfo asix r8152`).
- **Yocto (Kirkstone):** Für den Adapter müssen die Kernel-Optionen `CONFIG_USB_USBNET`, `CONFIG_USB_NET_AX8817X` (ASIX) bzw. `CONFIG_USB_RTL8152` aktiv sein. Im Repo sind sie nicht explizit gesetzt (Kernel-Fragment in `project/yocto/meta-bbb-sensors/recipes-kernel/linux` prüfen). Wenn sie fehlen, wäre ein Kernel-Fragment nötig.
- **Strom:** Der USB-Host-Port ist über einen Power-Switch auf maximal **500 mA** begrenzt ([Forum](https://forum.beagleboard.org/t/changing-usb-current-limit-in-bb-black/15530)). Ein Ethernet-Adapter braucht deutlich weniger, aber das Board sollte über das **Netzteil am Barrel-Jack (5 V, 1,2–2 A)** und nicht über Mini-USB versorgt werden ([DigiKey](https://forum.digikey.com/t/powering-the-beaglebone-black/186)).

### Variante 2: USB-WLAN-Stick
Zusätzlich zu den Punkten von Variante 1 braucht der Stick Firmware (`linux-firmware`) und eine Konfiguration mit `wpa_supplicant`. Im Yocto-Image kommen Recipes für Treiber und Firmware dazu. Viele Sticks nehmen mehr Strom auf, was die 500-mA-Grenze belastet. Für einen dauerhaft erreichbaren Testaufbau ist WLAN die schwächste Wahl.

### Variante 3: Gadget-Netz mit Zwischenrechner
Das BBB hängt per Mini-USB an einem Rechner, der das Netz per NAT oder Bridge weitergibt (Windows: Internetverbindungsfreigabe, Linux: `iptables`/`nftables`-NAT). Es funktioniert, aber das Board ist nur erreichbar, solange der Rechner läuft. Für Drone nicht geeignet.

### Variante 4: Gadget direkt am Router
Das BBB tritt als USB-Gerät auf (RNDIS/ECM). Ein Router mit USB-Host-Port nutzt diesen üblicherweise für Speicher oder Mobilfunk-Sticks, nicht für Gadget-Netzwerkadapter. Ob es beim vorhandenen Router geht, ist ohne Modellangabe nicht zu beantworten; die Chance ist gering.

## Gewählte Variante: Gadget-Netz über den Drone-Host (Variante 3)

Entscheidung: Das BBB hängt per Mini-USB am Rechner `192.168.2.55`, auf dem auch Drone läuft. Der Nachteil von Variante 3 („Zwischenrechner muss dauerhaft laufen“) entfällt, weil dieser Rechner ohnehin durchläuft. Kein Netzwerkkabel zum BBB und kein USB-Adapter nötig.

```
LAN ── 192.168.2.55 (Drone-Server/-Runner) ══ USB-Gadget ══ BBB
        │ usb-Interface: 192.168.7.1               192.168.7.2
        └ Drone-Container erreichen 192.168.7.2 über das Host-Routing
```

### Variante A: Drone-Runner greift direkt auf 192.168.7.2 zu (einfachste Lösung)
- Das BBB vergibt dem Host per DHCP `192.168.7.1`; das BBB selbst hat `192.168.7.2` (siehe `docs/SETUP.md`).
- Drone-Container laufen auf demselben Host. Docker leitet ihre Pakete über das Host-Routing (mit Masquerading) in das USB-Netz. Dann gilt für Drone: **`beagle_host` = `192.168.7.2`**, REST-Port 5000 und SSH-Port 22 bleiben unverändert. Es ist weder Port-Forwarding noch Codeänderung nötig.
- Einschränkung: `192.168.7.2` ist nur für diesen Host und seine Container erreichbar, nicht für andere Rechner im LAN.
- Zu prüfen am Host: `ip addr` (USB-Interface mit `192.168.7.1`), `sysctl net.ipv4.ip_forward` (Docker setzt `1`), `docker run --rm alpine ping -c 2 192.168.7.2`.

### Variante B: „spezieller Port“ auf 192.168.2.55 (Port-Forwarding, Zugriff aus dem ganzen LAN)
Ein Port auf `192.168.2.55` wird per DNAT an das BBB weitergereicht. Beispiel (ungetestet; `<lan-if>` und `<usb-if>` durch die echten Interfacenamen ersetzen):

```bash
sudo sysctl -w net.ipv4.ip_forward=1
# SSH: 192.168.2.55:2222 -> BBB:22
sudo iptables -t nat -A PREROUTING -i <lan-if> -p tcp --dport 2222 -j DNAT --to-destination 192.168.7.2:22
# REST-API: 192.168.2.55:5000 -> BBB:5000
sudo iptables -t nat -A PREROUTING -i <lan-if> -p tcp --dport 5000 -j DNAT --to-destination 192.168.7.2:5000
sudo iptables -t nat -A POSTROUTING -o <usb-if> -d 192.168.7.2 -j MASQUERADE
sudo iptables -A FORWARD -d 192.168.7.2 -p tcp -m multiport --dports 22,5000 -j ACCEPT
```

Die Regeln überstehen keinen Neustart; dauerhaft über `iptables-persistent`/`nftables` oder ein systemd-Unit-File sichern. Das USB-Interface heißt je nach System `usb0` oder `enx<MAC>`.

**Achtung bei Variante B:** `tests/conftest.py` prüft `BEAGLE_HOST` immer auf **Port 5000**. Wird die REST-API auf einem anderen Host-Port angeboten, müsste der Test um eine Variable wie `BEAGLE_PORT` erweitert werden. Wird Port 5000 auf `192.168.2.55` mit 5000 weitergeleitet, geht es ohne Codeänderung, aber nur, wenn dort kein anderer Dienst Port 5000 nutzt. SSH-basierte Tests (`BEAGLE_USER`, SSH-Port 22) bräuchten ebenfalls einen Port-Parameter, wenn SSH auf `2222` liegt.

### Empfehlung für diesen Aufbau
**Variante A.** `beagle_host` = `192.168.7.2`. Sie braucht keine Zusatzkonfiguration auf dem Host und keine Codeänderung. Variante B nur, wenn Rechner außerhalb des Drone-Hosts auf das BBB zugreifen sollen. Dann ein Folge-Issue für `BEAGLE_PORT`/SSH-Port in den Tests anlegen.

## Vergleich mit den anderen Varianten (Rückfallebene)
1. **Onboard-Ethernet** (Variante 0), wenn später doch ein Kabel möglich ist.
2. **USB-Ethernet-Adapter** (Variante 1) als USB-Alternative zum Router; vorher Treiber im Image prüfen.
3. WLAN (Variante 2) und Gadget direkt am Router (Variante 4) nur, wenn nichts anderes geht.

In allen Fällen: stabile Adresse festlegen (hier `192.168.7.2`, fest durch das Gadget-Netz) und in den Drone-Secret `beagle_host` eintragen (siehe `ToDO/285-drone-secret-beagle-host.md`).

## Konfiguration (ungetestet, Richtwerte für Debian)

1. Adapter einstecken und prüfen:
   ```bash
   lsusb
   dmesg | tail -n 20
   ip link
   ```
2. Fehlt das Interface, Modul prüfen und laden:
   ```bash
   modinfo asix r8152
   sudo modprobe asix        # bzw. r8152
   ```
3. Adresse bekommen. Wie das Image Netzwerke verwaltet (`systemd-networkd`, `NetworkManager` oder `connman`), ist am Board zu prüfen (`systemctl status systemd-networkd NetworkManager connman`). Mit `systemd-networkd` z. B. `/etc/systemd/network/20-usb-eth.network`:
   ```ini
   [Match]
   Name=eth1

   [Network]
   DHCP=yes
   ```
   Der Interface-Name (`eth1`, `enx<MAC>`) hängt vom System ab.
4. Mit dem Gadget-Netz `192.168.7.2` kollidiert nichts, solange das LAN nicht ebenfalls `192.168.7.0/24` nutzt. Ist das der Fall, anderes Subnetz für den Router wählen oder die Gadget-Adresse ändern.
5. Von einem LAN-Rechner testen:
   ```bash
   ping <ip>
   ssh debian@<ip>
   curl http://<ip>:5000/health
   ```

## Offen
- [ ] Variante A am Drone-Host testen: `docker run --rm alpine ping -c 2 192.168.7.2`, danach `curl http://192.168.7.2:5000/health` aus einem Drone-Step
- [ ] Entscheiden, ob Variante B (Port-Forwarding, LAN-Zugriff) gebraucht wird; falls ja, `BEAGLE_PORT`/SSH-Port in den Tests ergänzen
- [ ] Prüfen, welcher Netzwerkdienst im Debian- und im Yocto-Image aktiv ist
- [ ] Bei USB-Adapter: Treiber im Debian-Image und im Yocto-Kernel bestätigen, bei Bedarf Kernel-Fragment als eigenes Issue anlegen
- [ ] `beagle_host` in Drone auf `192.168.7.2` setzen (Variante A)
