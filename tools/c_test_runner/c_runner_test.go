// Package c_test_runner ist der Go-Äquivalent zum Python allure-pytest Wrapper.
//
// Struktur:
//   - Eine Suite-Struct pro Hardware-Komponente (BME280Suite, GPIOSuite, UARTSuite)
//   - Jede Struct embeddet suite.Suite → entspricht einer Python-Klasse mit @allure.epic/@allure.feature
//   - Jede Methode = ein Test mit t.Epic/t.Feature/t.Story/t.Severity + Steps + Links
//   - runUnityTest() = Go-Äquivalent zu _run_unity_test() aus dem Python-Wrapper
//
// Run:
//
//	cd tools/c_test_runner && go mod tidy && go test -v ./... -count=1
//	allure generate ../../allure-results -o ../../allure-report --clean
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

	"github.com/ozontech/allure-go/pkg/allure"
	"github.com/ozontech/allure-go/pkg/framework/provider"
	"github.com/ozontech/allure-go/pkg/framework/suite"
)

// ── Paths ─────────────────────────────────────────────────────────────────────

func repoRoot() string {
	_, thisFile, _, _ := runtime.Caller(0)
	return filepath.Join(filepath.Dir(thisFile), "..", "..")
}

func cLibDir() string { return filepath.Join(repoRoot(), "c-lib") }
func testBin() string { return filepath.Join(repoRoot(), "project", "c", "test", "test_runner") }

// ── Unity output parser ───────────────────────────────────────────────────────

var resultRE = regexp.MustCompile(
	`^(?P<file>[^:]+):(?P<line>\d+):(?P<name>[^:]+):(?P<status>PASS|FAIL|IGNORE)(?::(?P<msg>.*))?$`,
)

type unityResult struct {
	File   string
	Line   int
	Name   string
	Status string
	Msg    string
}

func parseUnityOutput(output string) map[string]unityResult {
	results := make(map[string]unityResult)
	scanner := bufio.NewScanner(strings.NewReader(output))
	for scanner.Scan() {
		line := strings.TrimSpace(scanner.Text())
		m := resultRE.FindStringSubmatch(line)
		if m == nil {
			continue
		}
		names := resultRE.SubexpNames()
		r := unityResult{}
		for i, v := range m {
			switch names[i] {
			case "file":
				r.File = v
			case "line":
				r.Line, _ = strconv.Atoi(v)
			case "name":
				r.Name = v
			case "status":
				r.Status = v
			case "msg":
				r.Msg = strings.TrimSpace(v)
			}
		}
		results[r.Name] = r
	}
	return results
}

// ── Shared binary run (once per test binary execution) ────────────────────────

var (
	buildOnce   sync.Once
	unityResult_ map[string]unityResult
	rawStdout   string
	buildErr    error
)

func ensureBuilt() (map[string]unityResult, string, error) {
	buildOnce.Do(func() {
		build := exec.Command("make", "-C", cLibDir(), "test-bin")
		build.Stdout = os.Stderr
		build.Stderr = os.Stderr
		if err := build.Run(); err != nil {
			buildErr = fmt.Errorf("make test-bin: %w", err)
			return
		}
		out, _ := exec.Command(testBin()).CombinedOutput()
		rawStdout = string(out)
		unityResult_ = parseUnityOutput(rawStdout)
	})
	return unityResult_, rawStdout, buildErr
}

// ── Core helper — Go-Äquivalent zu Python _run_unity_test() ──────────────────
//
// Entspricht exakt diesem Python-Muster:
//
//	with allure.step("Starte C-Binary"):
//	    result = subprocess.run([binary_path, ...], capture_output=True, text=True)
//	    allure.attach(result.stdout, ...)
//	with allure.step("Prüfe Rückgabewert"):
//	    assert result.returncode == 0

