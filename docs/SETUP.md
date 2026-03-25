# Setup Guide

## Voraussetzungen

### Entwicklungsrechner (Linux/macOS)

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

```bash
# Auf BeagleBone deployen
make deploy

# Manuell
scp bin/embedded-armv7 \
    project/go-api/libs/libhardware.so \
    project/go-api/libs/libhardware_rs.so \
    debian@192.168.7.2:/app/

ssh debian@192.168.7.2 "systemctl restart embedded-sw"

# API testen
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
