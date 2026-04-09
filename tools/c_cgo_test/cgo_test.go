// Package c_cgo_test ruft die C-Library-Funktionen direkt per CGO auf und
// berichtet jeden Testfall als Allure-Ergebnis über das allure-go Framework.
//
// Im Gegensatz zum Unity-basierten c_test_runner (der ein externes Binary
// ausführt und dessen Output parst) nutzt dieses Paket den Provider-Ansatz:
// Go → CGO → C-Funktion → Rückgabewert prüfen.
//
// Getestet werden ausschließlich Fehler-Pfade, die ohne Hardware auslösbar
// sind (kein sysfs, kein /dev/ttyS*, NULL-Pointer).
//
// Run:
//
//	cd tools/c_cgo_test && go mod tidy && go test -v ./... -count=1
package c_cgo_test

/*
#cgo CFLAGS: -I../../project/c/include
#include "gpio.h"
#include "uart.h"
#include "spi.h"
#include "bme280.h"
#include <stdlib.h>
*/
import "C"
import (
	"testing"
	"unsafe"

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
	t.WithNewStep("gpio_export(999) aufrufen — kein /sys/class/gpio/export", func(sCtx provider.StepCtx) {
		ret := int(C.gpio_export(C.uint32_t(999)))
		sCtx.Assert().Equal(-1, ret, "gpio_export muss -1 zurückgeben wenn sysfs fehlt")
	})
}

func (s *GPIOSuite) TestUnexportFailsNoSysfs(t provider.T) {
	t.Epic("C Hardware Drivers")
	t.Feature("GPIO")
	t.Title("gpio_unexport schlägt fehl ohne sysfs")
	t.Severity(allure.NORMAL)
	t.WithNewStep("gpio_unexport(999) aufrufen — kein /sys/class/gpio/unexport", func(sCtx provider.StepCtx) {
		ret := int(C.gpio_unexport(C.uint32_t(999)))
		sCtx.Assert().Equal(-1, ret)
	})
}

func (s *GPIOSuite) TestSetDirectionFailsNoSysfs(t provider.T) {
	t.Epic("C Hardware Drivers")
	t.Feature("GPIO")
	t.Title("gpio_set_direction schlägt fehl ohne sysfs")
	t.Severity(allure.NORMAL)
	t.WithNewStep("gpio_set_direction(999, OUTPUT) aufrufen", func(sCtx provider.StepCtx) {
		ret := int(C.gpio_set_direction(C.uint32_t(999), C.GPIO_OUTPUT))
		sCtx.Assert().Equal(-1, ret)
	})
}

func (s *GPIOSuite) TestWriteFailsNoSysfs(t provider.T) {
	t.Epic("C Hardware Drivers")
	t.Feature("GPIO")
	t.Title("gpio_write schlägt fehl ohne sysfs")
	t.Severity(allure.NORMAL)
	t.WithNewStep("gpio_write(999, 1) aufrufen", func(sCtx provider.StepCtx) {
		ret := int(C.gpio_write(C.uint32_t(999), C.int(1)))
		sCtx.Assert().Equal(-1, ret)
	})
}

func (s *GPIOSuite) TestReadFailsNoSysfs(t provider.T) {
	t.Epic("C Hardware Drivers")
	t.Feature("GPIO")
	t.Title("gpio_read schlägt fehl ohne sysfs")
	t.Severity(allure.NORMAL)
	t.WithNewStep("gpio_read(999, &val) aufrufen", func(sCtx provider.StepCtx) {
		var val C.int
		ret := int(C.gpio_read(C.uint32_t(999), &val))
		sCtx.Assert().Equal(-1, ret)
	})
}

func TestGPIO(t *testing.T) {
	suite.RunSuite(t, new(GPIOSuite))
}

// ── UART ──────────────────────────────────────────────────────────────────────

type UARTSuite struct{ suite.Suite }

