# Issue #252: Software auf PRU-Cores (PRU-ICSS) auslagern für Echtzeit-Hardwarezugriff

## Feasibility-Analyse / Use-Case (Schritt 1)

Als MVP wird **kein** neuer Sensor-Treiber auf die PRU verlagert (BME280 läuft über I2C mit
Hardware-Controller, kein Bit-Banging nötig — PRU bringt hier keinen Vorteil). Stattdessen wird
der von Issue #252 selbst vorgeschlagene Schritt 2 ("minimales Hello-World-PRU-Programm, GPIO
togglen, zum Verifizieren der Kette") umgesetzt und um einen echten Kommunikationskanal
erweitert:

**PRU1 empfängt GPIO-Kommandos (SET/GET auf ein R30/R31-Bit) per RPMsg von Linux und
antwortet mit dem Ergebnis.** Das validiert die komplette Kette Toolchain → Firmware →
remoteproc-Laden → rpmsg-Kommunikation → Go-HAL-Backend end-to-end, ohne einen einzelnen
Sensor-Anwendungsfall vorwegzunehmen. Zukünftige zeitkritische Treiber (WS2812, Encoder,
eigene Bit-Bang-Protokolle) können auf dieser Kommunikationsschicht aufsetzen.

Getroffene technische Entscheidungen (abweichend von reinen TI-CCS-Beispielen):
- **Toolchain:** GNU-PRU-Toolchain (`dinuxbg/gnupru`, `pru-elf-gcc`) statt TI PRU-CGT — frei
  verfügbar als Prebuilt-Release-Tarball, kein Lizenz-Download-Formular nötig.
- **PSSP:** GCC-portierter Fork `dinuxbg/pru-software-support-package` (enthält
  `pru_rpmsg.c`/`pru_virtqueue.c` + Header, kompatibel mit GNU-PRU-Toolchain). Wird als
  Build-Abhängigkeit per Git-Clone geladen (analog zu Unity in `c-lib/Makefile`), nicht ins
  Repo vendored (zu groß, Fremdcode).
- **Firmware-Basis:** TI's offizielles `PRU_RPMsg_Echo_Interrupt1`-Beispiel (BSD-3-Clause,
  PRU1, System-Events 18/19) wurde erfolgreich mit der GNU-Toolchain kompiliert (ELF mit
  korrekt platzierten `.resource_table`/`.pru_irq_map`-Sections verifiziert) und dient als
  Basis für `main.c` — Payload-Interpretation wurde von "Echo" auf ein eigenes
  GPIO-Kommandoprotokoll umgestellt.
- **Pin-Konflikt:** GPIO3_21 (HDMI-Audio-Takt, siehe
  `specs/hw/BeagleBone/Black/06_detailed_hardware_design.md:160`) wird nicht verwendet.
  Die konkrete Zuordnung eines physischen P8/P9-Headerpins zum PRU1-R30/R31-Bit (Pinmux-Mode)
  ist **nicht** Teil dieses MVP — das RPMsg-Kommandoprotokoll selbst benötigt keinen extern
  gemuxten Pin (PRUSS-interne Interrupts/Shared-Memory). Vor physischer Verdrahtung eines
  Ausgangs muss der gewünschte Pin gegen die AM335x-TRM-Pinmux-Tabelle verifiziert werden.

## Phase 1 — PRU-Toolchain-Setup
- `scripts/setup_pru_toolchain.sh`: lädt das Prebuilt-Release
  `pru-elf-*.amd64.tar.xz` von `dinuxbg/gnupru` nach `toolchain/pru/gnupru/`, klont
  `dinuxbg/pru-software-support-package` (flach) nach `toolchain/pru/pssp/`. Idempotent
  (Skip falls vorhanden), analog zu `clone_layer()` in `scripts/build_yocto.sh`.

## Phase 2 — PRU1-Firmware
- `project/pru/fw/pru1_gpio_ctrl/`: `main.c` (RPMsg-Transport-Setup + Kommandoschleife:
  Opcode `SET`/`GET` auf `__R30`/`__R31`-Bit 0–15), `resource_table.h`, `intc_map_1.h`
  (adaptiert von TIs BSD-3-Clause-Referenz, System-Events 18/19 für PRU1), `Makefile`
  (`pru-gcc -mmcu=am335x.pru1`, `PSSP_DIR` überschreibbar).
- `scripts/build_pru_firmware.sh`: ruft bei Bedarf Phase 1 auf, baut die Firmware, kopiert
  `.elf` nach `bin/pru/bbb-pru1-gpio-ctrl.elf`.

## Phase 3 — Host-Kommunikationsschicht (C)
- `project/c/include/pru.h` + `project/c/src/pru.c`: `pru_load()`/`pru_stop()`
  (remoteproc-sysfs: `/sys/class/remoteproc/remoteprocN/{firmware,state}`), `pru_open()`
  (findet das passende `/dev/rpmsgN` **nicht** über einen festen Pfad, sondern per
  Sysfs-Scan `/sys/class/rpmsg/rpmsg*/{name,src}` nach Kanalname `rpmsg-raw` +
  Port 31 — korrigiert gegenüber der Issue-Beschreibung `/dev/rpmsg_pruX`: der
  Mainline-`rpmsg_char`-Treiber vergibt fortlaufende `/dev/rpmsg<N>`-Nodes, kein
  PRU-spezifisches Naming, siehe `drivers/rpmsg/rpmsg_char.c`),
  `pru_gpio_set()`/`pru_gpio_get()` (4-Byte Kommandoprotokoll,
  `project/c/include/pru_protocol.h`). In `c-lib/Makefile` SRCS ergänzt.
