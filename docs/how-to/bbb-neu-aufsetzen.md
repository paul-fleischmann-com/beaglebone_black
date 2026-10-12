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

```bash
# Auf dem BBB (via SSH): Devices prüfen
lsblk
# typisch: mmcblk0 = SD-Karte, mmcblk1 = eMMC (intern)
```

> **Wichtig:** Ist die SD-Karte **größer** als die eMMC (z.B. 29 GB SD → 14,6 GB eMMC),
> funktioniert direktes `dd` nicht. Dann Weg A oder Weg B verwenden.

### Weg A — Kleineres Image verwenden (empfohlen)

Ein 4-GB-Image passt auf jede BBB-eMMC und erlaubt direktes `dd`:

1. Image herunterladen: **`bone-debian-12.x-iot-armhf-*-4gb.img.xz`** von beagleboard.org
2. Auf SD flashen (wie in Abschnitt 2)
3. Von SD booten (Abschnitt 3), dann:

```bash
sudo dd if=/dev/mmcblk0 of=/dev/mmcblk1 bs=4M status=progress conv=fsync
sudo sync
sudo shutdown -h now
# SD-Karte entfernen, USB neu anstecken → bootet von eMMC
```

### Weg B — Partition für Partition kopieren

Wenn das laufende SD-System bereits eingerichtet ist und nicht nochmal neu aufgesetzt werden soll:

```bash
# 1. Partition-Layout von SD auf eMMC übertragen
sudo sfdisk --dump /dev/mmcblk0 | sudo sfdisk /dev/mmcblk1

# 2. Boot-Partition und Swap 1:1 kopieren
sudo dd if=/dev/mmcblk0p1 of=/dev/mmcblk1p1 bs=4M status=progress
sudo dd if=/dev/mmcblk0p2 of=/dev/mmcblk1p2 bs=4M status=progress

# 3. Root-Partition formatieren und per rsync befüllen
sudo mkfs.ext4 /dev/mmcblk1p3
sudo mount /dev/mmcblk1p3 /mnt
sudo rsync -aAX \
  --exclude={"/dev/*","/proc/*","/sys/*","/tmp/*","/run/*","/mnt/*"} \
  / /mnt/

# 4. UUID in /etc/fstab anpassen
# fstab enthält noch die UUID der SD-Karte — muss auf eMMC-UUID geändert werden
NEW_UUID=$(sudo blkid -s UUID -o value /dev/mmcblk1p3)
OLD_UUID=$(sudo blkid -s UUID -o value /dev/mmcblk0p3)
sudo sed -i "s/$OLD_UUID/$NEW_UUID/g" /mnt/etc/fstab
# Ergebnis prüfen:
cat /mnt/etc/fstab

sudo umount /mnt
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
