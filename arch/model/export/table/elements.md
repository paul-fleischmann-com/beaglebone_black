### All Elements

| Element | Kind | Technology | Description |
|---------|------|------------|-------------|
| bbcli | client_tool | Go 1.23 / Cobra + Viper | Kommandozeilen-Tool für direkte API-Interaktion; Subcommands: bme280, gpio, backend, system, completion. Cross-compiled für Linux amd64/arm. Quelle: tools/cli/ |
| bbgui | client_tool | Go / Fyne v2 | Desktop-GUI Anwendung mit grafischer Darstellung der Sensordaten; Tabs für BME280, GPIO, UART, SPI, Backend, System. Quelle: tools/desktop-gui/main.go |
| bbtui | client_tool | Go 1.24 / BubbleTea + Lipgloss | Interaktives Terminal-UI für Echtzeit-Anzeige von Sensordaten; Tabs 1-6, automatischer BME280-Refresh alle 2s. Quelle: tools/tui/main.go |
| BeagleBone Black Embedded SW | system |  | Embedded Linux Software auf TI AM335x ARM Cortex-A8 (1 GHz, 512 MB DDR3L RAM) |
| C Hardware Library | library | C / arm-linux-gnueabihf-gcc | Cross-kompilierte Shared Library (libhardware.so). Quellen: c-lib/ (Makefile-Target: make c-lib). Kopiert nach project/go-api/libs/ |
| BME280 Treiber (C) | component | C / I2C ioctl | Liest Temperatur, Luftfeuchtigkeit, Druck und Höhe via I2C-1 (Adresse 0x76). Bosch-Kompensationsalgorithmus. Quelle: project/c/src/bme280.c |
| GPIO Treiber (C) | component | C / sysfs /sys/class/gpio | Export, Richtungskonfiguration, Lesen und Schreiben von GPIO-Pins via sysfs. Quelle: project/c/src/gpio.c |
| SPI Treiber (C) | component | C / spidev ioctl | Bidirektionaler Datentransfer über SPI mit konfigurierbarer Geschwindigkeit (Mode 0-3). Quelle: project/c/src/spi.c |
| UART Treiber (C) | component | C / termios | Öffnen, Konfigurieren (Port, Baudrate), Senden und Empfangen via serieller Schnittstelle. Quelle: project/c/src/uart.c |
| REST API Server | container | Go 1.23 / gorilla/mux | HTTP-Server auf Port 5000; verarbeitet Anfragen und delegiert an HAL. Binary: bin/embedded. Quelle: project/go-api/ |
| API Handler | component | Go / gorilla/mux | HTTP-Handler-Methoden auf Server-Struct: HealthHandler, BME280Handler, BME280StreamHandler, GPIOAllHandler, GPIOReadHandler, GPIOWriteHandler, UARTConfigHandler, UARTSendHandler, UARTReceiveHandler, SPITransferHandler. Zusätzlich backendHandler (POST /api/v1/backend) für Laufzeit-Backend-Wechsel in project/go-api/cmd/main.go. Quelle: project/go-api/pkg/api/handlers.go |
| HTTP Server | component | Go / net/http | Server-Struct (HW HardwareDriver, HWMu *sync.Mutex), CORSMiddleware (Access-Control-Allow-Origin: *), NewHTTPServer mit konfigurierten Timeouts (Read: 10s, Write: 30s, Idle: 60s). Quelle: project/go-api/pkg/api/server.go |
| Hardware Abstraction Layer (HAL) | component | Go Interface | HardwareDriver Interface mit 14 Methoden: Name, Backend, BME280Read, GPIOExport, GPIOSetDirection, GPIORead, GPIOWrite, UARTOpen, UARTWrite, UARTRead, UARTClose, SPITransfer, Init, Close. Datentypen: BME280Data, GPIOData, UARTData, SPIData. Quelle: project/go-api/pkg/hal/interface.go |
| Auto Driver | component | Go / Decorator Pattern | Decorator über C- und Rust-Driver (autoDriver struct). Bei Init werden beide Backends sofort initialisiert; C ist primär, Rust ist Backup. Bei Fehler jeder der 14 HardwareDriver-Methoden transparenter Fallback auf Rust. Quelle: project/go-api/pkg/hal/loader/factory.go |
| C Driver | component | Go / CGO | Implementiert HardwareDriver via CGO-Bindings zur libhardware.so. Höchste Performance. Quelle: project/go-api/pkg/hal/c/driver.go |
| HAL Konfiguration | component | Go / os.Getenv | Config-Struct und Umgebungsvariablen-Loader. Felder: Backend (HW_BACKEND, default: auto), I2CBus (HW_I2C, default: /dev/i2c-1), BME280Addr (0x76), UARTPort (HW_UART, default: /dev/ttyO1), UARTBaud (115200), SPIDevice (/dev/spidev0.0), SPISpeed (1000000), Timeout (10s). Quelle: project/go-api/pkg/hal/config/config.go |
| Backend Factory | component | Go / Factory Pattern | NewDriver(cfg): erzeugt C-, Rust- oder Auto-Driver anhand von HW_BACKEND. Separates Package pkg/hal/loader/ zur Vermeidung von Import-Zyklen (pkg/hal/c importiert pkg/hal). Quelle: project/go-api/pkg/hal/loader/factory.go |
| Mock Driver | component | Go | Vollständige HardwareDriver-Implementierung für Unit-Tests ohne echte Hardware. Gibt statische Testwerte zurück. Bietet WasCalled() und Reset() für Testassertions. Quelle: project/go-api/pkg/hal/mock/driver.go |
| Rust Driver | component | Go / FFI (extern C) | Implementiert HardwareDriver via FFI-Bindings zur libhardware_rs.so. Memory-Safe. Quelle: project/go-api/pkg/hal/rust/driver.go |
| Hardware Interfaces | component | BeagleBone Black / Linux Kernel Interfaces | Physische Schnittstellen des TI AM335x Prozessors auf dem BeagleBone Black |
| BME280 Sensor | hardware | I2C-1 (/dev/i2c-1), Adresse 0x76 | Temperatur (-40..+85°C), Luftfeuchtigkeit (0-100% rH), Luftdruck (300-1100 hPa). P9_19 (I2C2_SCL), P9_20 (I2C2_SDA), P9_3 (3.3V), P9_1 (GND), SDO→GND |
| GPIO Pins | hardware | Linux sysfs /sys/class/gpio | Digitale Ein-/Ausgänge über P8/P9 Header. Export via /sys/class/gpio/export, Richtung via direction, Wert via value |
| SPI Bus | hardware | /dev/spidev0.0 / spidev ioctl | SPI Full-Duplex Transfer, Mode 0-3, bis 48 MHz. P9_22 (SCLK), P9_21 (MISO), P9_18 (MOSI) |
| UART / Serial | hardware | /dev/ttyO1 / termios | Serielle Schnittstelle, 115200 baud (default). P9_24 (TX), P9_26 (RX) |
| Rust Hardware Library | library | Rust / armv7-unknown-linux-musleabihf (musl) | Cross-kompilierte Shared Library (libhardware_rs.so). Memory-Safe Alternative zur C-Lib. Target: armv7-unknown-linux-musleabihf. Quelle: project/rust-lib/ |
| BME280 Treiber (Rust) | component | Rust / linux-embedded-hal, bme280 crate | Memory-safe BME280 via I2C. FFI-Export: rs_bme280_read(i2c_path, addr) → RsBme280Data. Quelle: project/rust-lib/src/bme280.rs |
| GPIO Treiber (Rust) | component | Rust / std::fs (sysfs) | GPIO-Steuerung mit Rust Memory-Safety. FFI-Exports: rs_gpio_export, rs_gpio_set_direction, rs_gpio_read, rs_gpio_write. Quelle: project/rust-lib/src/gpio.rs |
| SPI Treiber (Rust) | component | Rust / spidev crate | SPI Full-Duplex Transfer. FFI-Export: rs_spi_transfer(dev, speed, tx_ptr, len) → RsSpiData. Quelle: project/rust-lib/src/spi.rs |
| UART Treiber (Rust) | component | Rust / serialport crate | Serielle Kommunikation. FFI-Exports: rs_uart_open, rs_uart_write, rs_uart_read, rs_uart_close. Quelle: project/rust-lib/src/uart.rs |
| Entwickler / Operator | actor |  | Entwickelt, baut und deployt das System; überwacht Hardware-Sensoren |
| Web Dashboard | client_tool | HTML / Vanilla JavaScript / SSE | Browser-basiertes Dashboard für Sensor-Visualisierung und GPIO-Steuerung via SSE-Stream. Quelle: tools/web-gui/ |
