// [SDOC_LINK: SWR-016]
package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"net/http"
	"time"

	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/app"
	"fyne.io/fyne/v2/container"
	"fyne.io/fyne/v2/theme"
	"fyne.io/fyne/v2/widget"
)

const (
	gpioAPIPath    = "/api/v1/gpio/"
	gpioValueHigh  = "HIGH (1)"
	spiModeDefault = "Mode 0"
)

var apiBase = "http://192.168.7.2:5000"

// ── API Helper ───────────────────────────────────────────────────
func apiGet(path string, out interface{}) error {
	resp, err := http.Get(apiBase + path)
	if err != nil {
		return err
	}
	defer resp.Body.Close()
	return json.NewDecoder(resp.Body).Decode(out)
}

func apiPost(path string, in, out interface{}) error {
	body, _ := json.Marshal(in)
	resp, err := http.Post(apiBase+path, "application/json", bytes.NewReader(body))
	if err != nil {
		return err
	}
	defer resp.Body.Close()
	if out != nil {
		return json.NewDecoder(resp.Body).Decode(out)
	}
	return nil
}

// ── Main ─────────────────────────────────────────────────────────
func main() {
	a := app.New()
	a.Settings().SetTheme(theme.DarkTheme())
	w := a.NewWindow("BeagleBone Black Konfigurator")
	w.Resize(fyne.NewSize(900, 700))

	tabs := container.NewAppTabs(
		container.NewTabItem("🌡 BME280", bme280Tab()),
		container.NewTabItem("⚡ GPIO", gpioTab()),
		container.NewTabItem("📡 UART", uartTab()),
		container.NewTabItem("🔌 SPI", spiTab()),
		container.NewTabItem("🔧 Backend", backendTab()),
		container.NewTabItem("🖥 System", systemTab()),
	)
	tabs.SetTabLocation(container.TabLocationLeading)
	w.SetContent(tabs)
	w.ShowAndRun()
}

// ── BME280 Tab ───────────────────────────────────────────────────
func bme280Tab() *fyne.Container {
	tempLabel := widget.NewLabel("-- °C")
	humLabel := widget.NewLabel("-- %")
	pressLabel := widget.NewLabel("-- hPa")
	altLabel := widget.NewLabel("-- m")
	backLabel := widget.NewLabel("--")
	status := widget.NewLabel("")

	for _, l := range []*widget.Label{tempLabel, humLabel, pressLabel, altLabel} {
		l.TextStyle = fyne.TextStyle{Bold: true}
	}

	intervalEntry := widget.NewEntry()
	intervalEntry.SetText("2")
	oversamplingSelect := widget.NewSelect(
		[]string{"x1", "x2", "x4", "x8", "x16"}, nil)
	oversamplingSelect.SetSelected("x1")

	readFn := func() {
		var d map[string]interface{}
		if err := apiGet("/api/v1/bme280", &d); err != nil {
			status.SetText("❌ " + err.Error())
			return
		}
		tempLabel.SetText(fmt.Sprintf("%.2f °C", d["temperature"]))
		humLabel.SetText(fmt.Sprintf("%.2f %%", d["humidity"]))
		pressLabel.SetText(fmt.Sprintf("%.2f hPa", d["pressure"]))
		altLabel.SetText(fmt.Sprintf("%.1f m", d["altitude"]))
		backLabel.SetText(d["backend"].(string))
		status.SetText("✅ Aktualisiert")
	}

	readBtn := widget.NewButton("🔄 Lesen", readFn)
	saveBtn := widget.NewButton("💾 Speichern", func() {
		osMap := map[string]int{"x1": 1, "x2": 2, "x4": 4, "x8": 8, "x16": 16}
		apiPost("/api/v1/bme280/config", map[string]interface{}{
			"interval":     intervalEntry.Text,
			"oversampling": osMap[oversamplingSelect.Selected],
		}, nil)
		status.SetText("✅ Konfiguration gespeichert")
	})

	// Auto-Refresh
	go func() {
		for range time.Tick(2 * time.Second) {
			readFn()
		}
	}()

	return container.NewVBox(
		widget.NewCard("Messwerte", "",
			container.NewGridWithColumns(2,
				widget.NewLabel("Temperatur:"), tempLabel,
				widget.NewLabel("Luftfeuchtigkeit:"), humLabel,
				widget.NewLabel("Luftdruck:"), pressLabel,
				widget.NewLabel("Höhe:"), altLabel,
				widget.NewLabel("Backend:"), backLabel,
			)),
		widget.NewCard("Konfiguration", "",
			container.NewVBox(
				widget.NewLabel("Messintervall (Sekunden):"),
				intervalEntry,
				widget.NewLabel("Oversampling:"),
				oversamplingSelect,
			)),
		container.NewHBox(readBtn, saveBtn),
		status,
	)
}

