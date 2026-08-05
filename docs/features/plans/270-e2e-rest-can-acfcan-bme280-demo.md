# Issue #270: End-to-End-Kette REST → CAN → ACF-CAN (IEEE 1722) → CAN → BME280 über 5 virtuelle Devices

## Feasibility-Analyse (Schritt 1)

Alle Bausteine außer dem REST↔CAN-Gateway (D2) und der CAN→HAL-Bridge (D5) existieren
bereits (#256/#257/#259) und werden nur neu zusammengesteckt. Getroffene Entscheidungen:

- **ACF-CAN-Default für D3/D4:** Kernel-Modul `acfcan` (#256), wie vom Issue vorgeschlagen —
  exakt der Sysfs-Ablauf aus `tests/hardware/test_acfcan.py` (ethif/dstmac/streamid), nur
  zwischen zwei echten Netzwerk-Namespaces (dev3/dev4) statt einem gemeinsamen. Die
  User-Space-Alternative (`acf-can-talker`/`-listener`, #257) wird dokumentiert, aber nicht
  parallel implementiert (reine Konfigurationsvariante des Setup-Skripts, kein eigener Code).
- **`vxcan` statt `vcan`** für D2↔D3 und D4↔D5, wie im Issue begründet (zwei `vcan0` in
  getrennten Namespaces sind isoliert; `vxcan` verbindet sie tatsächlich).
- **CAN-Protokoll (minimal):** Request-ID `0x100` (leerer Payload = "read temperature"),
  Response-ID `0x101` (Payload = Temperatur als `float32`, big-endian, 4 Byte). Bewusst kein
  vollständiges BME280-Protokoll (Feuchtigkeit/Druck/Höhe = spätere Erweiterung, siehe Issue).
- **SocketCAN-Anbindung in Go ohne CGO:** D2/D5 sprechen den CAN-Bus direkt über
  `AF_CAN`/`SOCK_RAW`-Rohsockets (`golang.org/x/sys/unix`) an. Das ist kein Verstoß gegen die
  Hardware-Regel (Hardware-Zugriff nur in C/Rust) — SocketCAN ist eine Linux-Netzwerkschicht
  (wie das bereits genutzte HTTP/TCP in `go-api`), kein direkter Registerzugriff auf
  BME280/GPIO/UART/SPI. Der einzige echte Hardware-Zugriff (D5 → Sensor) bleibt exakt in der
  bestehenden HAL (`pkg/hal/c`, `pkg/hal/rust`, `pkg/hal/mock`).
- **D5-Backend:** `pkg/hal/mock` ist der Default (kein CGO, keine Hardware-Abhängigkeit, CI-tauglich,
  liefert deterministisch `Temperature: 23.45`). Echte Hardware (`c`/`rust`/`auto` über die
  bestehende `pkg/hal/loader`) ist über den Go-Build-Tag `hwreal` erreichbar (separates Binary,
  CGO_ENABLED=1, wie `bin/embedded`) — beide Varianten dokumentiert, wie vom Issue gefordert.
- **Visualisierung (Issue-Punkt 9, optional):** kein neues Web-Dashboard — dafür existiert
  bereits `tools/acfcan-viewer` (#259) und ein zweites Dashboard wäre reine Dopplung.
  Stattdessen strukturierte Log-Zeilen an jeder Station (D2 und D5 loggen Request/Response
  inkl. CAN-ID und Payload), ausreichend um die Übersetzungskette nachzuvollziehen.
- **Scope-Grenze:** Kein neuer Kernel-/Firmware-Code. D2/D5 sind reine Go-Anwendungsprozesse,
  die auf vorhandenen Linux-Primitiven (netns, veth, vxcan, SocketCAN, acfcan-Modul, HAL) aufsetzen.

## Phase 1 — CAN-Protokoll + SocketCAN-Anbindung (Go, ohne CGO)

- `project/go-api/pkg/e2edemo/protocol.go`: Konstanten `RequestCANID = 0x100`,
  `ResponseCANID = 0x101`, `EncodeResponse(temp float32) [8]byte`,
  `DecodeResponse(data []byte) (float32, error)` — reine, CGO-freie Funktionen, per
  `protocol_test.go` vollständig abgedeckt (Roundtrip, Fehlerfälle: falsche Länge).
- `project/go-api/pkg/e2edemo/cansock.go`: dünner Wrapper um einen `AF_CAN`/`SOCK_RAW`-Socket
  (`golang.org/x/sys/unix`) — `Open(ifaceName string) (*Conn, error)`,
  `(*Conn) Send(id uint32, data []byte) error`, `(*Conn) Receive(timeout time.Duration) (id uint32, data []byte, err error)`,
  `(*Conn) Close()`. Baut auf `unix.Socket(AF_CAN, SOCK_RAW, CAN_RAW)` + `unix.BindToDevice`/`SockaddrCAN` auf.
- `project/go-api/go.mod`: `golang.org/x/sys` als direkte Abhängigkeit ergänzen.
- Commit nach dieser Phase.

## Phase 2 — D5: CAN→HAL-Bridge (`can-hal-bridge`)

- `project/go-api/cmd/can-hal-bridge/main.go`: liest `--canif`/`CANHAL_BRIDGE_CANIF`, öffnet
  den CAN-Socket, wartet auf `RequestCANID`, ruft `driver.BME280Read()` auf, sendet
  `ResponseCANID` mit der Temperatur zurück, loggt jede Station.
- `project/go-api/cmd/can-hal-bridge/driver_mock.go` (`//go:build !hwreal`): liefert
  `mockdriver.New()` — Default, kein CGO.
- `project/go-api/cmd/can-hal-bridge/driver_real.go` (`//go:build hwreal`): liefert
  `loader.NewDriver(cfg)` (Backend über `--backend`/`HW_BACKEND`, wie `cmd/main.go`).
- Makefile: `can-hal-bridge` (Mock, `CGO_ENABLED=0`, cross-kompilierbar wie `bbcli-arm`) und
  `can-hal-bridge-hw` (`-tags hwreal`, `CGO_ENABLED=1`, hängt von `c-lib rust-lib` ab).
- Commit nach dieser Phase.

## Phase 3 — D2: REST↔CAN-Gateway (`rest-can-gateway`)

- `project/go-api/cmd/rest-can-gateway/main.go`: HTTP-Server (`net/http`, kein neues
  Framework nötig für eine einzelne Route), `GET /temperature` kodiert die Anfrage, sendet sie
  auf dem konfigurierten CAN-Interface, wartet mit Timeout (Pattern wie bestehende
  Timeout-Handhabung in `pkg/hal/c`/`pru`) auf die Antwort, antwortet mit JSON
  `{"temperature": <float>, "backend": "e2e-demo"}` oder `504` bei Timeout.
- CAN-Transport hinter einem kleinen Interface (`type canTransport interface{ Send(...); Receive(...) }`)
  gekapselt, damit der HTTP-Handler ohne echtes CAN-Interface per `httptest` getestet werden kann
  (Fake-Transport in `main_test.go`).
- Makefile: `rest-can-gateway` (`CGO_ENABLED=0`, wie `rest-can-gateway-arm` optional für ARM).
- Commit nach dieser Phase.

## Phase 4 — Netzwerk-Topologie-Setup-Skript

- `scripts/setup_e2e_demo.sh`: legt `dev1`..`dev5` an (`ip netns add`), verbindet
  D1↔D2 (`veth`, statische IPs `10.270.1.1/30` / `.2/30`), D2↔D3 und D4↔D5 (`vxcan`),
  D3↔D4 (`veth` + `acfcan`-Modul-Setup analog `tests/hardware/test_acfcan.py`, gegenläufig
  gespiegelte Stream-IDs). Startet `can-hal-bridge` (Mock-Default) in `dev5` und
  `rest-can-gateway` in `dev2` im Hintergrund. Gibt am Ende den `curl`-Befehl für `dev1` aus.
  Idempotent/aufräumend wie `setup_acfcan_vcan_demo.sh` (`trap ... EXIT`).
- Commit nach dieser Phase.

## Phase 5 — End-to-End-Test (Hardware, SSH-getrieben)

- `tests/hardware/test_e2e_demo.py`: Analog `test_acfcan.py` — SSH-Fixture baut die Topologie
  per `setup_e2e_demo.sh` auf dem Board auf, Test ruft
  `ip netns exec dev1 curl http://10.270.1.2:8080/temperature` auf und verifiziert, dass der
  Wert exakt `23.45` (Mock-Wert aus `pkg/hal/mock`) innerhalb eines Timeouts zurückkommt.
  Skip-Fixture falls `acfcan`/`vxcan`-Kernelmodule nicht verfügbar sind (wie bei `test_acfcan.py`).
- Commit nach dieser Phase.

## Phase 6 — CI-Pipeline + Doku

- `.drone.yml`: neue Pipeline `e2e-demo-build` (Pfad-getriggert auf
  `project/go-api/pkg/e2edemo/**`, `project/go-api/cmd/can-hal-bridge/**`,
  `project/go-api/cmd/rest-can-gateway/**`, `scripts/setup_e2e_demo.sh`) — baut/testet die
  Mock-Variante (`go build`/`go test`/`go vet`, kein CGO nötig, kein Cross-Compile-Toolchain-Bedarf).
- `Makefile`: `lint`-Target um `pkg/e2edemo` ergänzen, neue Targets in `info`/`.PHONY` aufnehmen.
- `README.md`: neuer Abschnitt unter "IEEE 1722 / ACF-CAN" mit Architekturdiagramm (aus dem
  Issue übernommen), Setup-Befehl, Troubleshooting (Namespace-Reihenfolge, `vxcan`-Modul,
  gespiegelte Stream-IDs).
- Commit nach dieser Phase.

## Akzeptanzkriterien (aus Issue, zu verifizieren)

- End-to-End-Test (Phase 5) verifiziert: Round-Trip-Wert an D1 entspricht exakt dem Wert,
  den D5 lokal vom HAL-Treiber liest.
- Setup-Skript baut alle 5 Namespaces + Links in einem Rutsch auf.
- Dokumentation enthält Architekturdiagramm + Troubleshooting.
