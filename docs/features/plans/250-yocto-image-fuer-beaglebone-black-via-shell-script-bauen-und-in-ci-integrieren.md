# Issue #250: Yocto-Image für BeagleBone Black via Shell-Script + CI

## Ziel
Ein Shell-Script baut ein Yocto-Image für die BeagleBone Black (Kirkstone, `beaglebone-yocto`
Machine). Das Script bindet einen eigenen Meta-Layer ein, der die BME280-Sensor-Software
(I2C-1, Adresse 0x76, siehe README) als Yocto-Recipe bereitstellt. Der Build wird als
Drone-CI-Pipeline verdrahtet.

## Phase 1 — Meta-Layer `meta-bbb-sensors`
- `project/yocto/meta-bbb-sensors/conf/layer.conf`
- `recipes-bbb/bme280-driver/bme280-driver_1.0.bb` — baut die vorhandenen BME280-C-Quellen
  (`project/c/src/bme280.c`, `project/c/include/bme280*.h`) als Ziel-Shared-Lib + Smoke-Test-
  Binary (Cross-Recipe, kein neuer Treiber-Code — die Hardware-Logik existiert bereits in C).
- `recipes-kernel/linux/linux-yocto-%.bbappend` + `bbb-bme280.cfg` — Kernel-Fragment aktiviert
  `CONFIG_I2C_OMAP`, `CONFIG_BME280`, `CONFIG_BME280_I2C`.
- `recipes-bsp/device-tree/bbb-bme280-overlay` — Overlay aktiviert I2C1 + BME280@0x76 im DT.
- `recipes-core/images/bbb-sensor-image.bb` — `core-image-minimal` + BME280-Paket + i2c-tools.

## Phase 2 — `scripts/build_yocto.sh`
- Idempotentes Klonen von poky/meta-openembedded/meta-arm/meta-ti (kirkstone), Skip falls
  Verzeichnis existiert.
- `oe-init-build-env`, `local.conf` (MACHINE, DL_DIR, SSTATE_DIR, INHERIT rm_work).
- `bitbake-layers add-layer` für Standard-Layer + eigenen `meta-bbb-sensors`-Layer.
- `bitbake $IMAGE` (Default `bbb-sensor-image`, überschreibbar).
- Env-Var-Defaults nach Projektkonvention (`${VAR:-default}`, siehe `scripts/build-arm.sh`).

## Phase 3 — Drone-Pipeline `build-yocto-image`
- Trigger: `cron: [nightly]` + `custom` (kein `push`/`pull_request` — Yocto-Build dauert
  Stunden, das würde jeden Push blockieren; Konvention siehe `nightly-hardware-regression`).
- Step führt `scripts/build_yocto.sh` aus, `save-results` Step wie in anderen Pipelines.
- Beachte Projekt-Konventionen: `$VAR` statt `${VAR}` in unquotierten `command`-Feldern,
  `-p "$TOKEN"` statt `--password-stdin`.
- `.drone.yml` mit `scripts/validate-drone-yml.sh` prüfen.

## Phase 4 — Doku & Konsistenz
- `Makefile`: Target `yocto-image` → `./scripts/build_yocto.sh`.
- `README.md`: neue Sektion "Yocto Image" (Build-Befehl, Layer-Übersicht).
- `.github/workflows/yocto-bbb.yml` prüfen: bleibt als schneller GH-Actions-Referenzbuild
  bestehen, wird aber nicht dupliziert gepflegt — Kommentar-Hinweis auf `scripts/build_yocto.sh`
  als Source of Truth für Layer-Liste.

## Akzeptanzkriterien (aus Issue #250)
1. Shell-Script baut Yocto-Image lokal ausführbar.
2. BME280-Layer ist Teil des Scripts/Images.
3. Drone-CI-Pipeline vorhanden und valide (`validate-drone-yml.sh`, `check-drone-yml`).
4. Doku ergänzt.