- Error-Path-Tests in `project/c/test/test_c_lib.c` (CI ohne Hardware: Fehlschlag ohne
  `/sys/class/remoteproc`/`/dev/rpmsg_*` erwartet, analog GPIO/UART-Tests).

## Phase 4 — HAL-Backend `pru`
- `interface.go`: `BackendPRU Backend = "pru"`.
- `pkg/hal/pru/driver.go`: CGO-Bindings an `pru.c` (via `libhardware.so`). `GPIOExport`,
  `GPIOSetDirection`, `GPIORead`, `GPIOWrite` real (Pin = R30/R31-Bit 0–15, nicht
  Linux-Sysfs-GPIO-Nummer — Semantikunterschied dokumentiert). `BME280Read`/`UART*`/
  `SPITransfer` liefern `nicht unterstützt`-Fehler (PRU-Backend deckt nur deterministisches
  GPIO ab).
- `factory.go`: `case "pru"`. Kein Teil von `auto` (bleibt C→Rust-Fallback).
- `config.go`: `HW_PRU_CORE` (Default `1`), `HW_PRU_RPMSG_PORT` (Default `31`, für den
  Sysfs-Scan), `HW_PRU_FIRMWARE` (Default `bbb-pru1-gpio-ctrl.elf`).

## Phase 5 — Yocto-Integration
- `meta-bbb-sensors/recipes-kernel/linux/files/bbb-pruss.cfg`: `CONFIG_REMOTEPROC`,
  `CONFIG_TI_PRUSS`, `CONFIG_RPMSG_CHAR`, `CONFIG_RPMSG_VIRTIO`.
- `meta-bbb-sensors/recipes-bsp/device-tree/bbb-pruss-overlay/`: DT-Overlay adaptiert von
  `beagleboard/bb.org-overlays` (`AM335X-PRU-RPROC-4-19-TI-00A0.dts`, GPL-2.0, verifizierte
  PRUSS/PRU0/PRU1-Remoteproc-Nodes inkl. IRQ-Mapping).
- `meta-bbb-sensors/recipes-bbb/pru-fw/pru-fw_1.0.bb`: `SRC_URI` lädt GNU-PRU-Toolchain +
  PSSP-Fork zur Fetch-Zeit (kein Netzwerk in `do_compile`, Yocto-Netzwerk-Sandbox-konform),
  baut `project/pru`-Firmware, installiert nach `/lib/firmware/`.
- `scripts/build_yocto.sh`: keine Änderung nötig (Rezept ist selbstständig).

## Phase 6 — CI
- Neue schnelle Drone-Pipeline `build-pru-firmware` (Trigger `push`/`pull_request`, kein
  Nightly nötig — Compile-Check dauert Sekunden): führt `scripts/build_pru_firmware.sh` aus.
  Kann PRU-Timing/GPIO **nicht** funktional testen (keine Hardware in CI), nur Kompilierbarkeit
  sichern.

## Phase 7 — Tests & Doku
- `tests/hardware/test_pru.py`: `BEAGLE_HOST`-gated, testet `/api/v1/gpio/{bit}` mit
  `HW_BACKEND=pru`.
- `Makefile`: Target `pru-fw`.
- `CLAUDE.md`: Key-Files-Tabelle + Build-Commands ergänzt.
- `README.md`: HAL-Backend-Tabelle um `pru` ergänzt.
- `CHANGELOG.md`: Eintrag.

## Akzeptanzkriterien (aus Issue #252, MVP-Scope)
1. Toolchain-Kette lokal nutzbar, Hello-World-Kommunikation (GPIO-Kommando per RPMsg) als
   Firmware-Quelltext vorhanden und **kompiliert** (mit echtem GNU-PRU-Compiler verifiziert).
2. remoteproc/rpmsg Kernel-Konfiguration + DT-Overlay für PRUSS in `meta-bbb-sensors` ergänzt.
3. Neue Kommunikationsschicht (C) für Linux↔PRU vorhanden.
4. Neuer HAL-Backend `pru` in `interface.go`/`factory.go`, kein direkter Hardware-Zugriff aus
   Go (Rule eingehalten).
5. Yocto-Rezept für PRU-Firmware vorhanden.
6. Funktionale Tests nur auf echter Hardware möglich (dokumentiert, Stub in
   `tests/hardware/`) — CI prüft nur Kompilierbarkeit, kein Determinismus-Nachweis ohne BBB.
7. Doku ergänzt.

## Bekannte Einschränkungen
- Kein Zugriff auf reale BeagleBone-Black-Hardware in dieser Umgebung — remoteproc-Laden,
  rpmsg-Kommunikation und GPIO-Timing sind **nicht** auf echtem Gerät verifiziert, nur die
  Firmware-Kompilierung. Vor Produktivnutzung: Deploy + Test gegen `192.168.7.2` nachholen.
- Physischer Pin (P8/P9-Header) für das GPIO-Kommando ist nicht final festgelegt (siehe
  Feasibility-Analyse) — nur die PRUSS-interne RPMsg-Kommunikation ist Gegenstand des MVP.