// ── GPIO Tab ─────────────────────────────────────────────────────
func gpioTab() *fyne.Container {
	pinEntry := widget.NewEntry()
	pinEntry.SetPlaceHolder("z.B. 60")
	dirSelect := widget.NewSelect([]string{"out", "in"}, nil)
	dirSelect.SetSelected("out")
	valSelect := widget.NewSelect([]string{gpioValueHigh, "LOW (0)"}, nil)
	valSelect.SetSelected(gpioValueHigh)
	status := widget.NewLabel("")

	configBtn := widget.NewButton("⚙️ Konfigurieren", func() {
		pin := pinEntry.Text
		if pin == "" {
			status.SetText("❌ Pin eingeben!")
			return
		}
		apiPost(gpioAPIPath+pin+"/export", nil, nil)
		apiPost(gpioAPIPath+pin+"/direction",
			map[string]string{"direction": dirSelect.Selected}, nil)
		status.SetText(fmt.Sprintf("✅ Pin %s → %s", pin, dirSelect.Selected))
	})

	setBtn := widget.NewButton("🔌 Setzen", func() {
		pin := pinEntry.Text
		if pin == "" {
			status.SetText("❌ Pin eingeben!")
			return
		}
		val := 0
		if valSelect.Selected == gpioValueHigh {
			val = 1
		}
		apiPost(gpioAPIPath+pin,
			map[string]interface{}{"value": val, "backend": "auto"}, nil)
		status.SetText(fmt.Sprintf("✅ Pin %s = %d", pin, val))
	})

	return container.NewVBox(
		widget.NewCard("GPIO Steuerung", "",
			container.NewVBox(
				widget.NewLabel("Pin Nummer:"), pinEntry,
				widget.NewLabel("Richtung:"), dirSelect,
				widget.NewLabel("Wert:"), valSelect,
			)),
		container.NewHBox(configBtn, setBtn),
		status,
	)
}

// ── UART Tab ─────────────────────────────────────────────────────
func uartTab() *fyne.Container {
	portSelect := widget.NewSelect([]string{
		"/dev/ttyO1", "/dev/ttyO2", "/dev/ttyO4", "/dev/ttyO5"}, nil)
	portSelect.SetSelected("/dev/ttyO1")
	baudSelect := widget.NewSelect([]string{
		"9600", "19200", "38400", "57600", "115200"}, nil)
	baudSelect.SetSelected("115200")
	sendEntry := widget.NewEntry()
	sendEntry.SetPlaceHolder("Nachricht...")
	rxLabel := widget.NewLabel("RX: --")
	status := widget.NewLabel("")

	return container.NewVBox(
		widget.NewCard("UART Konfiguration", "",
			container.NewVBox(
				widget.NewLabel("Port:"), portSelect,
				widget.NewLabel("Baudrate:"), baudSelect,
			)),
		widget.NewButton("💾 Konfigurieren", func() {
			var baud int
			fmt.Sscanf(baudSelect.Selected, "%d", &baud)
			apiPost("/api/v1/uart/config",
				map[string]interface{}{"port": portSelect.Selected, "baud": baud}, nil)
			status.SetText(fmt.Sprintf("✅ %s @ %s", portSelect.Selected, baudSelect.Selected))
		}),
		widget.NewCard("Daten", "",
			container.NewVBox(
				widget.NewLabel("Senden:"), sendEntry,
				container.NewHBox(
					widget.NewButton("📤 Senden", func() {
						apiPost("/api/v1/uart/send",
							map[string]string{"data": sendEntry.Text}, nil)
						status.SetText("✅ Gesendet: " + sendEntry.Text)
					}),
					widget.NewButton("📥 Empfangen", func() {
						var d map[string]interface{}
						apiGet("/api/v1/uart/receive?timeout=1000", &d)
						if d["data"] != nil {
							rxLabel.SetText("RX: " + fmt.Sprintf("%v", d["data"]))
						}
					}),
				),
				rxLabel,
			)),
		status,
	)
}

