package cdriver

/*
#cgo CFLAGS:  -I${SRCDIR}/../../../libs/include
#cgo LDFLAGS: -L${SRCDIR}/../../../libs -lhardware -lm
#include "bme280.h"
#include "gpio.h"
#include "uart.h"
#include "spi.h"
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

type CDriver struct {
	bme280 C.struct_bme280_dev
	// i2cCtx muss in C-Speicher liegen — CGO erlaubt keinen Go-Pointer
	// in bme280_dev.intf_ptr wenn bme280_dev selbst Go-Speicher ist.
	i2cCtx *C.bme280_i2c_ctx_t
	uart   C.uart_dev_t
	cfg    *config.Config
}

func New(cfg *config.Config) *CDriver   { return &CDriver{cfg: cfg} }
func (d *CDriver) Name() string         { return "C Hardware Driver" }
func (d *CDriver) Backend() hal.Backend { return hal.BackendC }

func (d *CDriver) Init() error {
	d.i2cCtx = (*C.bme280_i2c_ctx_t)(C.malloc(C.sizeof_bme280_i2c_ctx_t))
	if d.i2cCtx == nil {
		return fmt.Errorf("C BME280: malloc failed")
	}
	cp := C.CString(d.cfg.I2CBus)
	defer C.free(unsafe.Pointer(cp))
	if ret := C.bme280_open(cp, C.uint8_t(d.cfg.BME280Addr), &d.bme280, d.i2cCtx); ret != 0 {
		C.free(unsafe.Pointer(d.i2cCtx))
		d.i2cCtx = nil
		return fmt.Errorf("C BME280 open on %s@0x%02x: %d", d.cfg.I2CBus, d.cfg.BME280Addr, ret)
	}
	return nil
}
func (d *CDriver) BME280Read() (*hal.BME280Data, error) {
	var raw C.bme280_data_t
	if ret := C.bme280_read(&d.bme280, &raw); ret != 0 {
		return nil, fmt.Errorf("C BME280 read: %d", ret)
	}
	return &hal.BME280Data{
		Temperature: float64(raw.temperature),
		Humidity:    float64(raw.humidity),
		Pressure:    float64(raw.pressure),
		Altitude:    float64(raw.altitude),
		Timestamp:   time.Now().UTC(),
		Backend:     "c",
	}, nil
}
func (d *CDriver) GPIOExport(pin uint32) error {
	if ret := C.gpio_export(C.uint(pin)); ret != 0 {
		return fmt.Errorf("gpio_export: %d", ret)
	}
	return nil
}
func (d *CDriver) GPIOSetDirection(pin uint32, out bool) error {
	dir := C.GPIO_INPUT
	if out {
		dir = C.GPIO_OUTPUT
	}
	if ret := C.gpio_set_direction(C.uint(pin), C.gpio_direction_t(dir)); ret != 0 {
		return fmt.Errorf("gpio_dir: %d", ret)
	}
	return nil
}
func (d *CDriver) GPIORead(pin uint32) (*hal.GPIOData, error) {
	var val C.int
	if ret := C.gpio_read(C.uint(pin), &val); ret != 0 {
		return nil, fmt.Errorf("gpio_read: %d", ret)
	}
	return &hal.GPIOData{Pin: pin, Value: int(val), Backend: "c"}, nil
}
func (d *CDriver) GPIOWrite(pin uint32, value int) error {
	if ret := C.gpio_write(C.uint(pin), C.int(value)); ret != 0 {
		return fmt.Errorf("gpio_write: %d", ret)
	}
	return nil
}
func (d *CDriver) UARTOpen(port string, baud uint32) error {
	cp := C.CString(port)
	defer C.free(unsafe.Pointer(cp))
	if ret := C.uart_open(&d.uart, cp, C.uint(baud)); ret != 0 {
		return fmt.Errorf("uart_open: %d", ret)
	}
	return nil
}
func (d *CDriver) UARTWrite(data []byte) (int, error) {
	ret := C.uart_write(&d.uart, (*C.uint8_t)(unsafe.Pointer(&data[0])), C.size_t(len(data)))
	if ret < 0 {
		return 0, fmt.Errorf("uart_write failed")
	}
	return int(ret), nil
}
func (d *CDriver) UARTRead(ms int) (*hal.UARTData, error) {
	var buf [256]C.uint8_t
	ret := C.uart_read(&d.uart, &buf[0], C.size_t(256), C.int(ms))
	if ret < 0 {
		return nil, fmt.Errorf("uart_read failed")
	}
	return &hal.UARTData{Data: C.GoBytes(unsafe.Pointer(&buf[0]), ret), Length: int(ret), Backend: "c"}, nil
}
func (d *CDriver) UARTClose() { C.uart_close(&d.uart) }
func (d *CDriver) SPITransfer(device string, speed uint32, tx []byte) (*hal.SPIData, error) {
	var dev C.spi_dev_t
	cp := C.CString(device)
	defer C.free(unsafe.Pointer(cp))
	C.spi_open(&dev, cp, C.uint(speed), 0)
	defer C.spi_close(&dev)
	rx := make([]byte, len(tx))
	ret := C.spi_transfer(&dev, (*C.uint8_t)(unsafe.Pointer(&tx[0])), (*C.uint8_t)(unsafe.Pointer(&rx[0])), C.size_t(len(tx)))
	if ret < 0 {
		return nil, fmt.Errorf("spi_transfer failed")
	}
	return &hal.SPIData{RxBuf: rx, Length: len(rx), Backend: "c"}, nil
}
func (d *CDriver) Close() {
	C.bme280_close(&d.bme280)
	if d.i2cCtx != nil {
		C.free(unsafe.Pointer(d.i2cCtx))
		d.i2cCtx = nil
	}
	C.uart_close(&d.uart)
}
