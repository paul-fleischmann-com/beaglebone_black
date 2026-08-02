# acfcan-viewer

Open1722-ETH-Node mit Live-Visualisierung für die ACF-CAN-Demo (Issue #259).
Läuft als Container auf einem beliebigen Host im selben Netz wie die
BeagleBone Black — kein zweites Board nötig.

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