// ── SPI Tab ──────────────────────────────────────────────────────
func spiTab() *fyne.Container {
	deviceSelect := widget.NewSelect([]string{
		"/dev/spidev0.0", "/dev/spidev0.1", "/dev/spidev1.0"}, nil)
	deviceSelect.SetSelected("/dev/spidev0.0")
	speedEntry := widget.NewEntry()
	speedEntry.SetText("1000000")
	modeSelect := widget.NewSelect([]string{
		spiModeDefault, "Mode 1", "Mode 2", "Mode 3"}, nil)
	modeSelect.SetSelected(spiModeDefault)
	txEntry := widget.NewEntry()
	txEntry.SetPlaceHolder("Hex z.B. 0102FF")
	rxLabel := widget.NewLabel("RX: --")
	status := widget.NewLabel("")

	return container.NewVBox(
		widget.NewCard("SPI Konfiguration", "",
			container.NewVBox(
				widget.NewLabel("Device:"), deviceSelect,
				widget.NewLabel("Speed (Hz):"), speedEntry,
				widget.NewLabel("Mode:"), modeSelect,
			)),
		widget.NewButton("💾 Konfigurieren", func() {
			var speed, mode int
			fmt.Sscanf(speedEntry.Text, "%d", &speed)
			for i, m := range []string{spiModeDefault, "Mode 1", "Mode 2", "Mode 3"} {
				if m == modeSelect.Selected {
					mode = i
				}
			}
			apiPost("/api/v1/spi/config", map[string]interface{}{
				"device": deviceSelect.Selected, "speed": speed, "mode": mode}, nil)
			status.SetText("✅ SPI konfiguriert")
		}),
		widget.NewCard("Transfer", "",
			container.NewVBox(
				widget.NewLabel("TX (Hex):"), txEntry,
				widget.NewButton("🔄 Transfer", func() {
					var speed int
					fmt.Sscanf(speedEntry.Text, "%d", &speed)
					var d map[string]interface{}
					apiPost("/api/v1/spi/transfer", map[string]interface{}{
						"device": deviceSelect.Selected,
						"speed":  speed, "tx": []byte(txEntry.Text)}, &d)
					rxLabel.SetText(fmt.Sprintf("RX: %v", d["rx_buf"]))
				}),
				rxLabel,
			)),
		status,
	)
}

// ── Backend Tab ──────────────────────────────────────────────────
func backendTab() *fyne.Container {
	status := widget.NewLabel("Aktuelles Backend: --")
	status.TextStyle = fyne.TextStyle{Bold: true}

	go func() {
		var d map[string]interface{}
		if apiGet("/health", &d) == nil && d["backend"] != nil {
			status.SetText("Backend: " + d["backend"].(string) +
				"  |  Driver: " + d["driver"].(string))
		}
	}()

	mkBtn := func(label, backend string) *widget.Button {
		return widget.NewButton(label, func() {
			apiPost("/api/v1/backend",
				map[string]string{"backend": backend}, nil)
			status.SetText("✅ Backend: " + backend)
		})
	}

	return container.NewVBox(
		widget.NewCard("HAL Backend auswählen", "",
			container.NewVBox(
				status,
				container.NewHBox(
					mkBtn("⚙️ C Library", "c"),
					mkBtn("🦀 Rust Library", "rust"),
					mkBtn("🔄 Auto Fallback", "auto"),
				),
			)),
	)
}

// ── System Tab ───────────────────────────────────────────────────
func systemTab() *fyne.Container {
	statusLabel := widget.NewLabel("--")

	refreshFn := func() {
		var d map[string]interface{}
		if err := apiGet("/health", &d); err != nil {
			statusLabel.SetText("❌ Offline: " + err.Error())
			return
		}
		statusLabel.SetText(fmt.Sprintf(
			"✅ Online | Backend: %s | Driver: %s | Arch: %s",
			d["backend"], d["driver"], d["arch"]))
	}

	go func() {
		for range time.Tick(5 * time.Second) {
			refreshFn()
		}
	}()
	refreshFn()

	return container.NewVBox(
		widget.NewCard("System Status", "",
			container.NewVBox(
				statusLabel,
				container.NewHBox(
					widget.NewButton("🔄 Aktualisieren", refreshFn),
					widget.NewButton("🔄 Neu starten", func() {
						http.Post(apiBase+"/api/v1/system/restart",
							"application/json", nil)
						statusLabel.SetText("🔄 Neustart eingeleitet...")
					}),
				),
			)),
	)
}
