# acfcan-viewer: Open1722-ETH-Node mit Live-Visualisierung (#259).
# Läuft NATIV (x86_64/Host-Architektur), nicht auf der BeagleBone Black —
# Gegenstelle zur acf-can-talker-Instanz auf dem Board (siehe #256/#257).

FROM debian:bookworm-slim AS builder

RUN apt-get update -qq && apt-get install -y -qq --no-install-recommends \
      build-essential cmake git ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Gepinnt auf denselben Commit wie scripts/setup_open1722.sh (#256/#257),
# damit alle Open1722-Komponenten dieses Projekts identischen Code verwenden.
ARG OPEN1722_REV=8535cfd63da7a71ec1169d122b2c6d081b28e75b
RUN git clone https://github.com/COVESA/Open1722.git /open1722 \
    && git -C /open1722 checkout --detach "$OPEN1722_REV"

RUN cmake -S /open1722 -B /open1722/build -DCMAKE_BUILD_TYPE=Release \
    && cmake --build /open1722/build --target acf-can-listener -- -j"$(nproc)"

# mkad (Technica-Engineering/MKAdaemon, GPLv2, siehe #260) — MACsec/MKA-
# Absicherung der Verbindung zum Board. DISABLE_DBUS=1 wie in der
# Yocto-Recipe (project/yocto/meta-bbb-sensors/recipes-bbb/mkad/): spart
# glib/gio/libxml2, für diese Demo reicht die feste YAML-Config.
FROM debian:bookworm-slim AS mkad-builder

RUN apt-get update -qq && apt-get install -y -qq --no-install-recommends \
      build-essential python3 git ca-certificates pkg-config \
      libssl-dev libyaml-dev libbsd-dev \
      libnl-3-dev libnl-genl-3-dev libnl-route-3-dev \
    && rm -rf /var/lib/apt/lists/*

ARG MKAD_REV=23c987f9c3b531bf6912e2018269ced0b5189ecd
RUN git clone https://github.com/Technica-Engineering/MKAdaemon.git /mkad-src \
    && git -C /mkad-src checkout --detach "$MKAD_REV"

RUN cd /mkad-src && DISABLE_DBUS=1 ./configure && DISABLE_DBUS=1 python3 waf build

FROM debian:bookworm-slim

RUN apt-get update -qq && apt-get install -y -qq --no-install-recommends \
      python3 python3-pip iproute2 kmod \
      libssl3 libyaml-0-2 libbsd0 libnl-3-200 libnl-genl-3-200 libnl-route-3-200 \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /open1722/build/examples/acf-can/linux/acf-can-listener /usr/local/bin/acf-can-listener
COPY --from=mkad-builder /mkad-src/build/mkad /usr/local/bin/mkad

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --break-system-packages -r requirements.txt

COPY app.py index.html entrypoint.sh mkad-viewer.conf ./
RUN chmod +x entrypoint.sh

ENV ACFCAN_VIEWER_CANIF=vcan1
ENV ACFCAN_VIEWER_ETHIF=eth0
ENV ACFCAN_VIEWER_PORT=8080
ENV ACFCAN_VIEWER_MACSEC_IF=macsec0
ENV ACFCAN_VIEWER_MKAD_CONFIG=/app/mkad-viewer.conf

EXPOSE 8080

ENTRYPOINT ["/app/entrypoint.sh"]
