# BeagleBone Black neu aufsetzen (SD-Karte)

Anleitung zum Flashen eines frischen Debian-Images auf den BeagleBone Black —
von Windows und Linux aus.

---

## 1. Image herunterladen

Aktuelle Images: **https://www.beagleboard.org/distros**

Empfohlen: **Debian Bookworm Minimal** (IoT-Image, kein Desktop)

```
Dateiname: bone-debian-12.x-iot-armhf-YYYY-MM-DD-4gb.img.xz
```

---

## 2. SD-Karte flashen

### Windows — balenaEtcher (empfohlen)

1. [balenaEtcher](https://etcher.balena.io/) herunterladen und installieren
2. **Flash from file** → `.img.xz`-Datei auswählen (kein Entpacken nötig)
3. **Select target** → SD-Karte auswählen (mind. 4 GB)
4. **Flash!** → warten bis abgeschlossen
5. SD-Karte sicher auswerfen

### Windows — Rufus (Alternative)

1. [Rufus](https://rufus.ie/) herunterladen
2. Device: SD-Karte; Boot selection: `.img.xz`-Datei
3. Partition scheme: **MBR**; Start → OK

### Linux — dd

```bash
# SD-Karte identifizieren (VORSICHT: richtiges Device wählen!)
lsblk
# z.B. /dev/sdb — NIE das System-Laufwerk!

# Image entpacken und schreiben
xzcat bone-debian-12.x-iot-armhf-*.img.xz | sudo dd of=/dev/sdb bs=4M status=progress conv=fsync
sudo sync
```

### Linux — balenaEtcher (GUI-Alternative)

```bash
# AppImage herunterladen von https://etcher.balena.io/
chmod +x balenaEtcher-*.AppImage
./balenaEtcher-*.AppImage
```

---

## 3. Von SD-Karte booten

1. SD-Karte in den BBB-Slot einlegen
2. **S2-Taste** (Boot-Taster neben SD-Slot) gedrückt halten
3. USB-Kabel einstecken (Stromversorgung)
4. S2-Taste loslassen sobald die LEDs aufleuchten
5. BBB bootet jetzt vom SD-Karten-Image (ca. 60–90 s)

> Ohne S2 bootet der BBB vom internen eMMC (falls vorhanden).

---

## 4. Verbindung herstellen

### USB-Ethernet (automatisch nach Boot)

```bash
# Linux / macOS
ssh debian@192.168.7.2   # Passwort: temppwd

# Windows (PowerShell)
ssh debian@192.168.7.2
```

### Serielle Konsole (falls SSH nicht klappt)

**Linux:**
```bash
sudo screen /dev/ttyACM0 115200
# Enter drücken → Login-Prompt
```

**Windows:**
- Geräte-Manager → Anschlüsse → COM-Nummer merken
- PuTTY: Serial, `COMx`, 115200

---

## 5. Image auf eMMC flashen (permanent, optional)

Damit der BBB dauerhaft das neue System nutzt — auch ohne SD-Karte.

### Empfohlen: beagle-flasher (neuere Images ab 2024)

```bash
# Auf dem BBB (via SSH, von SD gebootet):
sudo beagle-flasher
```

Der BBB blinkt während des Flash-Vorgangs mit den LEDs und fährt anschließend automatisch
herunter. **SD-Karte entfernen**, USB neu anstecken → bootet von eMMC.

> **Hinweis:** `beagle-flasher` erfordert ausreichend Strom — am besten externes 5V-Netzteil
> statt USB verwenden, da USB unter Last zu wenig Strom liefern kann.

Falls `beagle-flasher` nicht gefunden wird:

```bash
sudo enable-beagle-flasher && sudo reboot
# BBB flasht beim Reboot automatisch die eMMC
```

### Fallback: manuell per dd (nur wenn SD-Karte ≤ eMMC-Größe)

```bash
lsblk   # mmcblk0 = SD-Karte, mmcblk1 = eMMC
sudo dd if=/dev/mmcblk0 of=/dev/mmcblk1 bs=4M status=progress conv=fsync
sudo sync
sudo shutdown -h now
# SD-Karte entfernen, USB neu anstecken → bootet von eMMC
```

---

## 6. Erstkonfiguration nach dem Flash

```bash
# SSH-Verbindung
ssh debian@192.168.7.2   # Passwort: temppwd

# Passwort sofort ändern
passwd

# Hostname setzen (optional)
sudo hostnamectl set-hostname beaglebone

# System aktualisieren
sudo apt update && sudo apt upgrade -y

# I2C-Tools installieren (für BME280)
sudo apt install i2c-tools

# BME280 prüfen (nach Verkabelung)
i2cdetect -y -r 1
# → Adresse 0x76 muss erscheinen

# App-Verzeichnis anlegen
sudo mkdir -p /app && sudo chown debian:debian /app
```

---

## Weiterführend

- Verkabelung BME280: `docs/how-to/bme280-seengreat-anschliessen.adoc`
- Go API deployen: `docs/SETUP.md` → Abschnitt "Deployen"
- Windows-Zugriff: `docs/SETUP.md` → Abschnitt "Windows-Zugriff"
