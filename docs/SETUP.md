# Setup Guide

## Voraussetzungen

### Entwicklungsrechner (Linux/macOS)

> **Windows-Nutzer:** Siehe Abschnitt [Windows-Zugriff](#windows-zugriff) weiter unten.

```bash
# Go 1.22+
wget https://go.dev/dl/go1.22.linux-amd64.tar.gz
sudo tar -C /usr/local -xzf go1.22.linux-amd64.tar.gz
echo 'export PATH=$PATH:/usr/local/go/bin' >> ~/.bashrc

# Rust + Cross-Compilation
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
cargo install cross cbindgen

# ARM Cross-Compiler
sudo apt install gcc-arm-linux-gnueabihf

# Python (Tests)
sudo apt install python3-pip
pip3 install pytest requests pytest-json-report
```

### BeagleBone Black

```bash
# SSH Verbindung
ssh debian@192.168.7.2   # Passwort: temppwd

# SSH Key einrichten
ssh-keygen -t ed25519 -f ~/.ssh/beagle_key
ssh-copy-id -i ~/.ssh/beagle_key.pub debian@192.168.7.2

# I2C prüfen
i2cdetect -y -r 1
# Ausgabe: 76 (BME280)

# App-Verzeichnis
sudo mkdir -p /app
sudo chown debian:debian /app
```

## Projekt bauen

```bash
git clone https://github.com/user/beaglebone-embedded.git
cd beaglebone-embedded

# Alles bauen
make all

# Einzeln
make c-lib       # → project/go-api/libs/libhardware.so
make rust-lib    # → project/go-api/libs/libhardware_rs.so
make go-api      # → bin/embedded-armv7
make cli         # → bin/bbcli-linux-amd64

# Tests
make test
```

## Deployen

### Option A — Aus dem Release (empfohlen, kein Build nötig)

```bash
# Binaries vom aktuellen Release herunterladen
mkdir -p /tmp/bbb-deploy && cd /tmp/bbb-deploy

gh release download v1.1.1 \
  --repo paul-fleischmann-com/beaglebone_black \
  --pattern "embedded-armv7" \
  --pattern "libhardware.so" \
  --pattern "libhardware_rs.so"

# App-Verzeichnis auf BBB anlegen
ssh debian@192.168.7.2 "sudo mkdir -p /app && sudo chown debian:debian /app"

# Binaries auf BBB kopieren
scp embedded-armv7 libhardware.so libhardware_rs.so debian@192.168.7.2:/app/

ssh debian@192.168.7.2 "chmod +x /app/embedded-armv7"
```

### Option B — Aus dem Quellcode bauen

```bash
# Alles bauen
make all

# Auf BeagleBone deployen
make deploy
```

### API testen

```bash
curl http://192.168.7.2:5000/health
curl http://192.168.7.2:5000/api/v1/bme280
```

## CLI einrichten

```bash
# bbcli installieren
sudo install -m 755 bin/bbcli-linux-amd64 /usr/local/bin/bbcli

# Konfiguration
bbcli config init
bbcli config set host 192.168.7.2

# Shell Completion
bbcli completion bash >> ~/.bashrc && source ~/.bashrc

# Test
bbcli system status
bbcli bme280 read
```

## Windows-Zugriff

### 1. USB-Treiber installieren

Beim ersten Anstecken versucht Windows den Treiber automatisch zu installieren.
Falls das fehlschlägt, Treiber-Paket manuell herunterladen:

- [beagleboard.org/getting-started](https://beagleboard.org/getting-started) → **Windows Drivers**

Nach erfolgreicher Installation zeigt der Geräte-Manager:
- **Netzwerkadapter**: `BeagleBone` (USB-Ethernet RNDIS, IP `192.168.7.2`)
- **Anschlüsse (COM & LPT)**: `COMx` (serielle Konsole)

### 2. SSH (Windows 10/11)

Windows 10/11 hat OpenSSH eingebaut:

```powershell
ssh debian@192.168.7.2
# Passwort: temppwd
```

Alternativ: [PuTTY](https://www.putty.org/) — Host `192.168.7.2`, Port `22`, SSH.

### 3. Serielle Konsole (z.B. für Passwort-Recovery)

1. Geräte-Manager öffnen → **Anschlüsse (COM & LPT)** → COM-Nummer merken (z.B. `COM4`)
2. PuTTY öffnen:
   - Connection type: **Serial**
   - Serial line: `COM4` (eigene Nummer eintragen)
   - Speed: `115200`
   - **Open** → Enter drücken → Login-Prompt erscheint

### 4. Passwort zurücksetzen (über serielle Konsole)

```bash
sudo passwd debian
# oder als root:
su -
passwd debian
```

---

## Systemd Service (BeagleBone)

```bash
# /etc/systemd/system/embedded-sw.service
cat > /etc/systemd/system/embedded-sw.service << 'EOF'
[Unit]
Description=BeagleBone Black Embedded SW
After=network.target

[Service]
Type=simple
User=debian
WorkingDirectory=/app
Environment=LD_LIBRARY_PATH=/app
Environment=HW_BACKEND=auto
ExecStart=/app/embedded-armv7
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable --now embedded-sw
systemctl status embedded-sw
```