func (s *UARTSuite) TestOpenFailsNoDevice(t provider.T) {
	t.Epic("C Hardware Drivers")
	t.Feature("UART")
	t.Title("uart_open schlägt fehl ohne Device")
	t.Severity(allure.NORMAL)
	t.WithNewStep("uart_open auf nicht-existentes /dev/ttyS99", func(sCtx provider.StepCtx) {
		var dev C.uart_dev_t
		port := C.CString("/dev/ttyS99")
		defer C.free(unsafe.Pointer(port))
		ret := int(C.uart_open(&dev, port, C.uint32_t(9600)))
		sCtx.Assert().Equal(-1, ret, "uart_open muss -1 zurückgeben wenn Device fehlt")
	})
}

func (s *UARTSuite) TestCloseInvalidFd(t provider.T) {
	t.Epic("C Hardware Drivers")
	t.Feature("UART")
	t.Title("uart_close mit ungültigem fd ist sicher")
	t.Severity(allure.MINOR)
	t.WithNewStep("uart_close auf Device mit fd=-1 aufrufen", func(sCtx provider.StepCtx) {
		var dev C.uart_dev_t
		dev.fd = C.int(-1)
		C.uart_close(&dev)
		sCtx.Assert().Equal(C.int(-1), dev.fd, "uart_close darf fd=-1 nicht verändern")
	})
}

func TestUART(t *testing.T) {
	suite.RunSuite(t, new(UARTSuite))
}

// ── SPI ───────────────────────────────────────────────────────────────────────

type SPISuite struct{ suite.Suite }

func (s *SPISuite) TestOpenFailsNoDevice(t provider.T) {
	t.Epic("C Hardware Drivers")
	t.Feature("SPI")
	t.Title("spi_open schlägt fehl ohne Device")
	t.Severity(allure.NORMAL)
	t.WithNewStep("spi_open auf nicht-existentes /dev/spidev99.0", func(sCtx provider.StepCtx) {
		var dev C.spi_dev_t
		device := C.CString("/dev/spidev99.0")
		defer C.free(unsafe.Pointer(device))
		ret := int(C.spi_open(&dev, device, C.uint32_t(1000000), C.uint8_t(0)))
		sCtx.Assert().Equal(-1, ret, "spi_open muss -1 zurückgeben wenn Device fehlt")
	})
}

func TestSPI(t *testing.T) {
	suite.RunSuite(t, new(SPISuite))
}

// ── BME280 ────────────────────────────────────────────────────────────────────

type BME280Suite struct{ suite.Suite }

func (s *BME280Suite) TestInitNullPtr(t provider.T) {
	t.Epic("C Hardware Drivers")
	t.Feature("BME280 Sensor")
	t.Title("bme280_init mit NULL-Pointer → Fehler")
	t.Severity(allure.NORMAL)
	t.WithNewStep("bme280_init(NULL) aufrufen", func(sCtx provider.StepCtx) {
		ret := int(C.bme280_init(nil))
		sCtx.Assert().NotEqual(0, ret, "bme280_init(NULL) muss Fehlercode zurückgeben")
	})
}

func (s *BME280Suite) TestGetSensorDataNullDev(t provider.T) {
	t.Epic("C Hardware Drivers")
	t.Feature("BME280 Sensor")
	t.Title("bme280_get_sensor_data mit NULL dev → Fehler")
	t.Severity(allure.NORMAL)
	t.WithNewStep("bme280_get_sensor_data(BME280_ALL, &data, NULL) aufrufen", func(sCtx provider.StepCtx) {
		var data C.struct_bme280_data
		ret := int(C.bme280_get_sensor_data(C.BME280_ALL, &data, nil))
		sCtx.Assert().NotEqual(0, ret)
	})
}

func (s *BME280Suite) TestCompensateNullCalib(t provider.T) {
	t.Epic("C Hardware Drivers")
	t.Feature("BME280 Sensor")
	t.Title("bme280_compensate_data mit NULL calib_data → Fehler")
	t.Severity(allure.MINOR)
	t.WithNewStep("bme280_compensate_data mit NULL calib_data aufrufen", func(sCtx provider.StepCtx) {
		var uncomp C.struct_bme280_uncomp_data
		var comp C.struct_bme280_data
		ret := int(C.bme280_compensate_data(C.BME280_ALL, &uncomp, &comp, nil))
		sCtx.Assert().NotEqual(0, ret)
	})
}

func TestBME280(t *testing.T) {
	suite.RunSuite(t, new(BME280Suite))
}
