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

FROM debian:bookworm-slim

RUN apt-get update -qq && apt-get install -y -qq --no-install-recommends \
      python3 python3-pip iproute2 kmod \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /open1722/build/examples/acf-can/linux/acf-can-listener /usr/local/bin/acf-can-listener

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --break-system-packages -r requirements.txt

COPY app.py index.html entrypoint.sh ./
RUN chmod +x entrypoint.sh

ENV ACFCAN_VIEWER_CANIF=vcan1
ENV ACFCAN_VIEWER_ETHIF=eth0
ENV ACFCAN_VIEWER_PORT=8080

EXPOSE 8080

ENTRYPOINT ["/app/entrypoint.sh"]
