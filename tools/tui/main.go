package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"os"
	"strings"
	"time"

	tea "github.com/charmbracelet/bubbletea"
	"github.com/charmbracelet/lipgloss"
)

const colorPrimary = "#38bdf8"

// ── Styles ───────────────────────────────────────────────────────
var (
	titleStyle = lipgloss.NewStyle().
			Bold(true).
			Foreground(lipgloss.Color(colorPrimary)).
			BorderStyle(lipgloss.RoundedBorder()).
			BorderForeground(lipgloss.Color("#334155")).
			Padding(0, 1)

	cardStyle = lipgloss.NewStyle().
			BorderStyle(lipgloss.RoundedBorder()).
			BorderForeground(lipgloss.Color("#334155")).
			Padding(1, 2).
			Margin(0, 1)

	activeTabStyle = lipgloss.NewStyle().
			Bold(true).
			Foreground(lipgloss.Color(colorPrimary)).
			BorderBottom(true).
			BorderStyle(lipgloss.NormalBorder()).
			BorderForeground(lipgloss.Color(colorPrimary)).
			Padding(0, 2)

	inactiveTabStyle = lipgloss.NewStyle().
				Foreground(lipgloss.Color("#64748b")).
				Padding(0, 2)

	successStyle = lipgloss.NewStyle().Foreground(lipgloss.Color("#22c55e"))
	errorStyle   = lipgloss.NewStyle().Foreground(lipgloss.Color("#ef4444"))
	labelStyle   = lipgloss.NewStyle().Foreground(lipgloss.Color("#94a3b8"))
)

var apiBase = "http://192.168.7.2:5000"

// ── Tab Enum ─────────────────────────────────────────────────────
type tabID int

const (
	tabBME280 tabID = iota
	tabGPIO
	tabUART
	tabSPI
	tabBackend
	tabSystem
)

// ── Datenstrukturen ──────────────────────────────────────────────
type bme280Data struct {
	Temperature float64 `json:"temperature"`
	Humidity    float64 `json:"humidity"`
	Pressure    float64 `json:"pressure"`
	Altitude    float64 `json:"altitude"`
	Backend     string  `json:"backend"`
}

// ── Messages ─────────────────────────────────────────────────────
type bme280Msg bme280Data
type statusMsg struct {
	text string
	ok   bool
}
type tickMsg time.Time

// ── Model ────────────────────────────────────────────────────────
type model struct {
	activeTab tabID
	bme280    bme280Data
	status    string
	statusOK  bool
	backend   string
	gpioPin   string
	width     int
	height    int
}

func initialModel() model {
	return model{activeTab: tabBME280, backend: "auto"}
}

// ── API Helper ───────────────────────────────────────────────────
// [SDOC_LINK: SWR-015]
func apiGet(path string, out interface{}) error {
	resp, err := http.Get(apiBase + path)
	if err != nil {
		return err
	}
	defer resp.Body.Close()
	return json.NewDecoder(resp.Body).Decode(out)
}

// ── Commands ─────────────────────────────────────────────────────
func fetchBME280() tea.Cmd {
	return func() tea.Msg {
		var d bme280Data
		if err := apiGet("/api/v1/bme280", &d); err != nil {
			return statusMsg{"❌ BME280 Fehler: " + err.Error(), false}
		}
		return bme280Msg(d)
	}
}

func setBackendCmd(backend string) tea.Cmd {
	return func() tea.Msg {
		resp, err := http.Post(
			apiBase+"/api/v1/backend",
			"application/json",
			strings.NewReader(`{"backend":"`+backend+`"}`),
		)
		if err != nil {
			return statusMsg{"❌ Backend Fehler", false}
		}
		resp.Body.Close()
		return statusMsg{"✅ Backend → " + backend, true}
	}
}

func tickEvery(d time.Duration) tea.Cmd {
	return tea.Tick(d, func(t time.Time) tea.Msg { return tickMsg(t) })
}

// ── Init ─────────────────────────────────────────────────────────
func (m model) Init() tea.Cmd {
	return tea.Batch(fetchBME280(), tickEvery(2*time.Second))
}

// ── Update ───────────────────────────────────────────────────────
func (m model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	switch msg := msg.(type) {

	case tea.WindowSizeMsg:
		m.width = msg.Width
		m.height = msg.Height

	case tickMsg:
		return m, tea.Batch(fetchBME280(), tickEvery(2*time.Second))

	case bme280Msg:
		m.bme280 = bme280Data(msg)
		m.status = "✅ Aktualisiert"
		m.statusOK = true

	case statusMsg:
		m.status = msg.text
		m.statusOK = msg.ok

	case tea.KeyMsg:
		switch msg.String() {
		case "q", "ctrl+c":
			return m, tea.Quit
		case "1":
			m.activeTab = tabBME280
		case "2":
			m.activeTab = tabGPIO
		case "3":
			m.activeTab = tabUART
		case "4":
			m.activeTab = tabSPI
		case "5":
			m.activeTab = tabBackend
		case "6":
			m.activeTab = tabSystem
		case "tab":
			m.activeTab = (m.activeTab + 1) % 6
		case "r":
			return m, fetchBME280()
		case "c":
			if m.activeTab == tabBackend {
				m.backend = "c"
				return m, setBackendCmd("c")
			}
		case "R":
			if m.activeTab == tabBackend {
				m.backend = "rust"
				return m, setBackendCmd("rust")
			}
		case "a":
			if m.activeTab == tabBackend {
				m.backend = "auto"
				return m, setBackendCmd("auto")
			}
		}
	}
	return m, nil
}