func runUnityTest(t provider.T, testName string) {
	results, raw, err := ensureBuilt()

	// Step 1: Starte Unity C-Binary
	t.WithNewStep(fmt.Sprintf("Starte Unity C-Binary: %s", testBin()),
		func(sCtx provider.StepCtx) {
			sCtx.WithAttachments(allure.NewAttachment(
				"C-Standard-Output", allure.Text, []byte(raw),
			))
			if err != nil {
				sCtx.WithAttachments(allure.NewAttachment(
					"C-Fehlermeldung", allure.Text, []byte(err.Error()),
				))
				t.Errorf("Build fehlgeschlagen: %v", err)
			}
		},
	)

	if err != nil {
		return
	}

	// Step 2: Suche Ergebnis
	r, ok := results[testName]
	t.WithNewStep(fmt.Sprintf("Suche Ergebnis für: %s", testName),
		func(sCtx provider.StepCtx) {
			if !ok {
				t.Errorf("Test %q nicht in Unity-Output gefunden", testName)
				return
			}
			detail := fmt.Sprintf("%s:%d  →  %s", filepath.Base(r.File), r.Line, r.Status)
			if r.Msg != "" {
				detail += "\n" + r.Msg
			}
			sCtx.WithAttachments(allure.NewAttachment(
				"Unity Testergebnis", allure.Text, []byte(detail),
			))
		},
	)

	if !ok {
		return
	}

	// Step 3: Prüfe Rückgabewert
	t.WithNewStep(fmt.Sprintf("Prüfe Rückgabewert → %s", r.Status),
		func(sCtx provider.StepCtx) {
			// Relevante Zeilen aus raw output anhängen
			var lines []string
			for _, l := range strings.Split(raw, "\n") {
				if strings.Contains(l, r.Name) ||
					strings.HasPrefix(l, "-") ||
					strings.Contains(l, "Tests") {
					lines = append(lines, l)
				}
			}
			if len(lines) > 0 {
				sCtx.WithAttachments(allure.NewAttachment(
					"Unity Console (gefiltert)", allure.Text,
					[]byte(strings.Join(lines, "\n")),
				))
			}

			switch r.Status {
			case "FAIL":
				t.Errorf("Unity meldet FAIL für %s: %s", r.Name, r.Msg)
			case "IGNORE":
				t.Skip(r.Msg)
			}
		},
	)
}

// ── BME280Suite ───────────────────────────────────────────────────────────────
// Entspricht:  @allure.epic('C Hardware Drivers') + @allure.feature('BME280 Sensor') class TestBME280

type BME280Suite struct{ suite.Suite }

func (s *BME280Suite) TestBME280InitNullPtrs(t provider.T) {
	t.Epic("C Hardware Drivers")
	t.Feature("BME280 Sensor")
	t.Story("Null-Pointer Validierung")
	t.Severity(allure.CRITICAL)
	t.Title("BME280 init — null function pointers")
	t.Description("Erwartet BME280_E_NULL_PTR wenn read/write/delay_us NULL sind.")
	t.AddLabel("owner", "Adrian")
	t.AddLabel("framework", "Unity")
	t.AddLabel("language", "C")
	t.Link("https://github.com/BoschSensortec/BME280_driver",
		"BME280 Treiber Dokumentation", allure.LinkType("link"))

	runUnityTest(t, "test_bme280_init_null_ptrs")
}

func (s *BME280Suite) TestBME280GetSensorDataNullOutput(t provider.T) {
	t.Epic("C Hardware Drivers")
	t.Feature("BME280 Sensor")
	t.Story("Null-Pointer Validierung")
	t.Severity(allure.NORMAL)
	t.Title("BME280 get_sensor_data — NULL comp_data")
	t.AddLabel("owner", "Adrian")

	runUnityTest(t, "test_bme280_get_sensor_data_null_output")
}

func (s *BME280Suite) TestBME280SetSensorSettingsNullSettings(t provider.T) {
	t.Epic("C Hardware Drivers")
	t.Feature("BME280 Sensor")
	t.Story("Null-Pointer Validierung")
	t.Severity(allure.NORMAL)
	t.Title("BME280 set_sensor_settings — NULL settings")
	t.AddLabel("owner", "Adrian")

	runUnityTest(t, "test_bme280_set_sensor_settings_null_settings")
}

