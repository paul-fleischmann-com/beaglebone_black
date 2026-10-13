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

## Empfehlung
1. **Onboard-Ethernet** verwenden, wenn ein Kabel möglich ist.
2. Geht das nicht, einen **USB-Ethernet-Adapter** (Variante 1) einsetzen. Vorher am Board prüfen, ob der Treiber im Image vorhanden ist.
3. WLAN (Variante 2) und die Gadget-Varianten (3, 4) nur, wenn 0 und 1 ausscheiden.

In allen Fällen: **DHCP-Reservierung** im Router (feste IP pro MAC-Adresse) oder statische Adresse im LAN, danach diese Adresse in den Drone-Secret `beagle_host` eintragen (siehe `ToDO/285-drone-secret-beagle-host.md`).

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
- [ ] Gewählte Variante am echten Board testen (Ping, SSH und `:5000` aus dem LAN)
- [ ] Prüfen, welcher Netzwerkdienst im Debian- und im Yocto-Image aktiv ist
- [ ] Bei USB-Adapter: Treiber im Debian-Image und im Yocto-Kernel bestätigen, bei Bedarf Kernel-Fragment als eigenes Issue anlegen
- [ ] Feste Adresse bzw. DHCP-Reservierung festlegen und in `beagle_host` (Drone) eintragen
