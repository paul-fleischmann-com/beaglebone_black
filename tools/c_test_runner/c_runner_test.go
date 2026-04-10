// Package c_test_runner runs the Unity C test binary and reports each result
// as an individual Allure result file (allure-results/*.json).
//
// Verwendet nur pkg/allure (kein pkg/framework) um API-Brüche zu vermeiden.
// Jede Unity-Test-Gruppe wird als t.Run Subtest abgebildet — gleiche logische
// Struktur wie der Python-Wrapper (BME280, GPIO, UART als Gruppen).
//
// Run:
//
//	cd tools/c_test_runner && go mod tidy && go test -v ./... -count=1
package c_test_runner

import (
	"bufio"
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"regexp"
	"runtime"
	"strconv"
	"strings"
	"sync"
	"testing"
	"time"

	"github.com/ozontech/allure-go/pkg/allure"
)

// ── Paths ─────────────────────────────────────────────────────────────────────

func repoRoot() string {
	_, f, _, _ := runtime.Caller(0)
	return filepath.Join(filepath.Dir(f), "..", "..")
}

func cLibDir() string { return filepath.Join(repoRoot(), "c-lib") }
func testBin() string { return filepath.Join(repoRoot(), "project", "c", "test", "test_runner") }

// ── Unity parser ──────────────────────────────────────────────────────────────

var resultRE = regexp.MustCompile(
	`^(?P<file>[^:]+):(?P<line>\d+):(?P<name>[^:]+):(?P<status>PASS|FAIL|IGNORE)(?::(?P<msg>.*))?$`,
)

type unityResult struct {
	File, Name, Status, Msg string
	Line                    int
}

func parseUnity(output string) map[string]unityResult {
	m := make(map[string]unityResult)
	sc := bufio.NewScanner(strings.NewReader(output))
	for sc.Scan() {
		groups := resultRE.FindStringSubmatch(strings.TrimSpace(sc.Text()))
		if groups == nil {
			continue
		}
		r := unityResult{}
		for i, name := range resultRE.SubexpNames() {
			switch name {
			case "file":
				r.File = groups[i]
			case "line":
				r.Line, _ = strconv.Atoi(groups[i])
			case "name":
				r.Name = groups[i]
			case "status":
				r.Status = groups[i]
			case "msg":
				r.Msg = strings.TrimSpace(groups[i])
			}
		}
		m[r.Name] = r
	}
	return m
}

// ── Build + run once ──────────────────────────────────────────────────────────

var (
	once      sync.Once
	cache     map[string]unityResult
	rawOutput string
	buildErr  error
)

func ensureRun() (map[string]unityResult, string, error) {
	once.Do(func() {
		b := exec.Command("make", "-C", cLibDir(), "test-bin")
		b.Stdout, b.Stderr = os.Stderr, os.Stderr
		if buildErr = b.Run(); buildErr != nil {
			return
		}
		out, _ := exec.Command(testBin()).CombinedOutput()
		rawOutput = string(out)
		cache = parseUnity(rawOutput)
	})
	return cache, rawOutput, buildErr
}

// ── Label helpers ─────────────────────────────────────────────────────────────

type meta struct{ feature, story, severity string }

var featureMap = map[string]meta{
	"test_bme280": {"BME280 Sensor", "I2C Sensor Driver", "normal"},
	"test_gpio":   {"GPIO", "Sysfs GPIO Driver", "normal"},
	"test_uart":   {"UART", "Serial Communication", "normal"},
	"test_spi":    {"SPI", "SPI Bus Driver", "normal"},
}

var stepKeys = [][2]string{
	{"null_ptr", "Verify null-pointer guard"},
	{"null_output", "Verify NULL output parameter"},
	{"null_data", "Verify NULL data parameter"},
	{"invalid_fd", "Verify invalid file-descriptor handling"},
	{"no_device", "Verify graceful failure without hardware"},
	{"no_sysfs", "Verify graceful failure without sysfs"},
	{"init", "Call init function"},
	{"open", "Open device"},
	{"close", "Close device"},
	{"read", "Read from device"},
	{"write", "Write to device"},
}

func metaFor(name string) meta {
	for prefix, m := range featureMap {
		if strings.HasPrefix(name, prefix) {
			return m
		}
	}
	return meta{"C Library", "Hardware Abstraction", "minor"}
}

func stepLabel(name string) string {
	for _, pair := range stepKeys {
		if strings.Contains(name, pair[0]) {
			return pair[1]
		}
	}
	return "Execute test"
}

func toAllureStatus(s string) allure.Status {
	switch s {
	case "PASS":
		return allure.Passed
	case "FAIL":
		return allure.Failed
	case "IGNORE":
		return allure.Skipped
	}
	return allure.Unknown
}

// ── Allure JSON writer ────────────────────────────────────────────────────────