func (s *BME280Suite) TestBME280CompensateNullData(t provider.T) {
	t.Epic("C Hardware Drivers")
	t.Feature("BME280 Sensor")
	t.Story("Kompensationsberechnung")
	t.Severity(allure.NORMAL)
	t.Title("BME280 compensate_data — NULL comp und calib")
	t.AddLabel("owner", "Adrian")

	runUnityTest(t, "test_bme280_compensate_null_data")
}

func TestBME280(t *testing.T) { suite.RunSuite(t, new(BME280Suite)) }

// ── GPIOSuite ─────────────────────────────────────────────────────────────────
// Entspricht:  @allure.epic('C Hardware Drivers') + @allure.feature('GPIO') class TestGPIO

type GPIOSuite struct{ suite.Suite }

func (s *GPIOSuite) TestGPIOExportFailsNoSysfs(t provider.T) {
	t.Epic("C Hardware Drivers")
	t.Feature("GPIO")
	t.Story("Sysfs Fehlerbehandlung")
	t.Severity(allure.NORMAL)
	t.Title("GPIO export — schlägt fehl ohne /sys/class/gpio")
	t.Description("Prüft ob gpio_export() einen Fehlercode zurückgibt wenn kein sysfs vorhanden ist.")
	t.AddLabel("owner", "Adrian")
	t.AddLabel("tag", "ci-compatible")

	runUnityTest(t, "test_gpio_export_fails_no_sysfs")
}

func (s *GPIOSuite) TestGPIOReadFailsNoSysfs(t provider.T) {
	t.Epic("C Hardware Drivers")
	t.Feature("GPIO")
	t.Story("Sysfs Fehlerbehandlung")
	t.Severity(allure.NORMAL)
	t.Title("GPIO read — schlägt fehl ohne /sys/class/gpio")
	t.AddLabel("owner", "Adrian")
	t.AddLabel("tag", "ci-compatible")

	runUnityTest(t, "test_gpio_read_fails_no_sysfs")
}

func (s *GPIOSuite) TestGPIOWriteFailsNoSysfs(t provider.T) {
	t.Epic("C Hardware Drivers")
	t.Feature("GPIO")
	t.Story("Sysfs Fehlerbehandlung")
	t.Severity(allure.NORMAL)
	t.Title("GPIO write — schlägt fehl ohne /sys/class/gpio")
	t.AddLabel("owner", "Adrian")
	t.AddLabel("tag", "ci-compatible")

	runUnityTest(t, "test_gpio_write_fails_no_sysfs")
}

func TestGPIO(t *testing.T) { suite.RunSuite(t, new(GPIOSuite)) }

// ── UARTSuite ─────────────────────────────────────────────────────────────────
// Entspricht:  @allure.epic('C Hardware Drivers') + @allure.feature('UART') class TestUART

type UARTSuite struct{ suite.Suite }

func (s *UARTSuite) TestUARTOpenFailsNoDevice(t provider.T) {
	t.Epic("C Hardware Drivers")
	t.Feature("UART")
	t.Story("Geräteinitialisierung")
	t.Severity(allure.CRITICAL)
	t.Title("UART open — schlägt fehl ohne /dev/ttyS1")
	t.Description("uart_open() muss einen Fehler zurückgeben wenn das Gerät nicht existiert.")
	t.AddLabel("owner", "Adrian")
	t.AddLabel("tag", "ci-compatible")

	runUnityTest(t, "test_uart_open_fails_no_device")
}

func (s *UARTSuite) TestUARTCloseInvalidFd(t provider.T) {
	t.Epic("C Hardware Drivers")
	t.Feature("UART")
	t.Story("Ressourcenfreigabe")
	t.Severity(allure.NORMAL)
	t.Title("UART close — fd=-1 darf nicht abstürzen")
	t.Description("uart_close() mit fd=-1 darf keinen Segfault oder undefined behaviour auslösen.")
	t.AddLabel("owner", "Adrian")

	runUnityTest(t, "test_uart_close_invalid_fd")
}

func TestUART(t *testing.T) { suite.RunSuite(t, new(UARTSuite)) }
