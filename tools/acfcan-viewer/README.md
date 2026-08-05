# acfcan-viewer

Open1722-ETH-Node mit Live-Visualisierung für die ACF-CAN-Demo (Issue #259).
Läuft als Container auf einem beliebigen Host im selben Netz wie die
BeagleBone Black — kein zweites Board nötig.

Vollständige Schritt-für-Schritt-Anleitung für die Gesamt-Demo (inkl.
optionaler MACsec/MKA-Absicherung, Issue #260):
[`docs/how-to/ieee1722-acfcan-demo-userguide.adoc`](../../docs/how-to/ieee1722-acfcan-demo-userguide.adoc).

```
BeagleBone Black                    Host (dieser Container)
vcan0 → acf-can-talker → eth0  ───▶  eth0 → acf-can-listener → vcan1 → app.py → Browser
```

## Bauen & starten

```bash
docker build -t acfcan-viewer .
docker run --rm -it \
  --network host \
  --cap-add=NET_ADMIN \
  -e ACFCAN_VIEWER_ETHIF=eth0 \
  acfcan-viewer
```

`--network host` + `--cap-add=NET_ADMIN` sind nötig, damit der Container ein
`vcan`-Interface anlegen und rohe Ethernet-Frames auf dem echten
Host-Interface empfangen kann (`acf-can-listener` braucht direkten Zugriff
auf das physische Interface, kein NAT/Bridge-Networking).

Dashboard danach unter `http://<host>:8080/`.

## Gegenstelle (BeagleBone Black)

```bash
make open1722-userspace && make deploy   # acf-can-talker aufs Board kopieren
ACFCAN_DEMO_DST_MAC=<MAC dieses Hosts> ./scripts/setup_acfcan_vcan_demo.sh
```

Siehe auch #256 (Kernel-Modul-Alternative) und #257 (User-Space-Tools).

## Umgebungsvariablen

| Variable | Standard | Bedeutung |
|---|---|---|
| `ACFCAN_VIEWER_CANIF` | `vcan1` | Lokales vcan-Interface, das `acf-can-listener` befüllt |
| `ACFCAN_VIEWER_ETHIF` | `eth0` | Ethernet-Interface, auf dem ACF-CAN-Frames empfangen werden |
| `ACFCAN_VIEWER_PORT` | `8080` | HTTP-Port des Dashboards |
| `ACFCAN_VIEWER_LISTENER_ARGS` | (leer) | Zusätzliche Flags für `acf-can-listener`, z.B. `--stream-id cafe11` |
| `ACFCAN_VIEWER_ENABLE_MACSEC` | (aus) | `1` aktiviert mkad + MACsec-Pfad (Issue #260) — siehe User-Guide |
| `ACFCAN_VIEWER_MACSEC_IF` | `macsec0` | MACsec-Interface, auf dem `acf-can-listener` bei aktivem MACsec hört |
| `ACFCAN_VIEWER_MKAD_CONFIG` | `/app/mkad-viewer.conf` | mkad-Konfigurationsdatei im Container |
| `ACFCAN_VIEWER_MKAD_WAIT_TIMEOUT` | `15` | Sekunden, die auf das Erscheinen von `macsec0` gewartet wird |
