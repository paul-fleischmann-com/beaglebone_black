// Package c_cgo_test exposes thin Go wrappers around the C library functions.
// CGO declarations must live in a non-test file; test files call these wrappers.
package c_cgo_test

/*
#cgo CFLAGS: -I../../project/c/include
#cgo LDFLAGS: -lm
#include "gpio.h"
#include "uart.h"
#include "spi.h"
#include "bme280.h"
#include <stdlib.h>
*/
import "C"
import "unsafe"

// ── GPIO ──────────────────────────────────────────────────────────────────────

func GPIOExport(pin uint32) int {
	return int(C.gpio_export(C.uint32_t(pin)))
}

func GPIOUnexport(pin uint32) int {
	return int(C.gpio_unexport(C.uint32_t(pin)))
}

func GPIOSetDirection(pin uint32, out bool) int {
	var dir C.gpio_direction_t = C.GPIO_INPUT
	if out {
		dir = C.GPIO_OUTPUT
	}
	return int(C.gpio_set_direction(C.uint32_t(pin), dir))
}

func GPIOWrite(pin uint32, val int) int {
	return int(C.gpio_write(C.uint32_t(pin), C.int(val)))
}

func GPIORead(pin uint32) int {
	var val C.int
	return int(C.gpio_read(C.uint32_t(pin), &val))
}

// ── UART ──────────────────────────────────────────────────────────────────────

func UARTOpen(port string, baud uint32) int {
	var dev C.uart_dev_t
	p := C.CString(port)
	defer C.free(unsafe.Pointer(p))
	return int(C.uart_open(&dev, p, C.uint32_t(baud)))
}

// UARTCloseSafe calls uart_close with fd=-1 and must not crash.
func UARTCloseSafe() {
	var dev C.uart_dev_t
	dev.fd = -1
	C.uart_close(&dev)
}

// ── SPI ───────────────────────────────────────────────────────────────────────

func SPIOpen(device string, speed uint32, mode uint8) int {
	var dev C.spi_dev_t
	d := C.CString(device)
	defer C.free(unsafe.Pointer(d))
	return int(C.spi_open(&dev, d, C.uint32_t(speed), C.uint8_t(mode)))
}

// ── BME280 ────────────────────────────────────────────────────────────────────

func BME280InitNull() int {
	return int(C.bme280_init(nil))
}

func BME280GetSensorDataNullDev() int {
	var data C.struct_bme280_data
	return int(C.bme280_get_sensor_data(C.BME280_ALL, &data, nil))
}

func BME280CompensateNullCalib() int {
	var uncomp C.struct_bme280_uncomp_data
	var comp C.struct_bme280_data
	return int(C.bme280_compensate_data(C.BME280_ALL, &uncomp, &comp, nil))
}