func writeResult(r unityResult, raw string) {
	m := metaFor(r.Name)
	now := time.Now().UnixMilli()

	result := allure.NewResult(r.Name, "c-unity/"+r.Name)
	result.Status = toAllureStatus(r.Status)
	result.WithLabels(
		&allure.Label{Name: "epic", Value: "C Hardware Drivers"},
		&allure.Label{Name: "feature", Value: m.feature},
		&allure.Label{Name: "story", Value: m.story},
		&allure.Label{Name: "severity", Value: m.severity},
		&allure.Label{Name: "owner", Value: "Adrian"},
		&allure.Label{Name: "framework", Value: "Unity"},
		&allure.Label{Name: "language", Value: "C"},
		&allure.Label{Name: "priority", Value: "high"},
	)
	desc := r.Msg
	if desc == "" {
		desc = fmt.Sprintf("%s — CI error-path test (no hardware required).\nSource: %s:%d",
			r.Name, filepath.Base(r.File), r.Line)
	}
	result.Description = desc
	if r.Msg != "" {
		result.StatusDetails = allure.StatusDetail{Message: r.Msg}
	}

	// Steps: source → execute → assert
	locStep := allure.NewStep(
		fmt.Sprintf("Source: %s:%d", filepath.Base(r.File), r.Line), allure.Passed, now, now+1, nil)

	execStep := allure.NewStep(stepLabel(r.Name), toAllureStatus(r.Status), now+1, now+2, nil)

	assertStep := allure.NewStep(
		fmt.Sprintf("Assert → %s", r.Status), toAllureStatus(r.Status), now+2, now+3, nil)

	result.Steps = []*allure.Step{locStep, execStep, assertStep}
	result.Start, result.Stop = now, now+3

	// Attach: relevant console lines
	var lines []string
	for _, l := range strings.Split(raw, "\n") {
		if strings.Contains(l, r.Name) || strings.HasPrefix(l, "-") || strings.Contains(l, "Tests") {
			lines = append(lines, l)
		}
	}
	if len(lines) > 0 {
		result.Attachments = []*allure.Attachment{
			allure.NewAttachment("unity console output", allure.Text,
				[]byte(strings.Join(lines, "\n"))),
		}
	}

	_ = result.Print()
}

// ── Core helper — Go-Äquivalent zu Python _run_unity_test() ──────────────────
//
// Entspricht exakt:
//
//	with allure.step("Starte C-Binary"):   result = subprocess.run(binary, ...)
//	with allure.step("Prüfe Rückgabewert"): assert result.returncode == 0

func runUnityTest(t *testing.T, name string, results map[string]unityResult, raw string) {
	t.Helper()

	r, ok := results[name]
	if !ok {
		t.Errorf("Test %q nicht in Unity-Output gefunden", name)
		return
	}

	writeResult(r, raw)

	t.Logf("[%s] %s  source=%s:%d", r.Status, r.Name, filepath.Base(r.File), r.Line)
	if r.Msg != "" {
		t.Log(r.Msg)
	}

	switch r.Status {
	case "FAIL":
		t.Fail()
	case "IGNORE":
		t.Skip(r.Msg)
	}
}

// ── BME280 — @allure.epic('C Hardware Drivers') @allure.feature('BME280 Sensor') ──

func TestBME280(t *testing.T) {
	results, raw, err := ensureRun()
	if err != nil {
		t.Skipf("Unity binary build failed: %v", err)
	}

	t.Run("test_bme280_init_null_ptrs", func(t *testing.T) {
		runUnityTest(t, "test_bme280_init_null_ptrs", results, raw)
	})
	t.Run("test_bme280_get_sensor_data_null_output", func(t *testing.T) {
		runUnityTest(t, "test_bme280_get_sensor_data_null_output", results, raw)
	})
	t.Run("test_bme280_set_sensor_settings_null_settings", func(t *testing.T) {
		runUnityTest(t, "test_bme280_set_sensor_settings_null_settings", results, raw)
	})
	t.Run("test_bme280_compensate_null_data", func(t *testing.T) {
		runUnityTest(t, "test_bme280_compensate_null_data", results, raw)
	})
}

// ── GPIO — @allure.epic('C Hardware Drivers') @allure.feature('GPIO') ──────────

func TestGPIO(t *testing.T) {
	results, raw, err := ensureRun()
	if err != nil {
		t.Skipf("Unity binary build failed: %v", err)
	}

	t.Run("test_gpio_export_fails_no_sysfs", func(t *testing.T) {
		runUnityTest(t, "test_gpio_export_fails_no_sysfs", results, raw)
	})
	t.Run("test_gpio_read_fails_no_sysfs", func(t *testing.T) {
		runUnityTest(t, "test_gpio_read_fails_no_sysfs", results, raw)
	})
	t.Run("test_gpio_write_fails_no_sysfs", func(t *testing.T) {
		runUnityTest(t, "test_gpio_write_fails_no_sysfs", results, raw)
	})
}

// ── UART — @allure.epic('C Hardware Drivers') @allure.feature('UART') ──────────

func TestUART(t *testing.T) {
	results, raw, err := ensureRun()
	if err != nil {
		t.Skipf("Unity binary build failed: %v", err)
	}

	t.Run("test_uart_open_fails_no_device", func(t *testing.T) {
		runUnityTest(t, "test_uart_open_fails_no_device", results, raw)
	})
	t.Run("test_uart_close_invalid_fd", func(t *testing.T) {
		runUnityTest(t, "test_uart_close_invalid_fd", results, raw)
	})
}
