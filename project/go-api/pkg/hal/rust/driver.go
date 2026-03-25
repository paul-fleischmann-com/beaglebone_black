package rustdriver

/*
#cgo CFLAGS:  -I${SRCDIR}/../../../libs/include
#cgo LDFLAGS: -L${SRCDIR}/../../../libs -lhardware_rs -ldl
#include "hardware_rs.h"
#include <stdlib.h>
*/
import "C"
import (
	"fmt"
	"myproject/pkg/hal"
	"myproject/pkg/hal/config"
	"time"
	"unsafe"
)

type RustDriver struct {
	uart C.RsUartHandle
	cfg  *config.Config
}

func New(cfg *config.Config) *RustDriver   { return &RustDriver{cfg: cfg} }
func (d *RustDriver) Name() string         { return "Rust Hardware Driver" }
func (d *RustDriver) Backend() hal.Backend { return hal.BackendRust }
func (d *RustDriver) Init() error          { return nil }
func (d *RustDriver) BME280Read() (*hal.BME280Data, error) {
	cp := C.CString(d.cfg.I2CBus)
	defer C.free(unsafe.Pointer(cp))
	raw := C.rs_bme280_read(cp, C.uint8_t(d.cfg.BME280Addr))
	if raw.error != 0 {
		return nil, fmt.Errorf("Rust BME280: %d", raw.error)
	}
	return &hal.BME280Data{
		Temperature: float64(raw.temperature),
		Humidity:    float64(raw.humidity),
		Pressure:    float64(raw.pressure),
		Altitude:    float64(raw.altitude),
		Timestamp:   time.Now().UTC(),
		Backend:     "rust",
	}, nil
}
func (d *RustDriver) GPIOExport(pin uint32) error {
	if ret := C.rs_gpio_export(C.uint32_t(pin)); ret != 0 {
		return fmt.Errorf("rs_gpio_export: %d", ret)
	}
	return nil
}
func (d *RustDriver) GPIOSetDirection(pin uint32, out bool) error {
	v := C.int(0)
	if out {
		v = 1
	}
	if ret := C.rs_gpio_set_direction(C.uint32_t(pin), v); ret != 0 {
		return fmt.Errorf("rs_gpio_dir: %d", ret)
	}
	return nil
}
func (d *RustDriver) GPIORead(pin uint32) (*hal.GPIOData, error) {
	raw := C.rs_gpio_read(C.uint32_t(pin))
	if raw.error != 0 {
		return nil, fmt.Errorf("rs_gpio_read: %d", raw.error)
	}
	return &hal.GPIOData{Pin: pin, Value: int(raw.value), Backend: "rust"}, nil
}
func (d *RustDriver) GPIOWrite(pin uint32, value int) error {
	if ret := C.rs_gpio_write(C.uint32_t(pin), C.int(value)); ret != 0 {
		return fmt.Errorf("rs_gpio_write: %d", ret)
	}
	return nil
}
func (d *RustDriver) UARTOpen(port string, baud uint32) error {
	cp := C.CString(port)
	defer C.free(unsafe.Pointer(cp))
	d.uart = C.rs_uart_open(cp, C.uint32_t(baud))
	if d.uart.port == nil {
		return fmt.Errorf("rs_uart_open failed")
	}
	return nil
}
func (d *RustDriver) UARTWrite(data []byte) (int, error) {
	ret := C.rs_uart_write(&d.uart, (*C.uint8_t)(unsafe.Pointer(&data[0])), C.uint32_t(len(data)))
	if ret < 0 {
		return 0, fmt.Errorf("rs_uart_write failed")
	}
	return int(ret), nil
}
func (d *RustDriver) UARTRead(ms int) (*hal.UARTData, error) {
	raw := C.rs_uart_read(&d.uart)
	if raw.error != 0 {
		return nil, fmt.Errorf("rs_uart_read failed")
	}
	data := C.GoBytes(unsafe.Pointer(&raw.buf[0]), C.int(raw.len))
	return &hal.UARTData{Data: data, Length: int(raw.len), Backend: "rust"}, nil
}
func (d *RustDriver) UARTClose() { C.rs_uart_close(&d.uart) }
func (d *RustDriver) SPITransfer(device string, speed uint32, tx []byte) (*hal.SPIData, error) {
	cp := C.CString(device)
	defer C.free(unsafe.Pointer(cp))
	raw := C.rs_spi_transfer(cp, C.uint32_t(speed), (*C.uint8_t)(unsafe.Pointer(&tx[0])), C.uint32_t(len(tx)))
	if raw.error != 0 {
		return nil, fmt.Errorf("rs_spi_transfer: %d", raw.error)
	}
	rxBuf := C.GoBytes(unsafe.Pointer(&raw.buf[0]), C.int(raw.len))
	return &hal.SPIData{RxBuf: rxBuf, Length: int(raw.len), Backend: "rust"}, nil
}
func (d *RustDriver) Close() { C.rs_uart_close(&d.uart) }
