// Provider-basierte Allure-Tests für die C-Library.
// CGO-Deklarationen sind in cgo.go; diese Datei ruft nur Go-Wrapper auf.
//
// Run:
//
//	cd tools/c_cgo_test && go mod tidy && go test -v ./... -count=1
package c_cgo_test

import (
	"testing"

	"github.com/ozontech/allure-go/pkg/allure"
	"github.com/ozontech/allure-go/pkg/framework/provider"
	"github.com/ozontech/allure-go/pkg/framework/suite"
)

// ── GPIO ──────────────────────────────────────────────────────────────────────

type GPIOSuite struct{ suite.Suite }

func (s *GPIOSuite) TestExportFailsNoSysfs(t provider.T) {
	t.Epic("C Hardware Drivers")
	t.Feature("GPIO")
	t.Title("gpio_export schlägt fehl ohne sysfs")
	t.Severity(allure.NORMAL)
	t.WithNewStep("gpio_export(999) — kein /sys/class/gpio/export", func(sCtx provider.StepCtx) {
		sCtx.Assert().Equal(-1, GPIOExport(999))
	})
}

func (s *GPIOSuite) TestUnexportFailsNoSysfs(t provider.T) {
	t.Epic("C Hardware Drivers")
	t.Feature("GPIO")
	t.Title("gpio_unexport schlägt fehl ohne sysfs")
	t.Severity(allure.NORMAL)
	t.WithNewStep("gpio_unexport(999) — kein /sys/class/gpio/unexport", func(sCtx provider.StepCtx) {
		sCtx.Assert().Equal(-1, GPIOUnexport(999))
	})
}

func (s *GPIOSuite) TestSetDirectionFailsNoSysfs(t provider.T) {
	t.Epic("C Hardware Drivers")
	t.Feature("GPIO")
	t.Title("gpio_set_direction schlägt fehl ohne sysfs")
	t.Severity(allure.NORMAL)
	t.WithNewStep("gpio_set_direction(999, OUTPUT)", func(sCtx provider.StepCtx) {
		sCtx.Assert().Equal(-1, GPIOSetDirection(999, true))
	})
}

func (s *GPIOSuite) TestWriteFailsNoSysfs(t provider.T) {
	t.Epic("C Hardware Drivers")
	t.Feature("GPIO")
	t.Title("gpio_write schlägt fehl ohne sysfs")
	t.Severity(allure.NORMAL)
	t.WithNewStep("gpio_write(999, 1)", func(sCtx provider.StepCtx) {
		sCtx.Assert().Equal(-1, GPIOWrite(999, 1))
	})
}

func (s *GPIOSuite) TestReadFailsNoSysfs(t provider.T) {
	t.Epic("C Hardware Drivers")
	t.Feature("GPIO")
	t.Title("gpio_read schlägt fehl ohne sysfs")
	t.Severity(allure.NORMAL)
	t.WithNewStep("gpio_read(999, &val)", func(sCtx provider.StepCtx) {
		sCtx.Assert().Equal(-1, GPIORead(999))
	})
}

func TestGPIO(t *testing.T) { suite.RunSuite(t, new(GPIOSuite)) }

// ── UART ──────────────────────────────────────────────────────────────────────

type UARTSuite struct{ suite.Suite }

func (s *UARTSuite) TestOpenFailsNoDevice(t provider.T) {
	t.Epic("C Hardware Drivers")
	t.Feature("UART")
	t.Title("uart_open schlägt fehl ohne Device")
	t.Severity(allure.NORMAL)
	t.WithNewStep("uart_open(\"/dev/ttyS99\", 9600)", func(sCtx provider.StepCtx) {
		sCtx.Assert().Equal(-1, UARTOpen("/dev/ttyS99", 9600))
	})
}

func (s *UARTSuite) TestCloseInvalidFdSafe(t provider.T) {
	t.Epic("C Hardware Drivers")
	t.Feature("UART")
	t.Title("uart_close mit fd=-1 ist sicher")
	t.Severity(allure.MINOR)
	t.WithNewStep("uart_close mit fd=-1 — darf nicht abstürzen", func(sCtx provider.StepCtx) {
		UARTCloseSafe()
	})
}

func TestUART(t *testing.T) { suite.RunSuite(t, new(UARTSuite)) }

// ── SPI ───────────────────────────────────────────────────────────────────────

type SPISuite struct{ suite.Suite }

func (s *SPISuite) TestOpenFailsNoDevice(t provider.T) {
	t.Epic("C Hardware Drivers")
	t.Feature("SPI")
	t.Title("spi_open schlägt fehl ohne Device")
	t.Severity(allure.NORMAL)
	t.WithNewStep("spi_open(\"/dev/spidev99.0\")", func(sCtx provider.StepCtx) {
		sCtx.Assert().Equal(-1, SPIOpen("/dev/spidev99.0", 1000000, 0))
	})
}

func TestSPI(t *testing.T) { suite.RunSuite(t, new(SPISuite)) }

// ── BME280 ────────────────────────────────────────────────────────────────────

type BME280Suite struct{ suite.Suite }

func (s *BME280Suite) TestInitNullPtr(t provider.T) {
	t.Epic("C Hardware Drivers")
	t.Feature("BME280 Sensor")
	t.Title("bme280_init(NULL) → Fehlercode")
	t.Severity(allure.NORMAL)
	t.WithNewStep("bme280_init(NULL) aufrufen", func(sCtx provider.StepCtx) {
		sCtx.Assert().NotEqual(0, BME280InitNull())
	})
}

func (s *BME280Suite) TestGetSensorDataNullDev(t provider.T) {
	t.Epic("C Hardware Drivers")
	t.Feature("BME280 Sensor")
	t.Title("bme280_get_sensor_data mit NULL dev → Fehlercode")
	t.Severity(allure.NORMAL)
	t.WithNewStep("bme280_get_sensor_data(BME280_ALL, &data, NULL)", func(sCtx provider.StepCtx) {
		sCtx.Assert().NotEqual(0, BME280GetSensorDataNullDev())
	})
}

func (s *BME280Suite) TestCompensateNullCalib(t provider.T) {
	t.Epic("C Hardware Drivers")
	t.Feature("BME280 Sensor")
	t.Title("bme280_compensate_data mit NULL calib → Fehlercode")
	t.Severity(allure.MINOR)
	t.WithNewStep("bme280_compensate_data(BME280_ALL, &uncomp, &comp, NULL)", func(sCtx provider.StepCtx) {
		sCtx.Assert().NotEqual(0, BME280CompensateNullCalib())
	})
}

func TestBME280(t *testing.T) { suite.RunSuite(t, new(BME280Suite)) }