// ── View ─────────────────────────────────────────────────────────
func (m model) View() string {
	var sb strings.Builder

	// Titel
	sb.WriteString(titleStyle.Render("🤖 BeagleBone Black TUI") + "\n")

	// Tabs
	tabs := []string{"1:BME280", "2:GPIO", "3:UART", "4:SPI", "5:Backend", "6:System"}
	tabRow := ""
	for i, t := range tabs {
		if tabID(i) == m.activeTab {
			tabRow += activeTabStyle.Render(t)
		} else {
			tabRow += inactiveTabStyle.Render(t)
		}
	}
	sb.WriteString(tabRow + "\n\n")

	// Tab Inhalt
	switch m.activeTab {
	case tabBME280:
		sb.WriteString(m.bme280View())
	case tabGPIO:
		sb.WriteString(m.gpioView())
	case tabBackend:
		sb.WriteString(m.backendView())
	default:
		sb.WriteString(cardStyle.Render(labelStyle.Render("In Entwicklung...")))
	}

	// Status
	sb.WriteString("\n")
	if m.status != "" {
		if m.statusOK {
			sb.WriteString(successStyle.Render(m.status))
		} else {
			sb.WriteString(errorStyle.Render(m.status))
		}
	}
	sb.WriteString("\n\n" + labelStyle.Render(
		"Tab:Wechseln  r:Refresh  q:Beenden  "+
			"[Backend] c:C  R:Rust  a:Auto"))

	return sb.String()
}

func (m model) bme280View() string {
	d := m.bme280
	content := fmt.Sprintf(
		"%s  🌡 Temperatur:       %s\n"+
			"%s  💧 Luftfeuchtigkeit: %s\n"+
			"%s  🔵 Luftdruck:        %s\n"+
			"%s  ⛰  Höhe:             %s\n"+
			"%s  🔧 Backend:          %s\n\n%s",
		labelStyle.Render("→"), successStyle.Render(fmt.Sprintf("%.2f °C", d.Temperature)),
		labelStyle.Render("→"), successStyle.Render(fmt.Sprintf("%.2f %%", d.Humidity)),
		labelStyle.Render("→"), successStyle.Render(fmt.Sprintf("%.2f hPa", d.Pressure)),
		labelStyle.Render("→"), successStyle.Render(fmt.Sprintf("%.1f m", d.Altitude)),
		labelStyle.Render("→"), successStyle.Render(d.Backend),
		labelStyle.Render("r = Aktualisieren"),
	)
	return cardStyle.Render("🌡 BME280 Sensor\n\n" + content)
}

func (m model) gpioView() string {
	content := labelStyle.Render(
		"GPIO Steuerung\n\n" +
			"Pin eingeben und HIGH/LOW setzen\n\n" +
			"Aktiver Pin: " + m.gpioPin + "\n\n" +
			"h:HIGH  l:LOW  i:Pin eingeben")
	return cardStyle.Render("⚡ GPIO\n\n" + content)
}

func (m model) backendView() string {
	backends := []struct{ key, icon, name string }{
		{"c", "⚙️ ", "C Library"},
		{"R", "🦀", "Rust Library"},
		{"a", "🔄", "Auto (C→Rust Fallback)"},
	}
	var rows string
	for _, b := range backends {
		style := labelStyle
		if b.name == m.backend || (b.key == "a" && m.backend == "auto") ||
			(b.key == "c" && m.backend == "c") ||
			(b.key == "R" && m.backend == "rust") {
			style = successStyle
		}
		rows += style.Render(fmt.Sprintf("[%s] %s %s\n", b.key, b.icon, b.name))
	}
	content := rows + "\n" + labelStyle.Render("Taste drücken zum Wechseln")
	return cardStyle.Render("🔧 HAL Backend\n\n" + content)
}

func main() {
	if len(os.Args) > 1 {
		apiBase = "http://" + os.Args[1] + ":5000"
	}
	p := tea.NewProgram(
		initialModel(),
		tea.WithAltScreen(),
		tea.WithMouseCellMotion(),
	)
	if _, err := p.Run(); err != nil {
		fmt.Printf("Fehler: %v\n", err)
		os.Exit(1)
	}
}
